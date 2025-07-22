from tkinter import *
from tkinter import ttk
from tkinter import font

from db import add_products, get_products, add_to_cart
from Cart import Cart, CartItem
from Product import Product



# root window
def create_root_window():
    root = Tk()
    root.title("MiniPOS")
    return root

# Content frame setup
def create_content_frame(root):
    content = ttk.Frame(root, padding=(3, 3, 12, 12))
    content.grid(column=0, row=0, sticky=(N, S, E, W))
    return content

# Left top frame setup
def create_left_top_frame(content):
    left_top_frame = ttk.Frame(content, borderwidth=5, relief="ridge", width=200, height=100)
    left_top_frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
    return left_top_frame

# Left bottom frame setup
def create_left_bottom_frame(content):
    left_bottom_frame = ttk.Frame(content, borderwidth=15, relief="ridge", width=200, height=100)
    left_bottom_frame.grid(column=0, row=2, columnspan=2, rowspan=1,sticky=(N, S, E, W) )
    return left_bottom_frame

# Right frame setup
def create_right_frame(content):
    right_frame = ttk.Frame(content, borderwidth=20, relief="ridge", width=100, height=100, padding="0 0 0 0")
    right_frame.grid(column=3, row=0, sticky=(N, S, E, W), rowspan=6, columnspan=3) 
    return right_frame 


def create_cart_label(left_top_frame, cart_image):
    highlightFont = font.Font(family='Helvetica', name='appHighlightFont', size=24, weight='bold')
    cart_label = ttk.Label(left_top_frame, text="Items in Cart", anchor='center', font=highlightFont)

    cart_label['image'] = cart_image
    cart_label['compound'] = 'right'
    cart_label.grid(column=0, row=0, rowspan=1, columnspan=3, sticky=(E, W))
    return cart_label

# Treeview setup
def create_treeview_withscroll(left_top_frame):

    treev = ttk.Treeview(left_top_frame, selectmode='browse')

    scroll = ttk.Scrollbar(left_top_frame, orient="vertical", command = treev.yview)

    treev.configure(yscrollcommand= scroll.set)

    scroll.grid(row=0, column=3, rowspan=3)
    treev['columns'] = ("Name", "Price", "Qty")
    treev['show'] = 'headings'

    treev.column("Name", anchor=W, width=10)
    treev.column("Price", anchor=CENTER, width=80)
    treev.column("Qty", anchor=CENTER, width=120)
    treev.heading("Name", text="Name", anchor=CENTER)
    treev.heading("Price", text="Price", anchor=CENTER)
    treev.heading("Qty", text="Qty", anchor=CENTER)
    # Inserting
    
    treev.grid(row=1, column=0, rowspan=1, columnspan=3, sticky=(E, W, S, N))
    return treev



def create_barcode_entry(right_frame, barcode):
    barcode_font = font.Font(family='Helvetica', name='appHighlightFont', size=24)
    barcode_entry = ttk.Entry(right_frame, textvariable=barcode, width=45, justify='center', font=barcode_font)
    barcode_entry.grid(row=0, column=0, columnspan=3, pady=(80, 0))
    return barcode_entry

def create_button(right_frame, callback, text):
    button = ttk.Button(right_frame, text=text, command=callback, width=20)
    return button

# Configure grid weights
def configure_grid_weights(root, content, left_top_frame, right_frame):
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    content.columnconfigure(0, weight=6)
    content.columnconfigure(1, weight=6)
    content.columnconfigure(2, weight=0)
    content.columnconfigure(3, weight=4)
    content.columnconfigure(4, weight=4)
    content.columnconfigure(5, weight=4)
    content.rowconfigure(1, weight=7)
    content.rowconfigure(2, weight=3)

    left_top_frame.columnconfigure(0, weight=1)
    left_top_frame.columnconfigure(1, weight=1)
    left_top_frame.columnconfigure(2, weight=1)
    left_top_frame.rowconfigure(0, weight=1)
    left_top_frame.rowconfigure(1, weight=9)

    right_frame.columnconfigure(0, weight=1)
    right_frame.columnconfigure(1, weight=1)
    right_frame.columnconfigure(2, weight=1)

    right_frame.rowconfigure(0, weight=0)
    right_frame.rowconfigure(1, weight=0)
    right_frame.rowconfigure(2, weight=0)
    right_frame.rowconfigure(3, weight=0)
    right_frame.rowconfigure(4, weight=0)
    right_frame.rowconfigure(5, weight=1)

def increase_quantity(tree, total_price_var):
    selected = tree.focus()  # Get the selected item's ID
    if not selected:
        return  # Nothing selected

    current_values = tree.item(selected, "values")  # Get current values tuple
    print(current_values)
    new_stock = int(current_values[2])  # Column 1 is index 1
    new_stock += 1  # Increase it

    # Replace the old values with updated quantity
    updated_values = (current_values[0], current_values[1], new_stock)  # update column 1
    tree.item(selected, values=updated_values)

    calculate_total(tree, total_price_var)

def decrement_quantity(treev, total_price_var):
    selected = treev.selection()
    if not selected:
        return  # nothing selected

    item_id = selected[0]
    values = treev.item(item_id, "values")

    name, price, stock = values
    stock = int(stock)

    if stock <= 1:
        treev.delete(item_id)
    else:
        new_values = (name, price, stock - 1)
        treev.item(item_id, values=new_values)

    calculate_total(treev, total_price_var)

def increment():
    print("You pressed increment!")

def calculate_total(tree, total_price_var):
    total = 0
    for item_id in tree.get_children():
        values = tree.item(item_id, "values")
        price = float(values[1])
        quantity = int(values[2])
        total += price * quantity
    total_price_var.set(f"{total:.2f}")


def add_item_to_cart(treev, barcode):
    product = add_to_cart(barcode.get())
    barcode.set("")
    treev.insert('', 'end', text='L1', values=(product.name, product.price, 1))
    print("Added A Product ", product)



# Main function to assemble the app
def init_screen():
    root = create_root_window()
    content = create_content_frame(root)

    cart_image = PhotoImage(file="shopping-cart.png").subsample(5, 5)
    
    total_price_var = StringVar()   


    # Create and configure frames
    left_top_frame = create_left_top_frame(content)
    left_bottom_frame = create_left_bottom_frame(content)
    right_frame = create_right_frame(content)

    # Create widgets inside frames
    create_cart_label(left_top_frame, cart_image)
    tree = create_treeview_withscroll(left_top_frame)

    barcode = StringVar()
    barcode_entry = create_barcode_entry(right_frame, barcode)
    increment_button = create_button(right_frame, lambda: increase_quantity(tree, total_price_var), "+")
    decrement_button = create_button(right_frame, lambda: decrement_quantity(tree, total_price_var), "-")
    increment_button.grid(row=1, column=1, sticky="", pady=(20, 0), padx=(20, 20))
    decrement_button.grid(row=2, column=1, sticky="")

    barcode_font = font.Font(family='Helvetica', name='appHighlightFont', size=24)
    total_label = ttk.Label(right_frame,text="Total", font=barcode_font)
    total_label.grid(row=3, column=1)

    calculate_total(tree, total_price_var)

    total_price = ttk.Label(right_frame, text="Total", font=barcode_font, textvariable=total_price_var)
    total_price.grid(row=4, column=1)
    
    # Configure grid weights
    configure_grid_weights(root, content, left_top_frame, right_frame)

    barcode_entry.focus()
    root.bind("<Return>", lambda event: add_item_to_cart(tree, barcode))
    root.mainloop()



