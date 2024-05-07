class Product:
    def __init__(self, product_index, product_name, price, manufacturer, remarks):
        self.product_index = product_index
        self.product_name = product_name
        self.price = price
        self.manufacturer = manufacturer
        self.remarks = tuple(remarks)
