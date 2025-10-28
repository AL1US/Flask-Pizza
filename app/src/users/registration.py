from flask import Blueprint, Flask, render_template, request, redirect, session
from src.web3_connect import contract
from src.routers.pizza import pizza_app
from web3.exceptions import ContractLogicError

reg_app = Blueprint("reg", __name__)
app = reg_app

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
    
    role = contract.functions.getRole().call({"from": session.get("address")})
    
    return render_template("profile.html", address=session.get("address"), role=role)

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