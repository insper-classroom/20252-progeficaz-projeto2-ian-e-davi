from flask import Blueprint, current_app, request, jsonify, url_for, Response

bp = Blueprint("imoveis", __name__)

REQUIRED_MIN = {"logradouro", "cidade"}

def repo():
    return current_app.config["REPO"]

@bp.get("/imoveis")
def listar():
    tipo = request.args.get("tipo")
    cidade = request.args.get("cidade")
    # suporte a filtros na própria listagem
    r = repo()
    if hasattr(r, "list_all"):
        try:
            return jsonify(r.list_all(tipo=tipo, cidade=cidade)), 200
        except TypeError:
            # caso sua implementação antiga não aceite kwargs
            itens = r.list_all()
            if tipo:
                itens = [i for i in itens if (i.get("tipo") or "").lower() == tipo.lower()]
            if cidade:
                itens = [i for i in itens if (i.get("cidade") or "").lower() == cidade.lower()]
            return jsonify(itens), 200
    return jsonify([]), 200

@bp.get("/imoveis/<int:_id>")
def detalhe(_id):
    item = getattr(repo(), "get", getattr(repo(), "get_by_id"))(_id)
    if not item:
        return jsonify({"erro": "não encontrado"}), 404
    return jsonify(item), 200

@bp.post("/imoveis")
def criar():
    data = request.get_json(silent=True) or {}
    if not REQUIRED_MIN.issubset(data.keys()):
        return jsonify({"erro": "payload inválido: exigidos logradouro e cidade"}), 400
    created = repo().create(data)
    if not created:
        return jsonify({"erro": "id duplicado"}), 409
    loc = url_for("imoveis.detalhe", _id=created["id"])
    return Response(status=201, headers={"Location": loc})

@bp.put("/imoveis/<int:_id>")
def atualizar(_id):
    r = repo()
    get_fn = getattr(r, "get", getattr(r, "get_by_id"))
    if not get_fn(_id):
        return jsonify({"erro": "não encontrado"}), 404
    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"erro": "payload inválido"}), 400
    updated = r.update(_id, data)
    return jsonify(updated), 200

@bp.patch("/imoveis/<int:_id>")
def patch(_id):
    return atualizar(_id)

@bp.delete("/imoveis/<int:_id>")
def remover(_id):
    r = repo()
    get_fn = getattr(r, "get", getattr(r, "get_by_id"))
    if not get_fn(_id):
        return jsonify({"erro": "não encontrado"}), 404
    ok = r.delete(_id)
    return (Response(status=204) if ok else (jsonify({"erro": "conflito na remoção"}), 409))
