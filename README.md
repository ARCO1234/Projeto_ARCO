# ARCO

Sistema escolar de Análise, Registro e Construção do Aluno, com frontend em
HTML/CSS/JavaScript e backend Flask/MySQL.

## Estrutura

```text
Projeto_ARCO/
├── App/
│   ├── __init__.py
│   ├── auth.py
│   ├── database.py
│   ├── extensions.py
│   ├── routes/
│   ├── static/
│   └── templates/
├── scripts/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── run.py
```

## Executar no Windows

Abra o PowerShell na pasta `Projeto_ARCO`:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Preencha o `.env` com os dados do MySQL, uma chave JWT segura e a chave do
serviço de e-mail. Para gerar a chave JWT:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

O valor `memory://` do limitador é adequado para desenvolvimento local. Em uma
implantação com mais de um processo, configure um armazenamento compartilhado.

Inicie o site:

```powershell
python run.py
```

Acesse `http://127.0.0.1:5000`.

## Testes

```powershell
python -m pytest -q
```

Os testes básicos não precisam de conexão com o banco. Login e consultas reais
dependem das tabelas já existentes no MySQL.

## Cuidados

- Nunca envie `.env` ou `.venv` para o Git.
- O frontend e as APIs são servidos pela mesma aplicação Flask.
- A redefinição de senha exige um token temporário obtido após validar o código.
- A análise comportamental deve apoiar decisões pedagógicas, sem diagnósticos ou
  punições automáticas.
