"""Registro central dos Blueprints do ARCO."""

from App.routes.aluno import aluno_bp
from App.routes.horario import horario_bp
from App.routes.pages import pages_bp
from App.routes.pergunta import pergunta_bp
from App.routes.recuperacao import recuperacao_bp
from App.routes.relatorio import relatorio_bp
from App.routes.resposta import resposta_bp
from App.routes.turma import turma_bp
from App.routes.usuario import usuario_bp

BLUEPRINTS = (
    pages_bp,
    usuario_bp,
    aluno_bp,
    turma_bp,
    relatorio_bp,
    horario_bp,
    pergunta_bp,
    resposta_bp,
    recuperacao_bp,
)
