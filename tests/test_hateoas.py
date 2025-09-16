# tests/test_hateoas.py

HEADERS_HAL = {"Accept": "application/hal+json"}

def test_hateoas_item(client):
    r = client.get("/imoveis/1?_hal=1", headers=HEADERS_HAL)
    assert r.status_code == 200
    j = r.get_json()
    assert "_links" in j
    for k in ("self", "update", "patch", "delete"):
        assert k in j["_links"]
        assert "href" in j["_links"][k]

def test_hateoas_lista(client):
    r = client.get("/imoveis?_hal=1", headers=HEADERS_HAL)
    assert r.status_code == 200
    j = r.get_json()
    # coleção com _links + _embedded
    assert "_links" in j and "_embedded" in j
    assert "self" in j["_links"] and "create" in j["_links"]
    assert "imoveis" in j["_embedded"]
    imoveis = j["_embedded"]["imoveis"]
    if imoveis:
        assert "_links" in imoveis[0]
        for k in ("self", "update", "patch", "delete"):
            assert k in imoveis[0]["_links"]
            assert "href" in imoveis[0]["_links"][k]
