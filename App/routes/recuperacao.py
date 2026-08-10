from flask import Blueprint, jsonify, request
from database import conectar
from datetime import datetime, timedelta
import secrets
import os
import logging
import resend
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
try:
    from App.extensions import limiter
except ModuleNotFoundError:
    from extensions import limiter

load_dotenv()

logger = logging.getLogger(__name__)

RESEND_API_KEY = os.getenv("RESEND_API_KEY")

if not RESEND_API_KEY:
    raise RuntimeError(
        "RESEND_API_KEY não encontrada nas variáveis de ambiente. "
        "Defina essa variável no seu .env antes de iniciar a aplicação."
    )

resend.api_key = RESEND_API_KEY

recuperacao_bp = Blueprint('recuperacao', __name__)


def gerar_codigo():
    # secrets.randbelow é seguro para geração de códigos sensíveis (CSPRNG)
    return str(secrets.randbelow(900000) + 100000)


# Prioridade - Solicitar código de recuperação
@recuperacao_bp.route('/recuperar-senha', methods=['POST'])
@limiter.limit("3 per minute")
def recuperar_senha():
    dados = request.json
    email = dados.get('email')

    if not email:
        return jsonify({"mensagem": "Informe o e-mail."}), 400

    conexao = None
    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT id_usuario FROM usuario WHERE e_mail = %s", (email,))
        usuario = cursor.fetchone()

        if not usuario:
            cursor.close()
            logger.info("Solicitação de recuperação para e-mail não cadastrado.")
            # Não revelamos se o e-mail existe ou não (evita descobrirem quais e-mails estão cadastrados)
            return jsonify({"mensagem": "Se o e-mail existir, um código foi enviado."}), 200

        codigo = gerar_codigo()
        expira = datetime.now() + timedelta(minutes=10)

        cursor_update = conexao.cursor()
        cursor_update.execute(
            "UPDATE usuario SET codigo_recuperacao = %s, codigo_expira = %s WHERE e_mail = %s",
            (codigo, expira, email)
        )
        conexao.commit()
        cursor.close()
        cursor_update.close()
    except Exception:
        logger.exception("Erro ao gerar/salvar código de recuperação para %s", email)
        return jsonify({"mensagem": "Erro interno. Tente novamente."}), 500
    finally:
        if conexao:
            conexao.close()

    try:
        resend.Emails.send({
            "from": "ARCO <onboarding@resend.dev>",  # troque pelo seu domínio verificado no Resend
            "to": [email],
            "subject": "Código de recuperação de senha - ARCO",
            "html": f"<p>Seu código de recuperação é: <strong>{codigo}</strong></p><p>Ele expira em 10 minutos.</p>"
        })
    except Exception as erro:
        # Loga o erro REAL retornado pela Resend (ex: domínio não verificado,
        # destinatário fora do modo sandbox, chave inválida, etc.)
        logger.exception("Erro ao enviar e-mail de recuperação para %s: %s", email, erro)
        return jsonify({"mensagem": "Erro ao enviar o e-mail. Tente novamente."}), 500

    return jsonify({"mensagem": "Código enviado para o e-mail."}), 200


# Prioridade - Validar código digitado
@recuperacao_bp.route('/verificar-codigo', methods=['POST'])
@limiter.limit("5 per minute")
def verificar_codigo():
    dados = request.json
    email = dados.get('email')
    codigo = dados.get('codigo')

    if not email or not codigo:
        return jsonify({"mensagem": "Dados incompletos."}), 400

    try:
        conexao = conectar()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT codigo_recuperacao, codigo_expira FROM usuario WHERE e_mail = %s",
            (email,)
        )
        usuario = cursor.fetchone()
        cursor.close()
        conexao.close()
    except Exception:
        logger.exception("Erro ao verificar código de recuperação para %s", email)
        return jsonify({"mensagem": "Erro interno. Tente novamente."}), 500

    codigo_salvo = usuario['codigo_recuperacao'] if usuario else None

    if not codigo_salvo or not secrets.compare_digest(codigo_salvo, codigo):
        return jsonify({"mensagem": "Código inválido."}), 400

    if usuario['codigo_expira'] and datetime.now() > usuario['codigo_expira']:
        return jsonify({"mensagem": "Código expirado. Solicite um novo."}), 400

    return jsonify({"mensagem": "Código validado com sucesso!"}), 200


# Prioridade - Redefinir a senha
@recuperacao_bp.route('/redefinir-senha', methods=['POST'])
def redefinir_senha():

    dados = request.json

    email = dados.get("email")
    nova_senha = dados.get("nova_senha")

    if not email or not nova_senha:
        return jsonify({"mensagem": "Dados incompletos."}), 400

    senha_hash = generate_password_hash(nova_senha)

    try:
        conexao = conectar()
        cursor = conexao.cursor()

        cursor.execute(
            """
            UPDATE usuario
            SET senha=%s,
                codigo_recuperacao=NULL,
                codigo_expira=NULL
            WHERE e_mail=%s
            """,
            (
                senha_hash,
                email
            )
        )

        conexao.commit()
        cursor.close()
        conexao.close()
    except Exception:
        logger.exception("Erro ao redefinir senha para %s", email)
        return jsonify({"mensagem": "Erro interno. Tente novamente."}), 500

    return jsonify({
        "mensagem": "Senha redefinida com sucesso!"
    }), 200