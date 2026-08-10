import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def conectar():
    try:
        conexao = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME", "Project"),
            autocommit=False
        )

        return conexao

    except mysql.connector.Error as erro:
        print(f"Erro ao conectar ao banco: {erro}")
        raise