from statistics import quantiles
from src.web3_connect import contract
from flask import Blueprint, Flask, redirect, render_template, request, session
from web3.exceptions import ContractLogicError

basket_app = Blueprint("basket", __name__)
app = basket_app

@app.route("/basket")
def basket():
  pizza = contract.functions.getBasket().call({"from": session.get("address")})
  
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
