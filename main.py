from flask import Flask, render_template, request, redirect,url_for
from database import fetch_products, fetch_sales,insert_products,insert_sales

#flask instance
app = Flask(__name__)


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
   return redirect(url_for('products'))



@app.route('/sales')
def sales():
    sales= fetch_sales()
    products = fetch_products()
    return render_template('sales.html',sales= sales,products=products)



@app.route('/add_sales',methods=['GET','POST'])
def add_sales():
    pid = request.form["pid"]
    quantity = request.form["quantity"]
    new_sale = (pid,quantity)
    insert_sales(new_sale)
    return redirect(url_for('sales'))
    


@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


app.run(debug=True)