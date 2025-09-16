from flask import Flask
from routes.imoveis import bp as imoveis_bp

def create_app(repo):
    app = Flask(__name__)
    # injeta o repositório (FakeRepo nos testes; MySQL em prod)
    app.config["REPO"] = repo
    app.register_blueprint(imoveis_bp)
    return app
