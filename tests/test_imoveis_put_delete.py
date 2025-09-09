def test_atualiza_existente_parcial(client):
    patch = {"valor": 640000.0, "tipo": "apartamento"}
    resp = client.put("/imoveis/2", json=patch)
    assert resp.status_code in (200, 204)
    get = client.get("/imoveis/2")
    assert get.status_code == 200
    item = get.get_json()
    assert item["valor"] == 640000.0
    assert item["tipo"] == "apartamento"

def test_atualiza_inexistente(client):
    assert client.put("/imoveis/999", json={"valor": 1.0}).status_code == 404

def test_remove_existente(client):
    assert client.delete("/imoveis/3").status_code == 204
    assert client.get("/imoveis/3").status_code == 404

def test_remove_inexistente(client):
    assert client.delete("/imoveis/999").status_code == 404
