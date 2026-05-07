from sqlalchemy.dialects.mysql import SMALLINT

from database import base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DECIMAL,SmallInteger

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

class Products(base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True, autoincrement=True,index=True,nullable=False)
    product_name = Column(String(50), nullable=False)

    #Lookup relationship, even though M:D is more suited.
    # To avoid Human error.
    supplier_id = Column(String ,nullable=True)
    category_id = Column(String, nullable=True)

    quantity_per_unit = Column(SmallInteger, nullable=False, default=0)
    unit_price = Column(DECIMAL(3, 2), nullable=True,default=0)#Float
    unit_in_stock = Column(SmallInteger, nullable=True,default=0)#its plural.
    unit_on_order = Column(SmallInteger, nullable=True,default=0)
    #even though there is default, null can be passed.
    reorder_level = Column(SmallInteger, nullable=True,default=0)
    discontinued = Column(SmallInteger, nullable=False, default=0)  # mandatory

class Suppliers(base):
    __tablename__ = "suppliers"
    supplier_id = Column(Integer, primary_key=True, autoincrement=True,index=True,nullable=False)
    company_name = Column(String(40), nullable=False)
    contact_name = Column(String(30), nullable=True)
    contact_title = Column(String(30), nullable=True)
    address = Column(String(60), nullable=True)
    city = Column(String(15), nullable=True)
    region = Column(String(15), nullable=True)
    postal_code = Column(String(10), nullable=True)
    country = Column(String(15), nullable=True)
    phone = Column(String(24), nullable=True)
    fax = Column(String(24), nullable=True)
    homepage = Column(String(50), nullable=True)


class Categories(base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True, autoincrement=True,index=True,nullable=False)
    category_name = Column(String(15), nullable=False)
    description = Column(String(50), nullable=True)
    picture=Column(String(50), nullable=True)