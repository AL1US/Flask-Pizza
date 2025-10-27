from flask import Flask, render_template, request, redirect, session
from src.routers import pizza
from src.web3_connect import contract
from src.routers.pizza import pizza_app

import json
from web3.exceptions import ContractLogicError

app = Flask(__name__)

app.register_blueprint(pizza_app)

app.secret_key = 'fa129c0e3c5bf9ed820cc0024697658ba5ab70331795c1fe21d7a5888be8'


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

@app.errorhandler(404)
def pageNotFount(error):
  return render_template('page404.html')

if __name__ == "__main__":
    app.run(debug=True)