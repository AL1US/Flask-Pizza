from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizza.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.secret_key = 'f9c8307a7ec441477937cb35c6303b01c1f8b6b285bfa989c11bdc2eed2bd5b3' # Его так никогда нельзя хранить, всегда в других файлах
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Users(db.Model): 
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False) 
    email = db.Column(db.String(50), nullable=False, unique=True)    
    pswd = db.Column(db.Text(200), nullable=False)

    def __repr__(self): 
        return f'<Users id={self.id_user}>' 

class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name_pizza = db.Column(db.String(50), unique=True)
    img_pizza = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    pryce = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Pizza id={self.id}>'

# @app.before_request
# def get_id():
#     g.db = Users('user_id')

# Главная страница
@app.route("/")
def index():
    pizza = Pizza.query.all()
    return render_template("index.html", pizza=pizza)

# Выход
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return render_template("index.html")

# Создание пиццы
@app.route("/create-pizza", methods=['POST', 'GET'])
def create_pizza():
    if request.method =="POST":
        name_pizza = request.form['name_pizza']
        img_pizza = request.form['img_pizza']
        description = request.form['description']
        pryce = request.form['pryce']
        
        pizza = Pizza(name_pizza=name_pizza, img_pizza=img_pizza, description=description, pryce=pryce)
        
        try:
            db.session.add(pizza)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'Технические шоколадки {e}', 500
    else:
        return render_template("create-pizza.html")
    
# Редактирование пиццы
@app.route("/about-pizza/<int:id>/update", methods=['POST', 'GET'])
def update_pizza(id):
    pizza = Pizza.query.get(id)
    if request.method =="POST":
        pizza.name_pizza = request.form['name_pizza']
        pizza.img_pizza = request.form['img_pizza']
        pizza.description = request.form['description']
        pizza.pryce = request.form['pryce']
        
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f'Технические шоколадки {e}', 500
    else:
        return render_template("pizza_update.html", pizza=pizza)

# конкретная пицца 
@app.route("/about-pizza/<int:id>")
def post_detail(id):
    pizza = Pizza.query.get(id) 
    return render_template("about-pizza.html", pizza=pizza) 

# Удаление пиццы
@app.route("/about-pizza/<int:id>/delete")
def delete(id):
    pizza = Pizza.query.get_or_404(id) 
    
    try:
        db.session.delete(pizza)
        db.session.commit()
        return redirect("/")
    except:
        return "технические шоколадки"

# Регистрация
@app.route("/reg", methods=["GET", "POST"])
def reg():
    if "user_id" in session:
        return redirect(url_for("MyProfile", id=session["user_id"]))
    
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        pswd = bcrypt.generate_password_hash(request.form['pswd']).decode('utf-8')

        if Users.query.filter_by(email=email).first():
            return "Эта почта уже зарегестрирована", 400

        new_user = Users(username=username, email=email, pswd=pswd)

        try:
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id_user
            return redirect(url_for('MyProfile', id=new_user.id_user))
        except:
            return 'Ошибка при регистрации'

    return render_template("reg.html")
  
# Вход
@app.route("/sign", methods=["GET", "POST"])
def sign():
    if "user_id" in session:
        return redirect(url_for("MyProfile", id=session["user_id"]))
    
    if request.method == "POST":
        email = request.form["email"]
        pswd = request.form["pswd"]

        user = Users.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.pswd, pswd):
            session["user_id"] = user.id_user
            return redirect(url_for("MyProfile", id=user.id_user))  
        else:
            return "Неверный email или пароль", 401  

    return render_template("sign.html")


# Проверка на то в сессии ли юзер
@app.context_processor
def where_user():
    user_is_logged_in = False
    current_user = None
    
    if "user_id" in session:
        user_is_logged_in = True
        current_user = Users.query.get(session['user_id'])

    return dict(logged_in=user_is_logged_in, current_user=current_user)
  
# Корзина
@app.route("/Purchases")
def Purchases():
    return render_template("Purchases.html")
  
# Мой профиль
@app.route("/MyProfile/<int:id>")
def MyProfile(id):
    if "user_id" not in session or session["user_id"] != id:
        return redirect(url_for("sign"))

    user = Users.query.get(id)
    if user:
        return render_template("MyProfile.html", user=user)


# Если страница не найдена
@app.errorhandler(404)
def pageNotFount(error):
  return render_template('page404.html')


if __name__=="__main__":
    app.run(debug=True)