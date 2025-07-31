from flask import Flask, render_template, request, redirect,url_for,flash
from database import fetch_products, fetch_sales,insert_products,insert_sales,available_stock,sales_per_product,profit_per_product,sales_per_day,profit_per_day

#flask instance
app = Flask(__name__)

app.secret_key = 'fjikmnej8dn3hdnd'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/products')
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
def sales():
    sales= fetch_sales()
    products = fetch_products()
    return render_template('sales.html',sales= sales,products=products)



@app.route('/make_sales',methods=['GET','POST'])
def add_sales():
    pid = request.form["pid"]
    quantity = request.form["quantity"]
    new_sale = (pid,quantity)
    check_stock = available_stock()
    if check_stock < quantity:
        print("Stock not available")
    insert_sales(new_sale)
    return redirect(url_for('sales'))
    

@app.route('/stock')
def stock():
    return render_template('stock.html')



@app.route('/dashboard')
def dashboard():
    sales_product = sales_per_product()
    profit_product = profit_per_product()
    sales_day = sales_per_day()
    profit_day = profit_per_day()
    return render_template('dashboard.html')


app.run(debug=True)