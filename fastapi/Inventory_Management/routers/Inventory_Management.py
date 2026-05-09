from email import message

from fastapi import Depends, APIRouter
from fastapi import HTTPException,Path
from typing import List, Dict, Any, Annotated

from jose import JWTError
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy import func

#Local imports
from models import Inventory
#from seed.dummy import NAME_TO_ID
from seed.dummy import PRODUCTS
from schemas.product import ProductBuilder
from schemas.product import ProductRequest
from routers.auth import get_curr_user


# router.include_router(auth.router)
# Inventory.base.metadata.create_all(bind=engine);
router = APIRouter(
    prefix="/inventory",
    tags=["inventory"]
)



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


# @router.get("/products")
# async def get_products():
#     return PRODUCTS
db_dependency=Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_curr_user)]


@router.get("/products")
async def get_products(user:user_dependency,db: db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return db.query(Inventory.Products).all()


# @router.get("/products/{product_name}",status_code=status.HTTP_200_OK)
# async def get_product_info(product_name: str) -> Dict[str,Any]:
#     try:
#         product_id= NAME_TO_ID.get(product_name.casefold())
#         return await get_product(product_id)
#     except KeyError:
#         raise HTTPException(status_code=404, detail="Product not found in Index")
#     except Exception as e:
#         raise HTTPException(status_code=404, detail=str(e))

@router.get("/products/id/{product_id}",status_code=status.HTTP_200_OK)
async def get_product(user:user_dependency, db: db_dependency,product_id: int):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    try:
        #always use first or all at the end of query.
        data=db.query(Inventory.Products).filter(Inventory.Products.product_id == product_id).first()
        if not data:
            raise HTTPException(status_code=404, detail="Product not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{product_name}",status_code=status.HTTP_200_OK)
async def get_product_info(user:user_dependency,product_name: str,db:db_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    try:
        data=db.query(Inventory.Products).filter(
                    func.lower((Inventory.Products.product_name))
                                       == product_name.lower()).first()
        if not data:
            raise HTTPException(status_code=404, detail="Product not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# @router.get("/products/{product_id}")
# async def get_product(product_id: int, status_code=status.HTTP_200_OK) -> Dict[str,Any]:
#     return PRODUCTS.get(product_id)



@router.get("/products/filter/{product_name}")
async def get_product_by_pricerange(product_name: str,max_price:float, status_code=status.HTTP_200_OK) -> Dict[str,Any]:
    for p in PRODUCTS.values():
        if p.get("product_name").casefold() == product_name.casefold() and p.get("unit_price") <= max_price:
            return p
    raise HTTPException(status_code=404, detail="No Product within this range")


# @router.post("/products/post/new")
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

# @router.post("/products/post/new", status_code=status.HTTP_201_CREATED)
# async def new_product(payload:ProductRequest) -> Dict[str,Any]:
#     try:
#         print("payload: ", payload)
#         payload = payload.model_dump()
#         new_product= (Product.ProductBuilder()
#              .set_name(payload["product_name"])
#              .set_price(payload["unit_price"])
#              .set_stock(payload["units_in_stock"]).build())
#         return {"message" : new_product}
#
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e)) #for generic server errors

@router.post("/products/new", status_code=status.HTTP_201_CREATED)
async def new_product(user:user_dependency,payload:ProductRequest,db:db_dependency):
    # data= payload.model_dump()
    #if not user -> returns true when its an empty list or string or None.
    #if not user vs if user is None
    #latter is just a referrence check  since None is singleton
    #former also check for empty ds or None.
    #since i am returning a dict, i would use if not user
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    #Validates FK relationship
    category_id_to_set,supplier_id_to_set,_=_validate_FK(db,payload.category_id,payload.supplier_id)


    new_product = (ProductBuilder()
                   .set_name(payload.product_name)
                   .set_price(payload.unit_price)
                   .set_stock(payload.units_in_stock)
                    .set_category_id(category_id_to_set)
                   .set_supplier(supplier_id_to_set)\
                    .set_owner_id(user["id"])
                   .build())
    try:
        db.add(new_product)
        db.commit()
        db.refresh(new_product)
        print("Use js to show a toast message")
        return new_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str("internal server error.."))



#Finder's Keeper
#Any loose product from data.sql that has no owner.
#After edit operation that record becomes the user
#who perfrom that operation on the record.
def get_categories(category_id: int,db:db_dependency):
    category = (db.query(Inventory.Categories).filter \
               (Inventory.Categories.category_id == category_id).first())
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/products/{product_id}",status_code=status.HTTP_200_OK)
async def update_product(user:user_dependency,product_id: int,payload:ProductRequest,db:db_dependency):
    #Credentials first
    if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")

    #Verify a product exist
    existing_product = db.query(Inventory.Products).filter(Inventory.Products.product_id == product_id).first()
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Blocks editing if the product has an owner. Allows edit if its the same owner.
    if (existing_product.owner_id is not None and existing_product.owner_id != user["id"]):
        #403 is for found resource but u can't update it.
        owner_username=db.query(Inventory.User).filter(Inventory.User.user_id == existing_product.owner_id).first().username
        raise HTTPException(status_code=403, detail=f"Product can only be updated by {owner_username}")

    #I skip the 3rd arg below cuz if the product doesnt exist why bother
    #Verify Categories are correct
    category_id_to_set, supplier_id_to_set, _ = _validate_FK(db, payload.category_id, payload.supplier_id)


    if category_id_to_set is None or supplier_id_to_set is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The provided Category or Supplier ID does not exist."
        )


    #Gets Category record, if there was an error, it will fail
    # category_id_to_set= get_categories(payload.category_id,db).category_id if payload.category_id else None
    #Above None is passed into Builder func, nw it wont update.
    #Similarly, for Supplier
    # supplier_id_to_set=get_suppliers(payload.supplier_id,db).supplier_id if payload.supplier_id else None


    updated = (ProductBuilder(existing_product)
               .set_name(payload.product_name)
               .set_price(payload.unit_price)
               .set_units_in_stock(payload.units_in_stock)
                .set_category_id(category_id_to_set)
                .set_supplier(supplier_id_to_set)
                .set_owner_id(user["id"])
               .build())
    try:
        db.commit()
        db.refresh(updated)
        return updated
    except Exception as e:
        db.rollback()
        #str(e) can leak table info.
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str("Internal Server Error.."))

def _validate_FK(db:db_dependency,category_id,supplier_id=None,product_id=None):

    if(product_id is not None):
        product_id = db.query(Inventory.Products).filter(Inventory.Products.product_id == product_id).first()
    # Gets Category record, if there was an error, it will fail
    if(category_id is not None):
        category_id = get_categories(category_id, db).category_id if category_id else None
    # Above None is passed into Builder func, nw it wont update.
    # Similarly, for Supplier
    if(supplier_id is not None):
        supplier_id = get_suppliers(supplier_id, db).supplier_id if supplier_id else None
    return category_id, supplier_id,product_id






def get_suppliers(supplier_id: int,db:db_dependency):
    supplier=(db.query(Inventory.Suppliers).filter (Inventory.Suppliers.supplier_id == supplier_id).first())
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier

@router.delete("/products/{product_id}",status_code=status.HTTP_200_OK)
async def delete_product(user:user_dependency,db:db_dependency,product_id: int =Path(gt=0)):
    if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")


    deleted_product=db.query(Inventory.Products).filter(Inventory.Products.product_id == product_id).first()
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if (deleted_product.owner_id is not None and deleted_product.owner_id != user["id"]):
        #403 is for found resource but u can't update it.
        owner_username=db.query(Inventory.User).filter(Inventory.User.user_id == deleted_product.owner_id).first().username
        raise HTTPException(status_code=403, detail=f"Product can only be updated by {owner_username}")

    product_name=deleted_product.product_name
    db.delete(deleted_product)
    db.commit()
    return {"message":f" Successfully deleted product {product_name} "}









