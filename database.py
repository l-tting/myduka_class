import psycopg2

#create a connection to the db
conn = psycopg2.connect(user="postgres",password='6979',host="localhost",port='5432',database='myduka2')

#cursor to execute db operations
cur = conn.cursor()

def fetch_products():
    cur.execute("select * from products")
    products = cur.fetchall()
    return products


def fetch_sales():
    cur.execute("select * from  sales")
    sales = cur.fetchall()
    return sales


def get_data(table):
    cur.execute(f"select * from {table}")
    data = cur.fetchall()
    return data


def insert_products(product_values):
    query= f"insert into products(name,buying_price,selling_price)values{product_values}"
    cur.execute(query)
    conn.commit()


def insert_sales(sales_details):
    query = f"insert into sales(pid,quantity)values{sales_details}"
    cur.execute(query)
    conn.commit()
















