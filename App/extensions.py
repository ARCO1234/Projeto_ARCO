"""
Extensões compartilhadas do Flask (evita import circular entre app.py e as rotas).
"""

from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
jwt = JWTManager()
