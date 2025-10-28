from src.web3_connect import contract
from flask import Blueprint, Flask, redirect, render_template, request, session
from web3.exceptions import ContractLogicError


pizza_app = Blueprint("pizza", __name__)
app = pizza_app

@app.route("/setPizza", methods = ["GET", "POST"])
def setPizza():
    if request.method == "POST":
        public_key = session.get("address")
        
        price_str = request.form.get("price")
        price_int = int(price_str)
        
        try:
            result = contract.functions.setPizza(
                request.form.get("img_pizza"),
                request.form.get("name_pizza"),
                request.form.get("description"),
                price_int
            ).transact({'from': public_key})
            
            return redirect("/")
        
        except ContractLogicError as e:
            return f"Ошибка: {e}"
        except Exception as e:   
            return f"Ошибка: {e}"
    
    return render_template("setPizza.html")