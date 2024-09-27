from flask import render_template, request, session, redirect
from flask import current_app as app
from applications.database import db
from applications.models import User, Product, Category, Assets
import json, os
import datetime
import matplotlib
import matplotlib.pyplot as plt



@app.route("/")
def front():
    return render_template("front.html")

@app.route("/home",methods=["GET","POST"])
def home():
    if request.method == "GET":
        products=Product.query.all()
        categories=Category.query.all()
        if "user" in session:
            user=User.query.filter_by(name=session["user"]).first()
            return render_template("home.html", user= session["user"], signed=True, admin=user.admin,products=products,categories=categories)
        else:
            return render_template("home.html", user="None", signed=False, admin=False,products=products,categories=categories)
    
    elif request.method=="POST":
        product_id= request.form["product"]
        qty = request.form["qty"]
        product = Product.query.filter_by(id = product_id).first()
        
        cart = json.loads(session["cart"])
        if product_id in cart:
            current = int(qty) + int(cart[product_id])
            if current <= int(product.stock):
                cart[product_id] = str(int(cart[product_id]) + int(qty))
        else:
            current = int(qty)
            if current <= int(product.stock):
                cart[product_id] = qty

        session["cart"] = json.dumps(cart)

        print(session["cart"])
        return redirect("/home")
        
    
@app.route("/register",methods=["GET","POST"])
def register():
    if "user" in session:
        return redirect("/home")
    if request.method=="GET":
        return render_template ("register.html")
    elif request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        user= User(name=username , password=password)
        db.session.add(user)
        db.session.commit()
        session["user"] = username
        session["cart"] = json.dumps(dict())
        return redirect("/home")
    
@app.route("/login",methods=["GET","POST"])
def login():
    if "user" in session:
        return redirect("/home")
    if request.method=="GET":
        return render_template ("login.html")
    elif request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        user= User.query.filter_by(name=username).first()
        if not user:
            return redirect("/register")
        elif user and user.password!=password:
            return redirect("/login")
        session["user"] = username
        session["cart"] = json.dumps(dict())
        return redirect("/home")
    
@app.route("/logout")
def logout():
    if "user" in session:
        session.pop("user")
    return redirect("/home")

@app.route("/dashboard")
def dashboard():
    if "user" in session:
        user=User.query.filter_by(name=session["user"]).first()
        if user.admin:
            categories=Category.query.all()
            return render_template("dashboard.html",categories=categories)
    return redirect("/home")

@app.route("/category_add", methods = ["GET", "POST"])
def add_category():
    if "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        if user.admin:
            if request.method == "GET":
                return render_template("category_add.html")
            elif request.method=="POST":
                name = request.form["name"]
                description = request.form["description"]
                category=Category(name=name,description=description, owner=user.id)
                db.session.add(category)
                db.session.commit()
                return redirect("/dashboard")
        return redirect("/home")
    
@app.route("/category_edit/<id>", methods = ["GET", "POST"])
def category_edit(id):
    if "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        if user.admin:
            categories = Category.query.filter_by(id = id).first()
            if request.method == "GET":
                return render_template("category_edit.html", categories=categories)
            elif request.method == "POST":
                name = request.form.get("name",None)
                description = request.form.get("description", None)
                if name:
                    categories.name = name
                if description:
                    categories.description = description
                db.session.commit()
                return redirect("/dashboard")
    return redirect("/home")

@app.route("/category_delete/<id>")
def delete_category(id):
    if "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        if user.admin:
            category = Category.query.filter_by(id = id).first()
            products = Product.query.filter_by(cat_id=id).all()
            for product in products:
                os.remove("./static/products/"+str(product.id)+".png")
                db.session.delete(product)
            db.session.delete(category)
            db.session.commit()
            return redirect("/dashboard")
    return redirect("/home")
            
@app.route("/product_add/<cat_id>", methods = ["GET", "POST"])
def add_product(cat_id):
    if "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        if user.admin:
            if request.method == "GET":
                return render_template("product_add.html")
            elif request.method == "POST":
                name = request.form["name"]
                description = request.form["description"]
                availability = request.form["availability"]
                stock = request.form["stock"]
                m_r_p = request.form["m_r_p"]
                type = request.form["type"]
                mfg_date = request.form["mfg_date"]
                exp_date = request.form["exp_date"]
                img = request.files["img"]
                product = Product(name = name, description = description, availability=availability, type=type, stock = stock, 
                                  m_r_p=m_r_p, mfg_date=mfg_date,exp_date=exp_date,cat_id=cat_id, owner = user.id)
                db.session.add(product)
                db.session.commit()
                img.save("./static/products/" + str(product.id) + ".png")
                return redirect("/dashboard")
    return redirect("/home")

@app.route("/all_products/<cat_id>")
def all_products(cat_id):
    if "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        if user.admin:
            products=Product.query.filter_by(cat_id=cat_id).all()
            return render_template("all_products.html",products=products)
    else:
        return redirect("/dashboard")

@app.route("/product_delete/<product_id>")
def delete_product(product_id):
    if "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        if user.admin:
            product = Product.query.filter_by(id = product_id).first()
            os.remove("./static/products/"+str(product.id)+".png")
            db.session.delete(product)
            db.session.commit()
    return redirect("/home")

@app.route("/product_update/<product_id>", methods = ["GET", "POST"])
def product_update(product_id):
    if "user" in session:
        user = User.query.filter_by(name=session["user"]).first()
        if user.admin:
            product = Product.query.filter_by(id = product_id).first()
            if request.method == "GET":
                return render_template("product_update.html", product=product)
            elif request.method == "POST":
                name = request.form.get("name",None)
                description = request.form.get("description", None)
                availability = request.form.get("availability",None)
                stock = request.form.get("stock", None)
                img = request.files.get("img", None)
                m_r_p = request.form.get("m_r_p", None)
                mfg_date = request.form.get("mfg_date", None)
                exp_date = request.form.get("exp_date", None)
                type = request.form.get("type", None)
                if name:
                    product.name = name
                if description:
                    product.description = description
                if availability:
                    product.availability = availability
                if stock:
                    product.stock = stock
                if m_r_p:
                    product.m_r_p = m_r_p
                if mfg_date:
                    product.mfg_date = mfg_date
                if exp_date:
                    product.exp_date = exp_date
                if type:
                    product.type = type
                if img:
                    img.save("./static/products/" + str(product.id) + ".png")
                db.session.commit()
                return redirect("/dashboard")
    return redirect("/home")
  
@app.route("/cart", methods = ["GET", "POST"])
def cart():
    if "user" in session:
        cart = json.loads(session["cart"])
        user = User.query.filter_by(name=session["user"]).first()
        products = [[Product.query.filter_by(id = product_id).first(), cart[product_id]] for product_id in cart.keys()]
        total = sum([int(Product.query.filter_by(id = product_id).first().m_r_p) * int(cart[product_id]) for product_id in cart.keys()])
        if request.method == "GET":
            return render_template("cart.html", products = products, total = total)
        elif request.method=="POST":
            if "delete" in request.form:
                cart.pop(request.form["delete"])
                session["cart"] = json.dumps(cart)
                return redirect("/cart")
            else:
                for product, qty in products:
                    product.stock -= int(qty)
                    asset = Assets(product=product.id, owner=product.owner, customer=user.id, qty=qty)
                    db.session.add(asset)
                    db.session.commit()
                session["cart"] = json.dumps(dict())
                return redirect("/cart")
    return redirect("/home")

@app.route("/search_products/<cat_id>",methods=["GET","POST"])
def search_products(cat_id):   
    if request.method == "GET":
        products=Product.query.filter_by(cat_id=cat_id).all()
        if "user" in session:
            user=User.query.filter_by(name=session["user"]).first()
            return render_template("search_products.html", user= session["user"], signed=True, admin=user.admin,products=products)
        else:
            return render_template("search_products.html", user="None", signed=False, admin=False,products=products)
        
    elif request.method=="POST":
        product_id= request.form["product"]
        qty = request.form["qty"]
        product = Product.query.filter_by(id = product_id).first()
        
        cart = json.loads(session["cart"])
        if product_id in cart:
            current = int(qty) + int(cart[product_id])
            if current <= int(product.stock):
                cart[product_id] = str(int(cart[product_id]) + int(qty))
        else:
            current = int(qty)
            if current <= int(product.stock):
                cart[product_id] = qty

        session["cart"] = json.dumps(cart)

        print(session["cart"])
        return redirect("/home")
    
@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        searched_word = request.form['searched_word']
        products = Product.query.filter(Product.name.ilike(f'%{searched_word}%')).all()
        categories = Category.query.filter(Category.name.ilike(f'%{searched_word}%')).all()

        try:
            searched_m_r_p = float(searched_word)
            products += Product.query.filter(Product.m_r_p == searched_m_r_p).all()
        except ValueError:
            pass
        try:
            searched_mfg_date = str(searched_word)
            products += Product.query.filter(Product.mfg_date == searched_mfg_date).all()
        except ValueError:
            pass
        try:
            searched_exp_date = str(searched_word)
            products += Product.query.filter(Product.exp_date == searched_exp_date).all()
        except ValueError:
            pass
        
        if "user" in session:
            user=User.query.filter_by(name=session["user"]).first()
            return render_template("search.html", user= session["user"], signed=True, admin=user.admin,products=products,categories=categories)
        
        else:
            return render_template("search.html", user="None", signed=False, admin=False,products=products,categories=categories)

        
@app.route('/summary',methods=['GET','POST'])
def summary():
    products=Product.query.all()
    a1=[]
    b1=[]
    for pro in products:
        a1.append(pro.name)
        b1.append(pro.stock)
    plt.figure()
    plt.bar(a1,b1)
    plt.xlabel('Product_names')
    plt.ylabel('Stock of the products')
    plt.title('Bar Graph')
    plt.savefig('static/bar_graph.png')

    plt.clf()

    return render_template('summary.html', img='static/bar_graph.png')
   