from Product import Product

class Cart():
    def __init__(self):
        self.total_price = 0
        self.cart = []

    def add_item(self, cart_item):
        for item in self.cart:
            if item == cart_item:
                item.increment_quantity()
                self.total_price += item.price  # just add the price of 1 item
                return
        self.cart.append(cart_item)
        self.total_price += cart_item.price

    def remove_item(self, cart_item):
        for item in self.cart:
            if item == cart_item:
                item.decrement_quantity()
                self.total_price -= item.price
                if item.quantity == 0:
                    self.cart.remove(item)
                return

    
    def get_cart_items(self):
        return self.cart
    
    def get_total_price(self):
        return str(self.total_price) + "$"
    

    def __repr__(self):
        return f"Total is {self.total_price} and cart items are: {self.cart}"
    
    def get_barcodes(self):
        barcodes = []
        for item in self.cart:
            barcodes.append(item.barcode)
        return barcodes

    def __iter__(self):
        return iter(self.cart)
    
    def find_item(self, cart_item_name : str):
        for item in self.cart:
            if item.name == cart_item_name:
                return item
        return None
    

    
        


class CartItem(Product):
    def __init__(self, name, price, stock, barcode, cart, quantity=1, id=None,):
        super().__init__(name, price, stock, barcode, id)
        self.price = price
        self.cart = cart
        self.quantity = quantity
            

        

    def __repr__(self):
        return f"Name: {self.name} , Barcode: {self.barcode} , Quantity: {self.quantity}, Price: {self.price}"
    
    
    def increment_quantity(self):
        self.quantity += 1

    def decrement_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
        else:
            self.quantity = 0
    def __eq__(self, other):
        return self.name == other.name and self.barcode == other.barcode
    
