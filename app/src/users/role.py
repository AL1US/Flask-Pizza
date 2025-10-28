
from src.web3_connect import contract
from flask import Blueprint, Flask, redirect, render_template, request, session
from web3.exceptions import ContractLogicError

role_app = Blueprint("role", __name__)
app = role_app

@app.route("/setRole", methods = ["GET", "POST"])
def setRole():
    if request.method == "POST":
        public_key = session.get("address")
        
        try:
            result = contract.functions.setManager(
                request.form.get("address_user"),
            ).transact({'from': public_key})
            
            return redirect("/profile")
        
        except ContractLogicError as e:
            return f"Ошибка: {e}"
        except Exception as e:   
            return f"Ошибка: {e}"
    
    return render_template("setManager.html")
