from flask import Flask, render_template, session
from src.routers_products.pizza import pizza_app
from src.routers_products.basket import basket_app
from src.web3_connect import contract

from src.users.role import role_app
from src.users.registration import reg_app

app = Flask(__name__)

app.secret_key = 'fa129c0e3c5bf9ed820cc0024697658ba5ab70331795c1fe21d7a5888be8'

app.register_blueprint(pizza_app)
app.register_blueprint(role_app)
app.register_blueprint(reg_app)
app.register_blueprint(basket_app)

@app.route("/")
def index():
  
  user_address = session.get("address")
  
  if user_address:
    pizza = contract.functions.getAllPizzas().call({"from": user_address})
  else:
    pizza = contract.functions.getAllPizzas().call()
  
  pizza_list = []
  
  for e in pizza:
    pizza_list.append({
      'id': e[0],
      "url_img": e[1],
      "name": e[2],
      "description": e[3],
      "price": e[4]
    })

  return render_template("index.html", pizza=pizza_list)

@app.errorhandler(404)
def pageNotFount(error):
  return render_template('page404.html')

@app.context_processor
def where_user():
    user_is_logged_in = False
    current_user = None
    
    if "address" in session:
        user_is_logged_in = True
        current_user = session["address"]
        
    return dict(logged_in=user_is_logged_in, current_user=current_user)

if __name__ == "__main__":
    app.run(debug=True)