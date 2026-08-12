from flask import Blueprint, jsonify
from App.database import conectar
from flask_jwt_extended import jwt_required


aluno_bp = Blueprint('aluno', __name__)

@aluno_bp.route('/alunos', methods=['GET'])
@jwt_required()

def listar_alunos():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM aluno")
    alunos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(alunos)


 
