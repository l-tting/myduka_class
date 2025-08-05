from flask import Flask, render_template, request, redirect,url_for,flash,session
from database import fetch_products, fetch_sales,insert_products,insert_sales,available_stock,sales_per_product,profit_per_product,sales_per_day,profit_per_day,insert_user,check_user
from flask_bcrypt import Bcrypt
from functools  import wraps


#flask instance
app = Flask(__name__)

#bcrypt instance
bcrypt = Bcrypt(app)

app.secret_key = 'fjikmnej8dn3hdnd'


@app.route('/')
def home():
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def protected(*args,**kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args,**kwargs)
    return protected


@app.route('/products')
@login_required
def products():
    products = fetch_products()
    return render_template('products.html',products=products)



@app.route('/add_products',methods=['GET','POST'])
def add_products():
   product_name = request.form['product']
   buying_price = request.form['buying_price']
   selling_price = request.form['selling_price']
   new_product = (product_name,buying_price,selling_price)
   insert_products(new_product)
   flash("Product added succesfully","success")
   return redirect(url_for('products'))


@app.route('/sales')
@login_required
def sales():
    sales= fetch_sales()
    products = fetch_products()
    return render_template('sales.html',sales= sales,products=products)


@app.route('/make_sales',methods=['GET','POST'])
def add_sales():
    pid = request.form["pid"]
    quantity = request.form["quantity"]
    new_sale = (pid,quantity)
    check_stock = available_stock(pid)
    if check_stock < float(quantity): 
        flash("Stock not enough","error")
        return redirect(url_for('sales'))
    insert_sales(new_sale)
    return redirect(url_for('sales'))
    

@app.route('/stock')
@login_required
def stock():
    return render_template('stock.html')



@app.route('/dashboard')
@login_required
def dashboard():
    sales_product = sales_per_product()
    profit_product = profit_per_product()
    sales_day = sales_per_day()
    profit_day = profit_per_day()

    #product data
    product_names = [i[0] for i in sales_product]
    sales_per_p = [float(i[1]) for i in sales_product]
    profit_per_p = [float(i[1]) for i in  profit_product]

    #day data
    days = [str(i[0]) for i in sales_day]
    sales_per_d = [float(i[1]) for i in sales_day]
    profit_per_d = [float(i[1]) for i in profit_day]
    return render_template('dashboard.html',
            product_names= product_names,sales_per_p=sales_per_p,profit_per_p=profit_per_p,
            days = days,sales_per_d=sales_per_d,profit_per_d=profit_per_d      
                    )


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == "POST":
        full_name = request.form['full_name'] 
        email = request.form['email']
        phone_number = request.form['tel']
        password = request.form['password']

        existing_user = check_user(email)
        if not existing_user:
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            new_user = (full_name,email,phone_number,hashed_password)
            insert_user(new_user)
            flash("user registered successfully","success")
            return redirect(url_for('login'))
        else:
            flash("User already exists ,please login","danger")

    return render_template("register.html")



@app.route('/login',methods=["GET","POST"])
def login():
    if request.method =="POST":
        email = request.form['email']
        password = request.form["password"]

        existing_user = check_user(email)
        if not existing_user:
            flash("User does not exist ,please register","danger")
            return redirect(url_for("register"))
        else:
            if bcrypt.check_password_hash(existing_user[-1],password):
                flash("Logged in","success")
                session["email"] = email
                return redirect(url_for('dashboard'))
            else:
                flash("Password incorrect,try again","danger")
    return render_template("login.html")


app.run(debug=True)