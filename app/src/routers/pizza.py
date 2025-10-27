from os import name
from src.web3_connect import contract
from flask import Blueprint, Flask, redirect, render_template, request, session

pizza_app = Blueprint("pizza", __name__)
app = pizza_app

@app.route("/setPizza", methods = ["GET, POST"])
def setPizza():
    if request.method == "POST":
        public_key = session.get("address")
        
        try:
            result = contract.functions.setPizza(
                request.form.get("name-pizza"),
                request.form.get("description"),
                request.form.get("price")
            )
        
    
    
    return render_template("setPizza.html")