import os, pytest
from app import create_app
from repo.mysql_repo import ImoveisRepo as MySQLRepo

skip_no_db = pytest.mark.skipif(
    not os.getenv("DATABASE_URL"),
    reason="DATABASE_URL não configurado; pulando testes de integração."
)

@skip_no_db
def test_mysql_crud_basico():
    repo = MySQLRepo()
    app = create_app(repo=repo)
    client = app.test_client()

    # CREATE
    novo = {"logradouro":"Praça XPTO","cidade":"Campinas","tipo":"terreno","valor":123.45,"data_aquisicao":"2022-01-01"}
    r = client.post("/imoveis", json=novo)
    assert r.status_code == 201
    loc = r.headers["Location"]

    # GET
    g = client.get(loc)
    assert g.status_code == 200
    assert g.get_json()["cidade"] == "Campinas"

    # DELETE
    assert client.delete(loc.replace("/api/v1","")).status_code in (204, 404)  # se mudar prefixo, ajuste aqui
