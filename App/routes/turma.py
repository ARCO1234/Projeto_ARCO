from flask import Blueprint, jsonify
from App.database import conectar
from flask_jwt_extended import jwt_required

turma_bp = Blueprint('turma', __name__)

@turma_bp.route('/turmas', methods=['GET'])
@jwt_required()
def listar_turmas():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM turma")
    turmas = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(turmas)
