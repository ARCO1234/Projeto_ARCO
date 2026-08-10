import resend
import os
from flask import Flask, jsonify
from dotenv import load_dotenv
load_dotenv()

resend.api_key = os.environ["RESEND_API_KEY"]

app = Flask(__name__)


@app.route("/")
def index():
    params: resend.Emails.SendParams = {
        "from": "Acme <onboarding@resend.dev>",
        "to": ["projeto.arco.01@gmail.com"],
        "subject": "hello world",
        "html": "<strong>it works!</strong>",
    }

    r = resend.Emails.send(params)
    return jsonify(r)

if __name__ == "__main__":
    app.run()