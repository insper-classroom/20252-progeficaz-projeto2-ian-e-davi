import os
from flask import Blueprint, current_app, jsonify, request, url_for, abort
from repo import get_repo

bp = Blueprint("imoveis", __name__)
API = os.getenv("API_PREFIX", "/api/v1")

def linkify(item):
    _id = item["id"]
    item["links"] = [
        {"rel": "self", "href": f"{API}/imoveis/{_id}"},
        {"rel": "collection", "href": f"{API}/imoveis"},
    ]
    return item

def require_fields(payload, required=("titulo", "tipo", "cidade")):
    missing = [k for k in required if not payload.get(k)]
    if missing:
        abort(jsonify({"error": "Campos obrigatórios ausentes", "missing": missing}), 400)

@bp.get(f"{API}/imoveis")
def list_imoveis():
    repo = get_repo()
    items = [linkify(x) for x in repo.list_all()]
    return jsonify({"count": len(items), "items": items, "links": [{"rel":"self","href":f"{API}/imoveis"}]}), 200

@bp.get(f"{API}/imoveis/<int:_id>")
def get_imovel(_id):
    repo = get_repo()
    item = repo.get_by_id(_id)
    if not item:
        abort(jsonify({"error":"Imóvel não encontrado"}), 404)
    return jsonify(linkify(item)), 200

@bp.post(f"{API}/imoveis")
def create_imovel():
    repo = get_repo()
    payload = request.get_json(silent=True) or {}
    require_fields(payload)
    created = repo.create(payload)
    location = f"{API}/imoveis/{created['id']}"
    return jsonify(linkify(created)), 201, {"Location": location}

@bp.put(f"{API}/imoveis/<int:_id>")
def update_imovel(_id):
    repo = get_repo()
    if not repo.get_by_id(_id):
        abort(jsonify({"error":"Imóvel não encontrado"}), 404)
    payload = request.get_json(silent=True) or {}
    require_fields(payload)  # PUT exige os obrigatórios
    updated = repo.update(_id, payload)
    return jsonify(linkify(updated)), 200

@bp.patch(f"{API}/imoveis/<int:_id>")
def patch_imovel(_id):
    repo = get_repo()
    if not repo.get_by_id(_id):
        abort(jsonify({"error":"Imóvel não encontrado"}), 404)
    payload = request.get_json(silent=True) or {}
    updated = repo.update(_id, payload)  # PATCH aceita parcial
    return jsonify(linkify(updated)), 200

@bp.delete(f"{API}/imoveis/<int:_id>")
def delete_imovel(_id):
    repo = get_repo()
    if not repo.get_by_id(_id):
        abort(jsonify({"error":"Imóvel não encontrado"}), 404)
    ok = repo.delete(_id)
    return ("", 204) if ok else (jsonify({"error":"Não foi possível remover"}), 409)
