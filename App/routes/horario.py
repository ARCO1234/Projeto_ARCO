from flask import Blueprint, jsonify
from App.database import conectar
from flask_jwt_extended import jwt_required


horario_bp = Blueprint('horario', __name__)

@horario_bp.route('/horarios', methods=['GET'])
@jwt_required()

def listar_horarios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM horario")
    horarios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(horarios)
