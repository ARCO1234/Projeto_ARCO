from flask import Blueprint, jsonify, request
from database import conectar
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from werkzeug.security import check_password_hash
from auth import requer_tipo, GESTOR

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/verificar-token', methods=['GET'])
@jwt_required()
def verificar_token():
    """
    Rota mínima usada pelo front-end (auth-guard.js) só para saber se o
    token salvo no navegador ainda é válido. Qualquer papel logado passa.
    """
    return jsonify({"valido": True, "tipo": get_jwt().get("tipo")}), 200


@usuario_bp.route('/usuarios', methods=['GET'])
@requer_tipo(GESTOR)
def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(usuarios)

@usuario_bp.route('/definir-senha-inicial', methods=['POST'])
@jwt_required()
def definir_senha_inicial():
    """
    Usada logo após o primeiro login de quem entrou com senha temporária
    (importada do banco pré-existente). Diferente da recuperação de senha,
    aqui não precisa de código por e-mail porque a pessoa já provou quem
    é ao logar com a senha temporária.
    """
    from werkzeug.security import generate_password_hash

    dados = request.json
    nova_senha = dados.get('nova_senha')

    if not nova_senha or len(nova_senha) < 6:
        return jsonify({"mensagem": "A nova senha precisa ter pelo menos 6 caracteres."}), 400

    matricula = get_jwt_identity()
    senha_hash = generate_password_hash(nova_senha)

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE usuario SET senha = %s, senha_temporaria = FALSE WHERE matricula = %s",
        (senha_hash, matricula)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Senha definida com sucesso!"}), 200


@usuario_bp.route('/login', methods=['POST'])
def login():

    dados = request.json

    email = dados.get('e_mail')
    senha = dados.get('senha')

    if not email or not senha:
        return jsonify({"mensagem": "Informe e-mail e senha."}), 400

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuario WHERE e_mail=%s",
        (email,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if not usuario:
        return jsonify({"mensagem": "Email ou senha incorretos!"}), 401

    if not check_password_hash(usuario["senha"], senha):
        return jsonify({"mensagem": "Email ou senha incorretos!"}), 401

    identidade = usuario["matricula"]
    claims_extras = {
        "tipo": usuario["Tipo"],
        "nome": usuario["nome"],
        "senha_temporaria": bool(usuario.get("senha_temporaria", False)),
    }

    access = create_access_token(identity=identidade, additional_claims=claims_extras)

    refresh = create_refresh_token(identity=identidade, additional_claims=claims_extras)

    return jsonify({

        "access_token": access,

        "refresh_token": refresh,

        "tipo": usuario["Tipo"],

        "senha_temporaria": bool(usuario.get("senha_temporaria", False)),

        "tipo": usuario["Tipo"],

        "mensagem": "Login realizado com sucesso!"

    })


# Prioridade 5 - Rota de refresh token
@usuario_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identidade_atual = get_jwt_identity()
    claims_atuais = get_jwt()
    claims_extras = {"tipo": claims_atuais.get("tipo"), "nome": claims_atuais.get("nome")}
    novo_access_token = create_access_token(identity=identidade_atual, additional_claims=claims_extras)
    return jsonify(access_token=novo_access_token)