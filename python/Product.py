# Product class represents a product so I don't have to deal with a thousand arguments all the time
# I can just pass this


class Product():
    def __init__(self, name, price, stock, barcode, id=None):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.barcode = barcode
    
    def __repr__(self):
        return f"ID: {self.id} | Name: {self.name}| Price: {self.price} | Stock: {self.stock} | Barcode: {self.barcode}"
    
    def get_all_attributes(self):
        # ID is omitted we will not supply that
        return (self.name, self.price, self.stock, self.barcode,)

        