
from fastapi import FastAPI,Request
from starlette.responses import HTMLResponse

# from fastapi import HTTPException,Path
# from typing import List, Dict, Any, Annotated
# from starlette import status
# from sqlalchemy.orm import Session
from database import engine, SessionLocal
from sqlalchemy import func
from fastapi.templating import Jinja2Templates
#Local imports
from models import Inventory
from fastapi.staticfiles import StaticFiles
# from seed.dummy import NAME_TO_ID
# from seed.dummy import PRODUCTS
# from schemas.product import ProductBuilder
# from schemas.product import ProductRequest
from routers import auth,Inventory_Management

app = FastAPI()
Inventory.base.metadata.create_all(bind=engine);

app.include_router(auth.router)
app.include_router(Inventory_Management.router)

templates=Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def test(request:Request):
    return templates.TemplateResponse(request, "home.html")

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close();
#
#
#
# """
# dependency injection instead of method establishing a conn, open and closing.
# we inject the sql conn. This make them loosely coupled. We can even
# have mock database to test things.
# Essence: Don't call us, we will call you.
# """
#
#
# # @app.get("/products")
# # async def get_products():
# #     return PRODUCTS
# db_dependency=Annotated[Session,Depends(get_db)]
# @app.get("/")
# async def get_products(db: db_dependency):
#     return db.query(Inventory.Products).all()
#
#
# # @app.get("/products/{product_name}",status_code=status.HTTP_200_OK)
# # async def get_product_info(product_name: str) -> Dict[str,Any]:
# #     try:
# #         product_id= NAME_TO_ID.get(product_name.casefold())
# #         return await get_product(product_id)
# #     except KeyError:
# #         raise HTTPException(status_code=404, detail="Product not found in Index")
# #     except Exception as e:
# #         raise HTTPException(status_code=404, detail=str(e))
#
# @app.get("/products/id/{product_id}",status_code=status.HTTP_200_OK)
# async def get_product(product_id: int, db: db_dependency):
#     try:
#         #always use first or all at the end of query.
#         data=db.query(Inventory.Products).filter(Inventory.Products.product_id == product_id).first()
#         if not data:
#             raise HTTPException(status_code=404, detail="Product not found")
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
# @app.get("/products/{product_name}",status_code=status.HTTP_200_OK)
# async def get_product_info(product_name: str,db:db_dependency):
#     try:
#         data=db.query(Inventory.Products).filter(
#                     func.lower((Inventory.Products.product_name))
#                                        == product_name.lower()).first()
#         if not data:
#             raise HTTPException(status_code=404, detail="Product not found")
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#
#
#
# # @app.get("/products/{product_id}")
# # async def get_product(product_id: int, status_code=status.HTTP_200_OK) -> Dict[str,Any]:
# #     return PRODUCTS.get(product_id)
#
#
#
# @app.get("/products/filter/{product_name}")
# async def get_product_by_pricerange(product_name: str,max_price:float, status_code=status.HTTP_200_OK) -> Dict[str,Any]:
#     for p in PRODUCTS.values():
#         if p.get("product_name").casefold() == product_name.casefold() and p.get("unit_price") <= max_price:
#             return p
#     raise HTTPException(status_code=404, detail="No Product within this range")
#
#
# # @app.post("/products/post/new")
# # async def new_product(payload=Body()):
# #     try:
# #         new_product= (Product.ProductBuilder()
# #              .set_name(payload.get("product_name"))
# #              .set_price(payload.get("unit_price"))
# #              .set_stock(payload.get("units_in_stock")).build())
# #         return {"message" : new_product}
# #
# #     except ValueError as e:
# #         raise HTTPException(status_code=400, detail=str(e))
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e)) #for generic server errors
#
# # @app.post("/products/post/new", status_code=status.HTTP_201_CREATED)
# # async def new_product(payload:ProductRequest) -> Dict[str,Any]:
# #     try:
# #         print("payload: ", payload)
# #         payload = payload.model_dump()
# #         new_product= (Product.ProductBuilder()
# #              .set_name(payload["product_name"])
# #              .set_price(payload["unit_price"])
# #              .set_stock(payload["units_in_stock"]).build())
# #         return {"message" : new_product}
# #
# #     except ValueError as e:
# #         raise HTTPException(status_code=400, detail=str(e))
# #     except Exception as e:
# #         raise HTTPException(status_code=500, detail=str(e)) #for generic server errors
#
# @app.post("/products/post/new", status_code=status.HTTP_201_CREATED)
# async def new_product(payload:ProductRequest,db:db_dependency):
#     # data= payload.model_dump()
#     new_product = (ProductBuilder()
#                    .set_name(payload.product_name)
#                    .set_price(payload.unit_price)
#                    .set_stock(payload.units_in_stock)
#                    .set_supplier(payload.supplier_id)
#                    .build())
#
#     db.add(new_product)
#     db.commit()
#     db.refresh(new_product)
#     return new_product
#
#
# @app.put("/products/{product_id}",status_code=status.HTTP_200_OK)
# async def update_product(product_id: int,payload:ProductRequest,db:db_dependency):
#     existing_product=db.query(Inventory.Products).filter(Inventory.Products.product_id == product_id).first()
#     if not existing_product:
#         raise HTTPException(status_code=404, detail="Product not found")
#
#
#     #Gets Category record, if there was an error, it will fail
#     category_id_to_set= get_categories(payload.category_id,db).category_id if payload.category_id else None
#     #Above None is passed into Builder func, nw it wont update.
#     #Similarly, for Supplier
#     supplier_id_to_set=get_suppliers(payload.supplier_id,db).supplier_id if payload.supplier_id else None
#
#
#     updated = (ProductBuilder(existing_product)
#                .set_name(payload.product_name)
#                .set_price(payload.unit_price)
#                .set_units_in_stock(payload.units_in_stock)
#                 .set_category_id(category_id_to_set)
#                 .set_supplier(supplier_id_to_set)
#
#                .build())
#     db.commit()
#     return updated
#
#
# def get_categories(category_id: int,db:db_dependency):
#     category = (db.query(Inventory.Categories).filter \
#                (Inventory.Categories.category_id == category_id).first())
#     if not category:
#         raise HTTPException(status_code=404, detail="Category not found")
#     return category
#
#
# def get_suppliers(supplier_id: int,db:db_dependency):
#     supplier=(db.query(Inventory.Suppliers).filter (Inventory.Suppliers.supplier_id == supplier_id).first())
#     if not supplier:
#         raise HTTPException(status_code=404, detail="Supplier not found")
#     return supplier
#
# @app.delete("/products/{product_id}",status_code=status.HTTP_200_OK)
# async def delete_product(db:db_dependency,product_id: int =Path(gt=0)):
#     deleted_product=db.query(Inventory.Products).filter(Inventory.Products.product_id == product_id).first()
#     if not deleted_product:
#         raise HTTPException(status_code=404, detail="Product not found")
#     product_name=deleted_product.product_name
#     db.delete(deleted_product)
#     db.commit()
#     return {"message":f" Successfully deleted product {product_name} "}
#
