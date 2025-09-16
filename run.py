from app import create_app
from repo.fake_repo import ImoveisRepo as FakeRepo

seed = [
    {"id": 1, "logradouro": "Rua 1", "tipo_logradouro": "rua", "bairro": "Centro", "cidade": "São Paulo",
     "cep": "01000-000", "tipo": "casa", "valor": 500000.0, "data_aquisicao": "2020-01-01"},
    {"id": 2, "logradouro": "Av 2", "tipo_logradouro": "avenida", "bairro": "Jardins", "cidade": "São Paulo",
     "cep": "01400-000", "tipo": "apartamento", "valor": 750000.0, "data_aquisicao": "2021-06-10"},
]
app = create_app(repo=FakeRepo(seed))
if __name__ == "__main__":
    app.run(debug=True)
