from flask import Blueprint, current_app, request, jsonify, url_for, Response

bp = Blueprint("imoveis", __name__)

# obrigatórios mínimos (do SQL): logradouro, cidade
REQUIRED_MIN = {"logradouro", "cidade"}

def repo():
    return current_app.config["REPO"]

@bp.get("/imoveis")
def listar():
    tipo = request.args.get("tipo")
    cidade = request.args.get("cidade")
    return jsonify(repo().list_all(tipo=tipo, cidade=cidade)), 200

@bp.get("/imoveis/<int:_id>")
def detalhe(_id):
    item = repo().get(_id)
    if not item:
        return jsonify({"erro": "não encontrado"}), 404
    return jsonify(item), 200

@bp.post("/imoveis")
def criar():
    data = request.get_json(silent=True) or {}
    # valida mínimos
    if not REQUIRED_MIN.issubset(set(data.keys())):
        return jsonify({"erro": "payload inválido: exigidos logradouro e cidade"}), 400

    created = repo().create(data)
    if not created:
        return jsonify({"erro": "id duplicado"}), 409

    loc = url_for("imoveis.detalhe", _id=created["id"])
    return Response(status=201, headers={"Location": loc})

@bp.put("/imoveis/<int:_id>")
def atualizar(_id):
    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"erro": "payload inválido"}), 400
    updated = repo().update(_id, data)
    if not updated:
        return jsonify({"erro": "não encontrado"}), 404
    return jsonify(updated), 200

@bp.delete("/imoveis/<int:_id>")
def remover(_id):
    ok = repo().delete(_id)
    if not ok:
        return jsonify({"erro": "não encontrado"}), 404
    return Response(status=204)
