import mysql.connector

def conectar():
    conexao = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Hn*18062007",
        database="Project"
    )
    return conexao

# .\venv\Scripts\activate