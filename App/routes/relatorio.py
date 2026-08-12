from flask import Blueprint, jsonify, request
from App.database import conectar
from flask_jwt_extended import jwt_required
from App.auth import matricula_atual, is_gestor, is_apoio

relatorio_bp = Blueprint('relatorio', __name__)


@relatorio_bp.route('/relatorios', methods=['GET'])
@jwt_required()
def listar_relatorios():
    """
    - gestor: vê todos os relatórios, sem restrição.
    - equipe de apoio: vê todos os relatórios (leitura ampla).
    - profissional (professor): vê SOMENTE os relatórios em que ele é o autor.
    """
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)

    if is_gestor() or is_apoio():
        cursor.execute("SELECT * FROM relatorio")
    else:
        cursor.execute(
            "SELECT * FROM relatorio WHERE `MATRICULA.PROF` = %s",
            (matricula_atual(),)
        )

    relatorios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(relatorios)


@relatorio_bp.route('/relatorios/<int:id_relatorio>', methods=['GET'])
@jwt_required()
def obter_relatorio(id_relatorio):
    """Busca um relatório específico, respeitando a mesma regra de dono."""
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM relatorio WHERE id_relatorio = %s", (id_relatorio,))
    relatorio = cursor.fetchone()
    cursor.close()
    conexao.close()

    if not relatorio:
        return jsonify({"mensagem": "Relatório não encontrado."}), 404

    dono = relatorio["MATRICULA.PROF"] == matricula_atual()
    if not (is_gestor() or is_apoio() or dono):
        return jsonify({"mensagem": "Você não tem permissão para ver este relatório."}), 403

    return jsonify(relatorio)


# Prioridade 3 - Criar relatório
@relatorio_bp.route('/relatorios', methods=['POST'])
@jwt_required()
def criar_relatorio():
    """
    Todo mundo (gestor, profissional, equipe de apoio) só consegue criar
    relatório em nome de si mesmo: a matrícula do autor vem sempre do
    token (matricula_atual), nunca de um campo enviado pelo cliente -
    isso evita que alguém crie relatório "fingindo" ser outro usuário.
    """
    dados = request.json
    matricula_prof = matricula_atual()

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


@relatorio_bp.route('/relatorios/<int:id_relatorio>', methods=['PUT'])
@jwt_required()
def editar_relatorio(id_relatorio):
    """Só o gestor ou o próprio autor podem editar um relatório."""
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM relatorio WHERE id_relatorio = %s", (id_relatorio,))
    relatorio = cursor.fetchone()

    if not relatorio:
        cursor.close()
        conexao.close()
        return jsonify({"mensagem": "Relatório não encontrado."}), 404

    dono = relatorio["MATRICULA.PROF"] == matricula_atual()
    if not (is_gestor() or dono):
        cursor.close()
        conexao.close()
        return jsonify({"mensagem": "Você não tem permissão para editar este relatório."}), 403

    dados = request.json
    status = dados.get('status', relatorio['Status'])
    data = dados.get('data', relatorio['DATA'])
    tipo_relatorio = dados.get('tipo_relatorio', relatorio['Tipo_Relatorio'])

    cursor.execute(
        "UPDATE relatorio SET Status = %s, DATA = %s, Tipo_Relatorio = %s WHERE id_relatorio = %s",
        (status, data, tipo_relatorio, id_relatorio)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Relatório atualizado com sucesso!"})
