from flask import Flask, render_template, request, redirect, session
from web3 import Web3
from web3.exceptions import ContractLogicError

import json

app = Flask(__name__)
app.secret_key = 'fa129c0e3c5bf9ed820cc0024697658ba5ab70331795c1fe21d7a5888be8'

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

if not w3.is_connected():
    print("not connected")
    
with open("../blockchain/artifacts/contracts/contract.sol/Contract.json") as f:
    config = json.load(f)

contract = w3.eth.contract(
    address=config["address"],
    abi=config["abi"]
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/reg", methods=['GET', 'POST'])
def reg():
    
    if request.method == "POST":
        public_key = request.form.get("_login")

        try:
            result = contract.functions.setReg(
                request.form.get("_login"),
                request.form.get("_password")
            ).transact({"from": public_key})
            
            session["address"] = public_key
            
        except ContractLogicError as e:
            return f"ошибка {e}"
        
        except Exception as e:
            return f"Ошибка {e}"
        return redirect("/profile")
    return render_template("reg.html")

@app.route("/profile")
def profile():
    
    if not session.get("address"):
        return redirect("/reg")

    return render_template("profile.html", address=session.get("address"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.context_processor
def where_user():
    user_is_logged_in = False
    current_user = None
    
    if "address" in session:
        user_is_logged_in = True
        
    return dict(logged_in=user_is_logged_in, current_user=current_user)

if __name__ == "__main__":
    app.run(debug=True)