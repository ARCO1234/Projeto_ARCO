from flask import Blueprint, jsonify
from App.database import conectar
from flask_jwt_extended import jwt_required

resposta_bp = Blueprint('resposta', __name__)

@resposta_bp.route('/respostas', methods=['GET'])
@jwt_required()
def listar_respostas():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resposta")
    respostas = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(respostas)
