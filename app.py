from flask import Flask, jsonify
from routes.imoveis import bp as imoveis_bp
import os

def create_app():
    app = Flask(__name__)
    app.register_blueprint(imoveis_bp)

    @app.get(os.getenv("API_PREFIX", "/api/v1") + "/health")
    def health():
        return jsonify({"status":"ok"}), 200

    return app

app = create_app()
