"""Rotas responsáveis somente pelas páginas HTML."""

from flask import Blueprint, redirect, render_template, url_for

pages_bp = Blueprint("pages", __name__)


@pages_bp.get("/")
def index():
    return redirect(url_for("pages.login_page"))


@pages_bp.get("/login-page")
def login_page():
    return render_template("login.html")


@pages_bp.get("/Inicial-page")
def inicial_page():
    return render_template("inicial.html")


@pages_bp.get("/professor-page")
def professor_page():
    return render_template("inicioprof.html")


@pages_bp.get("/config-page")
def config_page():
    return render_template("config.html")


@pages_bp.get("/recsenha-page")
def recsenha_page():
    return render_template("recsenha.html")


@pages_bp.get("/nvsenha-page")
def nvsenha_page():
    return render_template("nvsenha.html")


@pages_bp.get("/boasenha-page")
def boasenha_page():
    return render_template("boasenha.html")


@pages_bp.get("/horario-page")
def horario_page():
    return render_template("profhorario.html")


@pages_bp.get("/notificacoes-page")
def notificacoes_page():
    return render_template("Notifprof.html")


@pages_bp.get("/relatorio-page")
def relatorio_page():
    return render_template("em_construcao.html", titulo="Relatórios")
