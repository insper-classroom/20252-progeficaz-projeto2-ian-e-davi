from flask import Blueprint, current_app, request, jsonify, url_for, Response

bp = Blueprint("imoveis", __name__)

REQUIRED_FIELDS = {
    "logradouro", "tipo_logradouro", "bairro", "cidade",
    "cep", "tipo", "valor", "data_aquisicao"
}

def repo():
    return current_app.config["REPO"]


def _is_json_ct():
    ct = (request.headers.get("Content-Type") or "").lower()
    return ct.startswith("application/json")

def _ensure_json():
    if not _is_json_ct():
        return jsonify({"erro": "Content-Type deve ser application/json"}), 415
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"erro": "JSON inválido"}), 400
    return data

def _is_date_iso(s: str) -> bool:
    from datetime import datetime
    try:
        datetime.fromisoformat(s)
        return True
    except Exception:
        return False


try:
    from domain.validators import validate_create as _validate_create_ext
    from domain.validators import validate_update as _validate_update_ext
except Exception:
    _validate_create_ext = None
    _validate_update_ext = None

def _validate_create(data: dict):
    faltando = [c for c in REQUIRED_FIELDS if c not in data]
    if faltando:
        return False, {"erro": f"faltando campos: {', '.join(faltando)}"}
    if not isinstance(data.get("valor"), (int, float)):
        return False, {"erro": "valor deve ser numérico"}
    if not _is_date_iso(data.get("data_aquisicao", "")):
        return False, {"erro": "data_aquisicao deve ser ISO (YYYY-MM-DD)"}
    return True, None

def _validate_update(data: dict, mode: str = "patch"):
    if not isinstance(data, dict) or not data:
        return False, {"erro": "payload vazio"}
    if "valor" in data and not isinstance(data["valor"], (int, float)):
        return False, {"erro": "valor deve ser numérico"}
    if "data_aquisicao" in data and not _is_date_iso(data["data_aquisicao"]):
        return False, {"erro": "data_aquisicao deve ser ISO (YYYY-MM-DD)"}
    return True, None

def _validate_create_any(data: dict):
    if _validate_create_ext:
        try:
            return _validate_create_ext(data)
        except Exception:
            pass
    return _validate_create(data)

def _validate_update_any(data: dict, mode: str):
    if _validate_update_ext:
        try:
            return _validate_update_ext(data, mode=mode) 
        except TypeError:
            return _validate_update_ext(data)            
        except Exception:
            pass
    return _validate_update(data, mode=mode)

# ------------------------------ Rotas ----------------------------------------

@bp.get("/imoveis")
def listar():
    tipo = request.args.get("tipo")
    cidade = request.args.get("cidade")
    r = repo()
    if hasattr(r, "list_all"):
        try:
            itens = r.list_all(tipo=tipo, cidade=cidade)
        except TypeError:
            itens = r.list_all()
            if tipo:
                itens = [i for i in itens if (i.get("tipo") or "").lower() == tipo.lower()]
            if cidade:
                itens = [i for i in itens if (i.get("cidade") or "").lower() == cidade.lower()]
    else:
        itens = []

    if _hateoas_enabled():
        return jsonify(_wrap_collection(itens)), 200
    return jsonify(itens), 200


@bp.get("/imoveis/<int:_id>")
def detalhe(_id):
    r = repo()
    get_fn = getattr(r, "get", getattr(r, "get_by_id"))
    item = get_fn(_id)
    if not item:
        return jsonify({"erro": "não encontrado"}), 404

    if _hateoas_enabled():
        return jsonify({**item, "_links": _links_item(item)}), 200
    return jsonify(item), 200


@bp.post("/imoveis")
def criar():
    data = _ensure_json()
    if isinstance(data, tuple):  
        return data

    ok, err = _validate_create_any(data)
    if not ok:
        return jsonify(err), 400

    created = repo().create(data)
    if not created:
        return jsonify({"erro": "id duplicado"}), 409

    loc = url_for("imoveis.detalhe", _id=created["id"])
    return Response(status=201, headers={"Location": loc})

@bp.put("/imoveis/<int:_id>")
def atualizar(_id):
    data = _ensure_json()
    if isinstance(data, tuple):
        return data

    ok, err = _validate_update_any(data, mode="put")
    if not ok:
        return jsonify(err), 400

    r = repo()
    get_fn = getattr(r, "get", getattr(r, "get_by_id"))
    cur = get_fn(_id)
    if not cur:
        return jsonify({"erro": "não encontrado"}), 404

    updated = r.update(_id, data)
    return jsonify(updated), 200

@bp.patch("/imoveis/<int:_id>")
def patch(_id):
    data = _ensure_json()
    if isinstance(data, tuple):
        return data

    ok, err = _validate_update_any(data, mode="patch")
    if not ok:
        return jsonify(err), 400

    r = repo()
    get_fn = getattr(r, "get", getattr(r, "get_by_id"))
    cur = get_fn(_id)
    if not cur:
        return jsonify({"erro": "não encontrado"}), 404

    updated = r.update(_id, data)
    return jsonify(updated), 200

@bp.delete("/imoveis/<int:_id>")
def remover(_id):
    r = repo()
    get_fn = getattr(r, "get", getattr(r, "get_by_id"))
    if not get_fn(_id):
        return jsonify({"erro": "não encontrado"}), 404
    ok = r.delete(_id)
    if not ok:
        return jsonify({"erro": "conflito na remoção"}), 409
    return Response(status=204)

@bp.get("/health")
def health():
    return {"status": "ok"}, 200

# ---------------------- HATEOAS (helpers) ------------------------------------

def _hateoas_enabled() -> bool:
    
    if current_app.config.get("ENABLE_HATEOAS") is True:
        return True
    
    acc = (request.headers.get("Accept") or "").lower()
    if "application/hal+json" in acc:
        return True
    
    for key in ("_hal", "_hateoas"):
        val = (request.args.get(key) or "").lower()
        if val in ("1", "true", "yes", "on"):
            return True
    return False


def _links_item(it: dict):
    _id = it["id"]
    return {
        "self":   {"href": url_for("imoveis.detalhe", _id=_id)},
        "update": {"href": url_for("imoveis.atualizar", _id=_id), "method": "PUT"},
        "patch":  {"href": url_for("imoveis.patch", _id=_id), "method": "PATCH"},
        "delete": {"href": url_for("imoveis.remover", _id=_id), "method": "DELETE"},
    }

def _wrap_collection(items: list):
    return {
        "_links": {
            "self":   {"href": url_for("imoveis.listar")},
            "create": {"href": url_for("imoveis.criar"), "method": "POST"},
        },
        "count": len(items),
        "_embedded": {
            "imoveis": [{**it, "_links": _links_item(it)} for it in items]
        },
    }

