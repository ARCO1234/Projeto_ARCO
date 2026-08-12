"""
Script de importação de usuários vindos de um banco/planilha pré-existente.

O que ele faz para cada pessoa:
  1. Gera uma senha aleatória e segura.
  2. Salva no banco só o HASH dessa senha (nunca a senha em texto puro).
  3. Marca `senha_temporaria = TRUE`, obrigando a pessoa a trocar no 1º login.
  4. Envia a senha inicial por e-mail (via Resend), sem exibi-la no terminal.

AJUSTE a função `buscar_usuarios_pre_existentes()` para ler do seu banco
antigo (pode ser outra conexão MySQL, um CSV, uma planilha exportada, etc).
Aqui deixei um exemplo lendo de uma lista Python só pra você ver o formato
esperado.
"""

import os
import secrets
import string
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from werkzeug.security import generate_password_hash
import resend

load_dotenv()

from App.database import conectar


def gerar_senha_aleatoria(tamanho=10):
    """Gera uma senha aleatória e segura (letras, números e alguns símbolos)."""
    alfabeto = string.ascii_letters + string.digits + "!@#$%"
    return "".join(secrets.choice(alfabeto) for _ in range(tamanho))


def buscar_usuarios_pre_existentes():
    """
    SUBSTITUA esse conteúdo pela leitura real do seu banco/planilha antiga.
    Precisa devolver uma lista de dicionários com essas chaves:
    cpf, tipo, matricula, nome, e_mail

    `tipo` precisa ser um dos valores do ENUM: 'gestor', 'profissional', 'equipe de apoio'
    """
    return [
        # Exemplo - troque pelos dados reais:
        # {
        #     "cpf": "333.333.333-33",
        #     "tipo": "profissional",
        #     "matricula": "33333333333333",
        #     "nome": "Carlos Professor",
        #     "e_mail": "carlos@escola.com",
        # },
    ]


def enviar_senha_por_email(nome, email, senha_temporaria):
    try:
        resend.api_key = os.getenv("RESEND_API_KEY")
        resend.Emails.send({
            "from": "ARCO <onboarding@resend.dev>",  # troque pelo domínio verificado
            "to": [email],
            "subject": "Seu acesso ao sistema ARCO",
            "html": f"""
                <p>Olá, {nome}!</p>
                <p>Sua conta no sistema ARCO foi criada. Use os dados abaixo para o primeiro acesso:</p>
                <p><strong>E-mail:</strong> {email}<br>
                <strong>Senha temporária:</strong> {senha_temporaria}</p>
                <p>Você vai precisar trocar essa senha assim que fizer login pela primeira vez.</p>
            """
        })
        return True
    except Exception as erro:
        print(f"  [!] Falha ao enviar e-mail para {email}: {erro}")
        return False


def importar():
    usuarios = buscar_usuarios_pre_existentes()

    if not usuarios:
        print("Nenhum usuário retornado por buscar_usuarios_pre_existentes(). "
              "Edite essa função com os dados reais antes de rodar de novo.")
        return

    conexao = conectar()
    cursor = conexao.cursor()

    total_ok = 0
    total_erro = 0

    for usuario in usuarios:
        senha_temp = gerar_senha_aleatoria()
        senha_hash = generate_password_hash(senha_temp)

        try:
            cursor.execute(
                """
                INSERT INTO usuario (CPF, Tipo, matricula, nome, senha, e_mail, senha_temporaria)
                VALUES (%s, %s, %s, %s, %s, %s, TRUE)
                """,
                (usuario["cpf"], usuario["tipo"], usuario["matricula"],
                 usuario["nome"], senha_hash, usuario["e_mail"])
            )
            conexao.commit()

            enviado = enviar_senha_por_email(usuario["nome"], usuario["e_mail"], senha_temp)

            if enviado:
                print(f"  [OK] {usuario['nome']} ({usuario['e_mail']}) - senha enviada por e-mail.")
            else:
                print(f"  [ERRO DE ENVIO] {usuario['nome']} - senha temporária não exibida.")

            total_ok += 1

        except Exception as erro:
            print(f"  [ERRO] {usuario['nome']} ({usuario['e_mail']}): {erro}")
            total_erro += 1

    cursor.close()
    conexao.close()

    print(f"\nImportação concluída: {total_ok} usuário(s) criado(s), {total_erro} erro(s).")


if __name__ == "__main__":
    importar()
