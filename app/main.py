from flask import Flask, render_template, request, redirect, session
from src.web3_connect import contract
from src.routers.pizza import pizza_app

# from src.routers import pizza
from src.users.role import role_app
from src.users.registration import reg_app

import json
from web3.exceptions import ContractLogicError

app = Flask(__name__)

app.secret_key = 'fa129c0e3c5bf9ed820cc0024697658ba5ab70331795c1fe21d7a5888be8'

app.register_blueprint(pizza_app)
app.register_blueprint(role_app)
app.register_blueprint(reg_app)

@app.route("/")
def index():
    return render_template("index.html")

@app.errorhandler(404)
def pageNotFount(error):
  return render_template('page404.html')

if __name__ == "__main__":
    app.run(debug=True)