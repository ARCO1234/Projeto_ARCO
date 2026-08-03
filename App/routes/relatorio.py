from flask import Blueprint, jsonify, request
from database import conectar
from flask_jwt_extended import jwt_required, get_jwt_identity

relatorio_bp = Blueprint('relatorio', __name__)

@relatorio_bp.route('/relatorios', methods=['GET'])
@jwt_required()
def listar_relatorios():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM relatorio")
    relatorios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(relatorios)


# Prioridade 3 - Criar relatório
@relatorio_bp.route('/relatorios', methods=['POST'])
@jwt_required()
def criar_relatorio():
    dados = request.json
    matricula_prof = get_jwt_identity()  # matrícula do profissional logado (vem do token)

    matricula_aluno = dados.get('matricula_aluno')
    status = dados.get('status', 'Rascunho')       # Publicado, Rascunho ou Não feito
    data = dados.get('data')                         # formato 'YYYY-MM-DD'
    tipo_relatorio = dados.get('tipo_relatorio')      # individual, turma ou incidente

    if not matricula_aluno or not tipo_relatorio:
        return jsonify({"mensagem": "matricula_aluno e tipo_relatorio são obrigatórios."}), 400

    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO relatorio (`MATRICULA-ALUNO`, `MATRICULA.PROF`, Status, DATA, Tipo_Relatorio)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (matricula_aluno, matricula_prof, status, data, tipo_relatorio)
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Relatório criado com sucesso!", "id_relatorio": novo_id}), 201