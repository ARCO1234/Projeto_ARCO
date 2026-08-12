import re

import pytest

from App import create_app
from App.auth import senha_forte


@pytest.fixture()
def client():
    app = create_app({"TESTING": True, "RATELIMIT_ENABLED": False})
    return app.test_client()


@pytest.mark.parametrize(
    "path",
    [
        "/login-page",
        "/Inicial-page",
        "/professor-page",
        "/config-page",
        "/recsenha-page",
        "/nvsenha-page",
        "/boasenha-page",
        "/horario-page",
        "/notificacoes-page",
        "/relatorio-page",
    ],
)
def test_paginas_renderizam_e_estaticos_existem(client, path):
    resposta = client.get(path)
    assert resposta.status_code == 200

    html = resposta.get_data(as_text=True)
    arquivos = set(re.findall(r'''(?:src|href)=["'](/static/[^"']+)["']''', html))
    for arquivo in arquivos:
        assert client.get(arquivo).status_code == 200, arquivo


@pytest.mark.parametrize(
    "path",
    [
        "/verificar-token",
        "/usuarios",
        "/alunos",
        "/turmas",
        "/relatorios",
        "/horarios",
        "/perguntas",
        "/respostas",
    ],
)
def test_apis_protegidas_exigem_token(client, path):
    assert client.get(path).status_code == 401


def test_redefinir_senha_exige_token(client):
    assert client.post("/redefinir-senha", json={}).status_code == 401


def test_login_incompleto_nao_acessa_banco(client):
    resposta = client.post("/login", json={})
    assert resposta.status_code == 400


def test_recuperacao_incompleta_nao_acessa_banco(client):
    resposta = client.post("/recuperar-senha", json={})
    assert resposta.status_code == 400


def test_politica_de_senha():
    assert senha_forte("Arco#2026")
    assert not senha_forte("senha-fraca")
    assert not senha_forte("CURTA#2026")
