import random
import uuid
from typing import Optional

class Product:
    def __init__(self):
        # Generate a random ID (mimicking auto_increment)
        self.product_id = uuid.uuid4()
        self.product_name: str = ""
        self.supplier_id: Optional[int] = None
        self.category_id: Optional[int] = None
        self.quantity_per_unit: str = ""
        self.unit_price: float = 0.0
        self.units_in_stock: int = 0
        self.units_on_order: int = 0
        self.reorder_level: int = 0
        self.discontinued: int = 0

    def __str__(self):
        return f"{self.product_name+'by'+self.supplier_id+'@'+self.unit_price}"


    class ProductBuilder:
        def __init__(self):
            self.product = Product()

        def set_name(self, name: str):
            self.product.product_name = name
            return self # Allows for method chaining

        def set_supplier(self, supplier_id: int):
            self.product.supplier_id = supplier_id
            return self

        def set_price(self, price: float):
            self.product.unit_price = price
            return self


        def set_stock(self, stock: int):
            self.product.units_in_stock = stock
            return self

        def build(self):
            # better than is None Since it checks for Empty String as well.
            if not self.product.product_name:
                raise ValueError("Product name cannot be empty")

            if self.product.unit_price < 0:
                raise ValueError("Price cannot be negative")

            if self.product.units_in_stock < 0:
                raise ValueError("Stock cannot be negative")

            return self.product
