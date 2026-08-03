from flask import Blueprint, jsonify, request
from database import conectar
from datetime import datetime, timedelta
import random
import os
import resend
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.environ["RESEND_API_KEY"]

recuperacao_bp = Blueprint('recuperacao', __name__)


def gerar_codigo():
    return str(random.randint(100000, 999999))


# Prioridade - Solicitar código de recuperação
@recuperacao_bp.route('/recuperar-senha', methods=['POST'])
def recuperar_senha():
    dados = request.json
    email = dados.get('email')

    if not email:
        return jsonify({"mensagem": "Informe o e-mail."}), 400

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario FROM usuario WHERE e_mail = %s", (email,))
    usuario = cursor.fetchone()

    if not usuario:
        cursor.close()
        conexao.close()
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
    conexao.close()

    try:
        resend.Emails.send({
            "from": "ARCO <onboarding@resend.dev>",  # troque pelo seu domínio verificado no Resend
            "to": [email],
            "subject": "Código de recuperação de senha - ARCO",
            "html": f"<p>Seu código de recuperação é: <strong>{codigo}</strong></p><p>Ele expira em 10 minutos.</p>"
        })
    except Exception as erro:
        print("Erro ao enviar e-mail:", erro)
        return jsonify({"mensagem": "Erro ao enviar o e-mail. Tente novamente."}), 500

    return jsonify({"mensagem": "Código enviado para o e-mail."}), 200


# Prioridade - Validar código digitado
@recuperacao_bp.route('/verificar-codigo', methods=['POST'])
def verificar_codigo():
    dados = request.json
    email = dados.get('email')
    codigo = dados.get('codigo')

    if not email or not codigo:
        return jsonify({"mensagem": "Dados incompletos."}), 400

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute(
        "SELECT codigo_recuperacao, codigo_expira FROM usuario WHERE e_mail = %s",
        (email,)
    )
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not usuario or not usuario['codigo_recuperacao'] or usuario['codigo_recuperacao'] != codigo:
        return jsonify({"mensagem": "Código inválido."}), 400

    if usuario['codigo_expira'] and datetime.now() > usuario['codigo_expira']:
        return jsonify({"mensagem": "Código expirado. Solicite um novo."}), 400

    return jsonify({"mensagem": "Código validado com sucesso!"}), 200


# Prioridade - Redefinir a senha
@recuperacao_bp.route('/redefinir-senha', methods=['POST'])
def redefinir_senha():
    dados = request.json
    email = dados.get('email')
    nova_senha = dados.get('nova_senha')

    if not email or not nova_senha:
        return jsonify({"mensagem": "Dados incompletos."}), 400

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE usuario SET senha = %s, codigo_recuperacao = NULL, codigo_expira = NULL WHERE e_mail = %s",
        (nova_senha, email)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Senha redefinida com sucesso!"}), 200