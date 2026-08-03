from flask import Flask, render_template, jsonify, request
from database import conectar
from flask_cors import CORS
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()  # precisa vir antes do "import routes", para RESEND_API_KEY já estar disponível

import routes
from flask_jwt_extended import JWTManager, jwt_required


app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "senha-super-secreta"  # TODO: mover para variável de ambiente
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

jwt = JWTManager(app)

app.config['JSON_AS_ASCII'] = False

app.register_blueprint(routes.usuario_bp)
app.register_blueprint(routes.aluno_bp)
app.register_blueprint(routes.turma_bp)
app.register_blueprint(routes.relatorio_bp)
app.register_blueprint(routes.horario_bp)
app.register_blueprint(routes.pergunta_bp)
app.register_blueprint(routes.resposta_bp)
app.register_blueprint(routes.recuperacao_bp)


@app.route('/')
@jwt_required()
def index():
    conexao = conectar()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario")
    usuarios = cursor.fetchall()
    cursor.close()
    conexao.close()
    return jsonify(usuarios)


@app.route('/login-page')
def login_page():
    return render_template('login/login.html')


@app.route('/Inicial-page')
def inicial_page():
    return render_template('Inicial/inicial.html')


@app.route('/config-page')
def config_page():
    return render_template('config/config.html')


@app.route('/recsenha-page')
def recsenha_page():
    return render_template('recuperação_senha/recsenha.html')


@app.route('/nvsenha-page')
def nvsenha_page():
    return render_template('nova_senha/nvsenha.html')


@app.route('/boasenha-page')
def boasenha_page():
    return render_template('senha_recuperada/boasenha.html')


if __name__ == '__main__':
    app.run(debug=True)
