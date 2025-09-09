def test_cria_imovel_valido(client):
    novo = {
        # id opcional
        "logradouro": "Praça 9 de Julho",
        "tipo_logradouro": "praça",
        "bairro": "Centro",
        "cidade": "São Paulo",
        "cep": "01010-010",
        "tipo": "casa em condominio",
        "valor": 820000.0,
        "data_aquisicao": "2022-11-30"
    }
    resp = client.post("/imoveis", json=novo)
    assert resp.status_code == 201
    # pega Location e confirma
    loc = resp.headers.get("Location")
    assert loc
    get = client.get(loc)
    assert get.status_code == 200
    item = get.get_json()
    assert item["logradouro"] == "Praça 9 de Julho"
    assert item["tipo"] == "casa em condominio"

def test_cria_imovel_invalido_minimos(client):
    # falta logradouro e cidade
    resp = client.post("/imoveis", json={"tipo": "casa"})
    assert resp.status_code == 400

def test_cria_imovel_com_id_duplicado(client):
    duplicado = {
        "id": 1,
        "logradouro": "Rua X",
        "tipo_logradouro": "rua",
        "bairro": "Bairro X",
        "cidade": "São Paulo",
        "cep": "00000-000",
        "tipo": "casa",
        "valor": 1.0,
        "data_aquisicao": "2020-01-01"
    }
    resp = client.post("/imoveis", json=duplicado)
    assert resp.status_code in (400, 409)
