from db import get_products, add_products
from Product import Product
from Cart import CartItem, Cart
from gui import init_screen
def main():
    # new_product_example = Product("shoe", 5, 55, 123456) 
    # add_products(new_product_example)
    
    print(get_products())

    newCart = Cart()
    for product in get_products():
        cart_item = CartItem(*product.get_all_attributes(), newCart)
        newCart.add_item(cart_item)


    print("printing cart items...")
    for item_in_cart in newCart.get_cart_items():
        print(item_in_cart)
    
    print(newCart)

    init_screen()









if __name__ == "__main__":
    main()