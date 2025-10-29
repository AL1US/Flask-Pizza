from statistics import quantiles
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

@app.route("/add_to_basket", methods = ["GET", "POST"])
def add_to_basket():
    pk = session.get("address")
    if request.method == "POST":
        try:
            result = contract.functions.setPizzaInBasket(
            int(request.form.get("_id")),
            int(request.form.get("_quanity"))
            ).transact({"from": pk})
            
            return redirect("/basket")
            
        except ContractLogicError as e:
                return f"Ошибка: {e}"
        except Exception as e:   
                return f"Ошибка: {e}"
    
    return render_template("add_to_basket.html")

@app.route("/del_product", methods = ["GET", "POST"])
def del_product():

    pk = session.get("address")

    if request.method == "POST":
        try:
            result = contract.functions.delPizza(
            int(request.form.get("_index"))
            ).transact({"from": pk})
            return redirect("/")

        except ContractLogicError as e:
                return f"Ошибка: {e}"
        except Exception as e:   
                return f"Ошибка: {e}"
    
    return render_template("del_product.html")