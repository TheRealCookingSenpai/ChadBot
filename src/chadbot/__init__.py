from flask import Flask, render_template, request, make_response
from chatdef import digest
import sys
import random

cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None

app = Flask(__name__)


@app.route("/")
def home():
    resp = make_response(render_template("home.html"))
    resp.set_cookie('chadbotcookie', str(random.randint(1, 9999999999)))
    return resp

@app.route("/get")
def get_bot_response():
    sessioncookie = request.cookies.get('chadbotcookie')
    userText = request.args.get('msg')
    response = digest(userText, sessioncookie)
    print(response)
    return response
if __name__ == "__main__":
    app.run()