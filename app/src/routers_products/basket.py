from src.web3_connect import contract
from flask import Blueprint, Flask, redirect, render_template, request, session
from web3.exceptions import ContractLogicError

basket_app = Blueprint("basket", __name__)
app = basket_app

@app.route("/basket")
def basket():
    
    user_address = session.get("address")

    if user_address:
        pizza = contract.functions.getBasket().call({"from": user_address})
    else:
        pizza = contract.functions.getBasket().call()
  
    pizza_list = []
  
    for e in pizza:
        pizza_list.append({
        'id': e[0],
        "url_img": e[1],
        "name": e[2],
        "description": e[3],
        "price": e[4]
        })

    return render_template("basket.html", pizza=pizza_list)

@app.route("/buy_all_basket")
def buy_all_basket():
    pk = session.get("address")

    total_price = contract.functions.getBasketTotal(
        user = session.get("address")
        ).call({"from": pk})

    try:
        result = contract.functions.buyBasket().transact({"from": pk, "value": total_price})
                
        return redirect("/cheque")
            
    except ContractLogicError as e:
            return f"Ошибка: {e}"
    except Exception as e:   
            return f"Ошибка: {e}"
    

@app.route("/del_basket", methods = ["GET", "POST"])
def del_product():

    pk = session.get("address")

    if request.method == "POST":
        try:
            result = contract.functions.delProduct(
            int(request.form.get("_index"))
            ).transact({"from": pk})
            return redirect("/basket")

        except ContractLogicError as e:
                return f"Ошибка: {e}"
        except Exception as e:   
                return f"Ошибка: {e}"
    
    return render_template("del_basket.html")

@app.route("/cheque")
def cheque():
    
    pk = session.get("address")
    
    try:
        if "address" in session:
            cheque = contract.functions.getCheque().call({"from": pk})
        else:
            cheque = contract.functions.getCheque().call()
    
        cheque_list = []
  
        for array in cheque:
            for e in array:
                cheque_list.append({
                    'id': e[0],
                    "url_img": e[1],
                    "name": e[2],
                    "description": e[3],
                    "price": e[4]
                })

        
    except ContractLogicError as e:
        return f"Ошибка: {e}"
    except Exception as e:
        return f"Ошибка: {e}"
    
    return render_template("cheque.html", cheque = cheque_list)
