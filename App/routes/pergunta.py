from flask import Blueprint, jsonify, request
from App.database import conectar
from flask_jwt_extended import jwt_required

pergunta_bp = Blueprint('pergunta', __name__)

@pergunta_bp.route('/perguntas', methods=['GET'])
@jwt_required()
def listar_perguntas():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM pergunta")
    perguntas = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(perguntas)


# Prioridade 3 - Criar pergunta
@pergunta_bp.route('/perguntas', methods=['POST'])
@jwt_required()
def criar_pergunta():
    dados = request.json

    tipo = dados.get('tipo')                # texto_livre, multipla_escolha ou sim_nao
    texto = dados.get('texto')
    id_relatorio = dados.get('id_relatorio')

    if not tipo or not id_relatorio:
        return jsonify({"mensagem": "tipo e id_relatorio são obrigatórios."}), 400

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO pergunta (tipo, Texto, Id_relatorio) VALUES (%s, %s, %s)",
        (tipo, texto, id_relatorio)
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Pergunta criada com sucesso!", "id_pergunta": novo_id}), 201
