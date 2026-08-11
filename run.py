"""Ponto de entrada local do ARCO."""

import os

from App import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG") == "1")
