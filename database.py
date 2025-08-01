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

product_details = ("flour",100,200)
insert_products(product_details)


def insert_sales(sales_details):
    query = f"insert into sales(pid,quantity)values{sales_details}"
    cur.execute(query)
    conn.commit()

new_sale = ("1",200)
insert_sales(new_sale)

   
def available_stock(pid):
    cur.execute("select sum(stock_quantity) from stock where pid = %s",(pid,))  
    total_stock = cur.fetchone()[0] or 0

    cur.execute("select sum(quantity) from sales where pid = %s",(pid,)) 
    total_sales = cur.fetchone()[0] or 0
    return total_stock - total_sales



def sales_per_product():
    cur.execute("""
        select products.name ,sum(products.selling_price * sales.quantity) as total_sales
        from products inner join sales on sales.pid = products.id group by products.name
    """)
    data = cur.fetchall()
    return data


def profit_per_product():
    cur.execute("""
        select products.name , sum((products.selling_price -products.buying_price) * sales.quantity)  as profit 
        from sales join products on sales.pid = products.id group by products.name;
    """)
    data = cur.fetchall()
    return data


def sales_per_day():
    cur.execute("""
        select sales.created_at as date, sum(products.selling_price * sales.quantity) as total_sales from 
        products inner join sales on sales.pid = products.id group by(date);
    """)
    data = cur.fetchall()
    return data


def profit_per_day():
    cur.execute("""
        select sales.created_at as date, sum((products.selling_price -products.buying_price) * sales.quantity) as profit
        from products inner join sales on sales.pid = products.id group by(date);
    """)
    data = cur.fetchall()
    return data


sales_per_p = sales_per_product()
print(sales_per_p)


profit_per_p = profit_per_product()
print(profit_per_p)













