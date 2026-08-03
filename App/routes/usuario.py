from flask import Blueprint, jsonify, request
from database import conectar
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)

usuario_bp = Blueprint('usuario', __name__)

@usuario_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def listar_usuarios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(usuarios)

@usuario_bp.route('/login', methods=['POST'])
def login():
    dados = request.json
    email = dados.get('e_mail')
    senha = dados.get('senha')

    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE e_mail = %s AND senha = %s", (email, senha))
    usuario = cursor.fetchone()
    cursor.close()
    conexao.close()

    if usuario:
        # Usamos a matrícula como identidade do token, pois é ela que
        # as tabelas de relatório usam para referenciar o profissional.
        identidade = usuario['matricula']

        access = create_access_token(identity=identidade)
        refresh = create_refresh_token(identity=identidade)

        return jsonify(
            access_token=access,
            refresh_token=refresh,
            mensagem="Login realizado com sucesso!"
        )
    else:
        return jsonify({"mensagem": "Email ou senha incorretos!"}), 401


# Prioridade 5 - Rota de refresh token
@usuario_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identidade_atual = get_jwt_identity()
    novo_access_token = create_access_token(identity=identidade_atual)
    return jsonify(access_token=novo_access_token)