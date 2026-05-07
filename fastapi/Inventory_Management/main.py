
from fastapi import FastAPI, Depends
from fastapi import HTTPException
from typing import List, Dict, Any, Annotated
from starlette import status
from sqlalchemy.orm import Session
from database import engine, SessionLocal


#Local imports
from models import Inventory
from seed.dummy import NAME_TO_ID
from seed.dummy import PRODUCTS
from schemas.product import Product
from schemas.product import ProductRequest

Inventory.base.metadata.create_all(bind=engine);

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close();



"""
dependency injection instead of method establishing a conn, open and closing.
we inject the sql conn. This make them loosely coupled. We can even
have mock database to test things. 
Essence: Don't call us, we will call you.
"""


# @app.get("/products")
# async def get_products():
#     return PRODUCTS

@app.get("/")
async def get_products(db: Annotated[Session,Depends(get_db)]):
    return db.query(Inventory.Products).all()



@app.get("/products/{product_name}")
async def get_product_info(product_name: str,status_code=status.HTTP_200_OK) -> Dict[str,Any]:
    try:
        product_id= NAME_TO_ID.get(product_name.casefold())
        return await get_product(product_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Product not found in Index")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/products/{product_id}")
async def get_product(product_id: int, status_code=status.HTTP_200_OK) -> Dict[str,Any]:
    return PRODUCTS.get(product_id)

@app.get("/products/filter/{product_name}")
async def get_product_by_pricerange(product_name: str,max_price:float, status_code=status.HTTP_200_OK) -> Dict[str,Any]:
    for p in PRODUCTS.values():
        if p.get("product_name").casefold() == product_name.casefold() and p.get("unit_price") <= max_price:
            return p
    raise HTTPException(status_code=404, detail="No Product within this range")
    return {"message": "No product within the range"}


# @app.post("/products/post/new")
# async def new_product(payload=Body()):
#     try:
#         new_product= (Product.ProductBuilder()
#              .set_name(payload.get("product_name"))
#              .set_price(payload.get("unit_price"))
#              .set_stock(payload.get("units_in_stock")).build())
#         return {"message" : new_product}
#
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) #for generic server errors

@app.post("/products/post/new")
async def new_product(payload:ProductRequest, status_code=status.HTTP_201_CREATED) -> Dict[str,Any]:
    try:
        print("payload: ", payload)
        payload = payload.model_dump()
        new_product= (Product.ProductBuilder()
             .set_name(payload["product_name"])
             .set_price(payload["unit_price"])
             .set_stock(payload["units_in_stock"]).build())
        return {"message" : new_product}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) #for generic server errors


