import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required

try:
    from App.database import conectar
except ModuleNotFoundError:
    from database import conectar

try:
    from App.extensions import limiter
except ModuleNotFoundError:
    from extensions import limiter
# Carrega variáveis do .env
load_dotenv()

# Importa as rotas somente depois do load_dotenv
import routes

app = Flask(__name__)
limiter.init_app(app)

# ------------------------
# CONFIGURAÇÕES
# ------------------------

CORS(app)

app.config["JWT_SECRET_KEY"] = os.getenv(
    "JWT_SECRET_KEY",
    "coloque_uma_chave_bem_grande_aqui"
)

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JSON_AS_ASCII"] = False

jwt = JWTManager(app)

# ------------------------
# BLUEPRINTS
# ------------------------

app.register_blueprint(routes.usuario_bp)
app.register_blueprint(routes.aluno_bp)
app.register_blueprint(routes.turma_bp)
app.register_blueprint(routes.relatorio_bp)
app.register_blueprint(routes.horario_bp)
app.register_blueprint(routes.pergunta_bp)
app.register_blueprint(routes.resposta_bp)
app.register_blueprint(routes.recuperacao_bp)

# ------------------------
# ROTAS HTML
# ------------------------

@app.route("/")
def index():
    # A raiz do site sempre leva para o login. Se o usuário já tiver um
    # token válido salvo no navegador, o próprio login.js poderia checar
    # isso e redirecionar para a Inicial - mas por padrão, mandamos
    # todo mundo para o login.
    return redirect(url_for("login_page"))


@app.route("/login-page")
def login_page():
    return render_template("login.html")


# NÃO coloque jwt_required aqui.
# O token está sendo usado nas APIs.
@app.route("/Inicial-page")
def inicial_page():
    return render_template("inicial.html")


@app.route("/config-page")
def config_page():
    return render_template("config.html")


@app.route("/recsenha-page")
def recsenha_page():
    return render_template("recsenha.html")


@app.route("/nvsenha-page")
def nvsenha_page():
    return render_template("nvsenha.html")


@app.route("/boasenha-page")
def boasenha_page():
    return render_template("boasenha.html")


if __name__ == "__main__":
    app.run(debug=True)