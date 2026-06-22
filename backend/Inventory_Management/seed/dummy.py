#key is product_id
#fields: name, category, price, Quantity, Stock
#category is category_id to prevent insertion anomaly and Data duplication
#extra fields:
"""
Field             | Type          | Null | Key | Default | Extra          |
+-------------------+---------------+------+-----+---------+----------------+
| product_id        | smallint      | NO   | PRI | NULL    | auto_increment |
| product_name      | varchar(40)   | NO   |     | NULL    |                |
| supplier_id       | smallint      | YES  | MUL | NULL    |                |
| category_id       | smallint      | YES  | MUL | NULL    |                |
| quantity_per_unit | varchar(20)   | YES  |     | NULL    |                |
| unit_price        | decimal(10,2) | YES  |     | NULL    |                |
| units_in_stock    | smallint      | YES  |     | NULL    |                |
| units_on_order    | smallint      | YES  |     | NULL    |                |
| reorder_level     | smallint      | YES  |     | NULL    |                |
| discontinued      | tinyint(1)    | NO   |     | 0       |                |
"""
# Initial seed data following your SQL schema
# I used dictionary for O(1) retrieval.
PRODUCTS = {
    1: {
        "product_name": "Wireless Mouse",
        "supplier_id": 101,
        "category_id": 5,
        "quantity_per_unit": "1 piece",
        "unit_price": 25.99,
        "units_in_stock": 150,
        "units_on_order": 0,
        "reorder_level": 20,
        "discontinued": 0
    },
    2: {
        "product_name": "Mechanical Keyboard",
        "supplier_id": 101,
        "category_id": 5,
        "quantity_per_unit": "1 piece",
        "unit_price": 89.50,
        "units_in_stock": 45,
        "units_on_order": 20,
        "reorder_level": 10,
        "discontinued": 0
    },
    3: {
        "product_name": "Legacy USB Hub",
        "supplier_id": 105,
        "category_id": 2,
        "quantity_per_unit": "1 piece",
        "unit_price": 15.00,
        "units_in_stock": 0,
        "units_on_order": 0,
        "reorder_level": 5,
        "discontinued": 1
    }
}

# Secondary Index (The "Shortcut")
NAME_TO_ID = {
    "wireless mouse": 1,
    "mechanical keyboard": 2,
    "legacy usb hub": 3
}
