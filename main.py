from flask import Flask, render_template
from database import fetch_products, fetch_sales

#flask instance
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/products')
def products():
    products = fetch_products()
    numbers = [1,2,3,4,5]
    return render_template('products.html',products=products, numbers = numbers)


@app.route('/sales')
def sales():
    sales= fetch_sales()
    return render_template('sales.html',sales=sales)

@app.route('/stock')
def stock():
    return render_template('stock.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


app.run(debug=True)