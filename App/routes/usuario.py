"""Autenticação e administração de usuários."""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

from App.auth import GESTOR, requer_tipo, senha_forte
from App.database import conectar
from App.extensions import limiter

usuario_bp = Blueprint("usuario", __name__)


@usuario_bp.get("/verificar-token")
@jwt_required()
def verificar_token():
    return jsonify({"valido": True, "tipo": get_jwt().get("tipo")}), 200


@usuario_bp.get("/usuarios")
@requer_tipo(GESTOR)
def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    conexao.close()

    campos_sensiveis = {"senha", "codigo_recuperacao", "codigo_expira"}
    for usuario in usuarios:
        for campo in list(usuario):
            if campo.lower() in campos_sensiveis:
                usuario.pop(campo, None)

    return jsonify(usuarios)


@usuario_bp.post("/definir-senha-inicial")
@jwt_required()
def definir_senha_inicial():
    dados = request.get_json(silent=True) or {}
    nova_senha = dados.get("nova_senha")

    if not senha_forte(nova_senha):
        return jsonify({"mensagem": "A senha não atende aos requisitos de segurança."}), 400

    matricula = get_jwt_identity()
    senha_hash = generate_password_hash(nova_senha)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE usuario SET senha = %s, senha_temporaria = FALSE WHERE matricula = %s",
        (senha_hash, matricula),
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Senha definida com sucesso!"}), 200


@usuario_bp.post("/login")
@limiter.limit("5 per minute")
def login():
    dados = request.get_json(silent=True) or {}
    email = dados.get("e_mail")
    senha = dados.get("senha")

    if not email or not senha:
        return jsonify({"mensagem": "Informe e-mail e senha."}), 400

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE e_mail = %s", (email,))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not usuario or not check_password_hash(usuario["senha"], senha):
        return jsonify({"mensagem": "Email ou senha incorretos!"}), 401

    identidade = str(usuario["matricula"])
    tipo = str(usuario["Tipo"]).strip().lower()
    claims_extras = {
        "tipo": tipo,
        "nome": usuario["nome"],
        "senha_temporaria": bool(usuario.get("senha_temporaria", False)),
    }

    access = create_access_token(identity=identidade, additional_claims=claims_extras)
    refresh = create_refresh_token(identity=identidade, additional_claims=claims_extras)

    return jsonify(
        {
            "access_token": access,
            "refresh_token": refresh,
            "tipo": tipo,
            "senha_temporaria": claims_extras["senha_temporaria"],
            "mensagem": "Login realizado com sucesso!",
        }
    )


@usuario_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identidade_atual = get_jwt_identity()
    claims_atuais = get_jwt()
    claims_extras = {
        "tipo": claims_atuais.get("tipo"),
        "nome": claims_atuais.get("nome"),
        "senha_temporaria": claims_atuais.get("senha_temporaria", False),
    }
    novo_access_token = create_access_token(
        identity=identidade_atual,
        additional_claims=claims_extras,
    )
    return jsonify(access_token=novo_access_token)
