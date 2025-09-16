import os, pytest
from app import create_app
from repo.mysql_repo import ImoveisRepo

@pytest.mark.skipif(not os.getenv("DATABASE_URL"), reason="Sem DATABASE_URL")
def test_mysql_crud():
    app = create_app(repo=ImoveisRepo())
    client = app.test_client()

    novo = {"logradouro":"Rua Teste","cidade":"São Paulo","tipo":"casa","valor":123.45,"data_aquisicao":"2024-01-01"}
    r = client.post("/imoveis", json=novo)
    assert r.status_code == 201
    loc = r.headers["Location"]

    g = client.get(loc); assert g.status_code == 200
    uid = g.get_json()["id"]

    u = client.put(f"/imoveis/{uid}", json={"valor": 999.99})
    assert u.status_code == 200 and u.get_json()["valor"] == 999.99

    d = client.delete(f"/imoveis/{uid}"); assert d.status_code == 204
