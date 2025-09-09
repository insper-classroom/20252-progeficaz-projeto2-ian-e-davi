def test_lista_todos_imoveis(client):
    resp = client.get("/imoveis")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list) and len(data) == 3
    campos = {"id", "logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao"}
    assert campos.issubset(data[0].keys())

def test_busca_por_id_existente(client):
    resp = client.get("/imoveis/2")
    assert resp.status_code == 200
    item = resp.get_json()
    assert item["cidade"] == "São Paulo"
    assert item["tipo"] == "apartamento"

def test_busca_por_id_inexistente(client):
    assert client.get("/imoveis/999").status_code == 404

def test_filtra_por_tipo(client):
    resp = client.get("/imoveis?tipo=apartamento")
    assert resp.status_code == 200
    data = resp.get_json()
    assert all(i["tipo"] == "apartamento" for i in data)

def test_filtra_por_cidade(client):
    resp = client.get("/imoveis?cidade=Campinas")
    assert resp.status_code == 200
    data = resp.get_json()
    assert all(i["cidade"] == "Campinas" for i in data)
