import sqlite3
from tkinter import *
from tkinter import ttk

def fetch_and_display_products():
    # Clear previous content
    for widget in result_frame.winfo_children():
        widget.destroy()

    conn = sqlite3.connect("../data/products.db")
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

        for i, product in enumerate(products):
            product_label = Label(result_frame, text=str(product))
            product_label.grid(row=i, column=0, sticky="w")

    except sqlite3.Error as e:
        error_label = Label(result_frame, text=f"Error: {e}", fg="red")
        error_label.pack()

    conn.close()

# Basic GUI setup
root = Tk()
root.title("Product Viewer")

fetch_button = ttk.Button(root, text="Show Products", command=fetch_and_display_products)
fetch_button.pack(pady=10)

# Frame to hold results
result_frame = tk.Frame(root)
result_frame.pack(padx=10, pady=10)

root.mainloop()
