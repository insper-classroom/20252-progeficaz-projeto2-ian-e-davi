# tests/test_http_codes.py

def _novo(**overrides):
    base = {
        "logradouro": "Praça 9 de Julho",
        "tipo_logradouro": "praça",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "cep": "01010-010",
        "tipo": "casa",
        "valor": 820000.0,
        "data_aquisicao": "2022-11-30",
    }
    base.update(overrides)
    return base


def _id_from_location(resp):
    loc = resp.headers.get("Location")
    assert loc, "POST deve retornar Location"
    return int(loc.rstrip("/").split("/")[-1])


def test_post_201_location(client):
    r = client.post("/imoveis", json=_novo())
    assert r.status_code == 201
    assert "Location" in r.headers
    # consegue acessar o recurso pelo Location?
    loc = r.headers["Location"]
    r2 = client.get(loc)
    assert r2.status_code == 200


def test_post_415_quando_nao_json(client):
    r = client.post("/imoveis", data="{}", headers={"Content-Type": "text/plain"})
    assert r.status_code == 415


def test_post_400_quando_payload_incompleto(client):
    r = client.post("/imoveis", json={"cidade": "SP"})
    assert r.status_code == 400


def test_get_404_quando_inexistente(client):
    r = client.get("/imoveis/99999")
    assert r.status_code == 404


def test_put_404_quando_inexistente(client):
    r = client.put("/imoveis/99999", json=_novo())
    assert r.status_code == 404


def test_put_200_atualiza_total_em_existente(client):
    # seu repo já vem com id=1 existente no conftest
    r = client.put("/imoveis/1", json=_novo(cidade="Campinas"))
    assert r.status_code == 200
    body = r.get_json()
    assert body["cidade"] == "Campinas"


def test_patch_200_atualiza_parcial_em_existente(client):
    # repo já tem id=2
    r = client.patch("/imoveis/2", json={"cidade": "Santos"})
    assert r.status_code == 200
    body = r.get_json()
    assert body["cidade"] == "Santos"


def test_delete_204_e_depois_404(client):
    # repo já tem id=3
    r1 = client.delete("/imoveis/3")
    assert r1.status_code == 204
    r2 = client.delete("/imoveis/3")
    assert r2.status_code == 404
