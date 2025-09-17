import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import pytest
from app import create_app
from repo.fake_repo import ImoveisRepo as FakeRepo  

@pytest.fixture
def repo():
    return FakeRepo([
        {"id": 1, "logradouro": "Rua 1", "tipo_logradouro": "rua", "bairro": "Centro",
         "cidade": "São Paulo", "cep": "01000-000", "tipo": "casa", "valor": 500000.0, "data_aquisicao": "2020-01-01"},
        {"id": 2, "logradouro": "Av 2", "tipo_logradouro": "avenida", "bairro": "Jardins",
         "cidade": "São Paulo", "cep": "01400-000", "tipo": "apartamento", "valor": 750000.0, "data_aquisicao": "2021-06-10"},
        {"id": 3, "logradouro": "Estrada 3", "tipo_logradouro": "estrada", "bairro": "Barão Geraldo",
         "cidade": "Campinas", "cep": "13083-000", "tipo": "terreno", "valor": 300000.0, "data_aquisicao": "2019-03-15"},
    ])

@pytest.fixture
def client(repo):
    app = create_app(repo=repo)
    app.config["TESTING"] = True
    return app.test_client()
