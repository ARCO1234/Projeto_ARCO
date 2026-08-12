"""
Controle de acesso por papel (RBAC).

Papéis existentes (coluna `Tipo` da tabela `usuario`):
  - gestor           -> acesso total, sem restrição
  - profissional      -> só vê e interage com os PRÓPRIOS relatórios
  - equipe de apoio   -> vê tudo, mas só cria/edita os PRÓPRIOS relatórios

O papel do usuário é gravado como "claim" extra dentro do próprio JWT
no momento do login (veja routes/usuario.py), então não precisamos
consultar o banco de novo a cada requisição só para saber o papel.
"""

from functools import wraps
import re
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt, get_jwt_identity

GESTOR = "gestor"
PROFISSIONAL = "profissional"
APOIO = "equipe de apoio"


def senha_forte(senha):
    """Valida a mesma política exibida na tela de nova senha."""
    return bool(
        isinstance(senha, str)
        and 8 <= len(senha) <= 25
        and re.search(r"[A-Z]", senha)
        and re.search(r"[a-z]", senha)
        and re.search(r"\d", senha)
        and re.search(r"[^A-Za-z0-9]", senha)
    )


def requer_tipo(*tipos_permitidos):
    """
    Decorator que bloqueia a rota para quem não tiver um dos papéis
    informados. Gestor SEMPRE passa, independente da lista, porque
    gestão tem acesso irrestrito ao sistema.

    Uso:
        @relatorio_bp.route('/relatorios/tudo')
        @requer_tipo(GESTOR, APOIO)
        def rota():
            ...
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            tipo_usuario = get_jwt().get("tipo")

            if tipo_usuario == GESTOR:
                return f(*args, **kwargs)

            if tipo_usuario not in tipos_permitidos:
                return jsonify({"mensagem": "Você não tem permissão para acessar este recurso."}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator


def tipo_atual():
    """Retorna o papel (Tipo) do usuário logado, lido do token JWT atual."""
    return get_jwt().get("tipo")


def matricula_atual():
    """Retorna a matrícula (identidade) do usuário logado."""
    return get_jwt_identity()


def is_gestor():
    return tipo_atual() == GESTOR


def is_apoio():
    return tipo_atual() == APOIO


def is_profissional():
    return tipo_atual() == PROFISSIONAL
