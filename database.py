import psycopg2

#create a connection to the db
conn = psycopg2.connect(user="postgres",password='6979',host="localhost",port='5432',database='myduka2')

#cursor to execute db operations
cur = conn.cursor()

def fetch_products():
    cur.execute("select * from products")
    products = cur.fetchall()
    return products

products = fetch_products()


def insert_products():
    cur.execute("insert into products(name,buying_price,selling_price)values('eggs',15,20)")
    conn.commit()
 
insert_products()

print(products)


