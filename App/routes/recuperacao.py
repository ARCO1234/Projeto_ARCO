"""Fluxo seguro de recuperação de senha por código de e-mail."""

import logging
import os
import secrets
from datetime import datetime, timedelta

import resend
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import generate_password_hash

from App.auth import senha_forte
from App.database import conectar
from App.extensions import limiter

logger = logging.getLogger(__name__)
recuperacao_bp = Blueprint("recuperacao", __name__)


def gerar_codigo():
    return str(secrets.randbelow(900000) + 100000)


@recuperacao_bp.post("/recuperar-senha")
@limiter.limit("3 per minute")
def recuperar_senha():
    dados = request.get_json(silent=True) or {}
    email = dados.get("email")

    if not email:
        return jsonify({"mensagem": "Informe o e-mail."}), 400

    api_key = os.getenv("RESEND_API_KEY")
    if not api_key:
        logger.error("RESEND_API_KEY não configurada.")
        return jsonify({"mensagem": "Serviço de e-mail ainda não configurado."}), 503

    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario FROM usuario WHERE e_mail = %s", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            cursor.close()
            return jsonify({"mensagem": "Se o e-mail existir, um código foi enviado."}), 200

        codigo = gerar_codigo()
        expira = datetime.now() + timedelta(minutes=10)

        cursor.execute(
            "UPDATE usuario SET codigo_recuperacao = %s, codigo_expira = %s WHERE e_mail = %s",
            (codigo, expira, email),
        )
        conexao.commit()
        cursor.close()
    except Exception:
        logger.exception("Erro ao gerar ou salvar o código de recuperação.")
        return jsonify({"mensagem": "Erro interno. Tente novamente."}), 500
    finally:
        if conexao:
            conexao.close()

    try:
        resend.api_key = api_key
        resend.Emails.send(
            {
                "from": "ARCO <onboarding@resend.dev>",
                "to": [email],
                "subject": "Código de recuperação de senha - ARCO",
                "html": (
                    f"<p>Seu código de recuperação é: <strong>{codigo}</strong></p>"
                    "<p>Ele expira em 10 minutos.</p>"
                ),
            }
        )
    except Exception:
        logger.exception("Erro ao enviar o e-mail de recuperação.")
        return jsonify({"mensagem": "Erro ao enviar o e-mail. Tente novamente."}), 500

    return jsonify({"mensagem": "Código enviado para o e-mail."}), 200


@recuperacao_bp.post("/verificar-codigo")
@limiter.limit("5 per minute")
def verificar_codigo():
    dados = request.get_json(silent=True) or {}
    email = dados.get("email")
    codigo = str(dados.get("codigo", ""))

    if not email or not codigo:
        return jsonify({"mensagem": "Dados incompletos."}), 400

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT codigo_recuperacao, codigo_expira FROM usuario WHERE e_mail = %s",
            (email,),
        )
        usuario = cursor.fetchone()
        cursor.close()
        conexao.close()
    except Exception:
        logger.exception("Erro ao verificar o código de recuperação.")
        return jsonify({"mensagem": "Erro interno. Tente novamente."}), 500

    codigo_salvo = str(usuario["codigo_recuperacao"]) if usuario and usuario["codigo_recuperacao"] else ""

    if not codigo_salvo or not secrets.compare_digest(codigo_salvo, codigo):
        return jsonify({"mensagem": "Código inválido."}), 400

    if usuario["codigo_expira"] and datetime.now() > usuario["codigo_expira"]:
        return jsonify({"mensagem": "Código expirado. Solicite um novo."}), 400

    reset_token = create_access_token(
        identity=email,
        additional_claims={"purpose": "password_reset"},
        expires_delta=timedelta(minutes=10),
    )
    return jsonify(
        {
            "mensagem": "Código validado com sucesso!",
            "reset_token": reset_token,
        }
    ), 200


@recuperacao_bp.post("/redefinir-senha")
@jwt_required()
def redefinir_senha():
    if get_jwt().get("purpose") != "password_reset":
        return jsonify({"mensagem": "Autorização inválida para redefinir senha."}), 403

    dados = request.get_json(silent=True) or {}
    nova_senha = dados.get("nova_senha")
    email = get_jwt_identity()

    if not senha_forte(nova_senha):
        return jsonify({"mensagem": "A senha não atende aos requisitos de segurança."}), 400

    senha_hash = generate_password_hash(nova_senha)

    try:
        conexao = conectar()
        cursor = conexao.cursor()
        cursor.execute(
            """
            UPDATE usuario
            SET senha = %s, codigo_recuperacao = NULL, codigo_expira = NULL
            WHERE e_mail = %s
            """,
            (senha_hash, email),
        )
        conexao.commit()
        cursor.close()
        conexao.close()
    except Exception:
        logger.exception("Erro ao redefinir senha.")
        return jsonify({"mensagem": "Erro interno. Tente novamente."}), 500

    return jsonify({"mensagem": "Senha redefinida com sucesso!"}), 200
