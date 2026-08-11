"""Configuração principal da aplicação Flask do ARCO."""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from App.extensions import jwt, limiter


def create_app(test_config=None):
    """Cria uma instância configurada da aplicação."""
    project_root = Path(__file__).resolve().parent.parent
    load_dotenv(project_root / ".env")

    app = Flask(__name__)

    secret_key = os.getenv("JWT_SECRET_KEY")
    if test_config and test_config.get("TESTING"):
        secret_key = secret_key or "chave-exclusiva-dos-testes"

    if not secret_key:
        raise RuntimeError(
            "JWT_SECRET_KEY não configurada. Copie .env.example para .env "
            "e defina uma chave segura antes de iniciar o ARCO."
        )

    app.config.from_mapping(
        JWT_SECRET_KEY=secret_key,
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=15),
        JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=1),
        JSON_AS_ASCII=False,
        RATELIMIT_STORAGE_URI=os.getenv("RATELIMIT_STORAGE_URI", "memory://"),
    )

    if test_config:
        app.config.update(test_config)

    jwt.init_app(app)
    limiter.init_app(app)

    from App.routes import BLUEPRINTS

    for blueprint in BLUEPRINTS:
        app.register_blueprint(blueprint)

    return app
