from flask import render_template
from App import app


@app.route("/")
def inicio():
    return render_template("profhorario.html")