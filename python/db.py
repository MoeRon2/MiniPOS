# This file handles all db interactions for our program
# Connecting, getting data, sending data etc.

import sqlite3
from Product import Product
from Cart import CartItem


# Makes a connection to the sqlite database
# returns the connection and cursor
def get_connection():
    con = sqlite3.connect("../data/products.db")
    return con


def add_products(product):
    # get all attributes, gets everything in a tuple format so we don't have to write product.name, product.price everywhere If we are looking to use everything
    product_data = product.get_all_attributes()
    with get_connection() as con:
        cur = con.cursor()
        cur.execute("""INSERT INTO products (name, price, stock, barcode) VALUES (?, ?, ?, ?)""", product_data)
        con.commit()

def get_item(barcode, cart):
    with get_connection() as con:
        cur = con.cursor()
        res = cur.execute("""SELECT name, price, stock, barcode FROM products WHERE barcode = ?""", (barcode,))
        attributes = res.fetchone()
        print(attributes)
        product = CartItem(*attributes, cart)
        print(product)
        return product



#  getting column names
# column_names = [description[0] for description in cur.description]
# print("Column names:", column_names) 
# # For example here: Column names: ['id', 'name', 'price', 'stock', 'barcode']

def get_products():
    with get_connection() as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        res = cur.execute("""SELECT * FROM products""")
         # Convert rows into Product objects
        products = [Product(row["name"], row["price"], row["stock"], row["barcode"], row["id"]) for row in res]
        
        return products

