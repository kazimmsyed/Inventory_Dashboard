from email import message

from fastapi import Depends, APIRouter
from fastapi import HTTPException,Path,Request
from typing import List, Dict, Any, Annotated

from jose import JWTError
from sqlalchemy.ext.asyncio import result
from starlette import status
from sqlalchemy.orm import Session
from database import SessionLocal
from sqlalchemy import func,select

#Local imports
from models import Inventory
from models.Inventory import Products
#from seed.dummy import NAME_TO_ID
from seed.dummy import PRODUCTS
from schemas.product import ProductBuilder
from schemas.product import ProductRequest
from schemas.filter_strategy import FilterRequest,STRATEGIES,ALLOWED_FIELDS
from routers.auth import get_curr_user
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates/")


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

def redirect_to_login():
    redirect_response=RedirectResponse(url="/auth/login",status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key="access_token")
    return redirect_response

### Pages ###

@router.get("/products")
async def get_products(request:Request,db: db_dependency,page: int,size: int):
    #user: user_dependency
    try:
        result_psc = await fetch_inventory_data(db,page,size);
        # 2. Manually format into a list of dicts for JSON serialization
        formatted_data = []
        for product, supplier, category in result_psc:
            formatted_data.append({
                "product": product.product_id,
                "product_name": product.product_name,
                "units_in_stock": product.unit_in_stock,
                "unit_price": product.unit_price,
                "unit_on_order": product.unit_on_order,
                "supplier_name": supplier.company_name,
                "category_name": category.category_name,
                "supplier_id": supplier.supplier_id,
                "category_id": category.category_id,
                "product_id": product.product_id
            })

        return {"data": formatted_data}
    except Exception as e:
        return {"message":str(e)}


@router.get('/products/html')
async def render_products_all(request:Request,db:db_dependency,page: int = 1, size: int = 10):
    try:
        offset_num = (page - 1) * size
        helper_fields={"page":page,"size":size}

        user=await get_curr_user(request.cookies.get("access_token") )

        if user is None:
            return redirect_to_login()

        result_psc = await fetch_inventory_data(db,page,size)
        print("result_psc",result_psc)
        total = db.query(func.count(Inventory.Products.product_id)).scalar()
        helper_fields["total_pages"] = total/size
        return templates.TemplateResponse(request, "products.html", {"result_psc": result_psc, "user": user,
                                                                     "helper_fields": helper_fields})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))




@router.get('/products/home')
async def render_products_all(request:Request,db:db_dependency,page: int = 1, size: int = 10):
    try:
        offset_num = (page - 1) * size
        helper_fields={"page":page,"size":size}

        user=await get_curr_user(request.cookies.get("access_token") )

        if user is None:
            return redirect_to_login()

        result_psc = await fetch_inventory_data(db,page,size)
        print("result_psc",result_psc)
        total = db.query(func.count(Inventory.Products.product_id)).scalar()
        helper_fields["total_pages"] = total/size
        return templates.TemplateResponse("filter_home.html",{"request":request,"result_psc":result_psc,"user":user,\
                                                           "helper_fields":helper_fields})
    except Exception as e:
        print(str(e))
        print("------- from products/home")
        redirect_to_login()
        #raise HTTPException(status_code=404, detail=str(e))


@router.get('/categories')
async def getCategories(
        db:db_dependency
    ):
    try:
        rows=(db.query(
            Inventory.Categories.category_id,
            Inventory.Categories.category_name,
            Inventory.Categories.description
            )
            .all()
              )
        data=[{"category_id":e.category_id,"category_name":e.category_name,"description":e.description} for e in rows]
        return data

    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))


@router.get('/products/{id}')
async def getProductDetails(
        db:db_dependency,
        id : int=Path(gt=0)
):
    e= db.query(Inventory.Products).filter(Inventory.Products.product_id == id).first()
    print(e)
    if(e is None):
        return {"message":"Product not found"}
    result= {"product_name":e.product_name,
              "category_id": e.category_id,
              "product_id": e.product_id,
              "unit_price": e.unit_price,
              "unit_on_order": e.unit_on_order,
              "discontinued": e.discontinued,
              "owner_id": e.owner_id,
              "quantity_per_unit": e.quantity_per_unit,
              "supplier_id": e.supplier_id,
              "unit_in_stock": e.unit_in_stock,
              "reorder_level": e.reorder_level
              }

    print("result",result);
    return result;








@router.get('/category/{category_id}/products')
async def getProductBasedOnCategory(
    db:db_dependency,
    category_id: int = Path(gt=0),
    page: int =1 ,
    size: int = 10):

    try:
        offset_num = (page - 1) * size
        helper_fields = {"page": page, "size": size}
        row=(db.query(
                    Inventory.Products.product_name,
                    Inventory.Products.product_id
                    )
                    .filter(Inventory.Products.category_id == category_id)
                    .offset(offset_num)
                    .limit(size)
                    .all()
        )
        result= [ {"product_name": row.product_name, "product_id": row.product_id} for row in row]
        total = (
            db.query(func.count(Inventory.Products.product_id))
            .filter(Inventory.Products.category_id == category_id)
            .scalar()
        )
        helper_fields["records_count"] = total;
        helper_fields["total_pages"] = max(1, (total + size - 1) // size)
        return {
            "helper_fields": helper_fields,
            "data": result,  # same shape as /products if you want consistency
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



#post because we are doing a get but we
# Sending the data in payload.
@router.post("/products/filter")
async def filter_products(
    payload: FilterRequest,
    db: db_dependency
):
    print(payload)
    query = select(Inventory.Products)

    for filter_item in payload.filters:

        # Validate field
        if filter_item.field not in ALLOWED_FIELDS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid field: {filter_item.field}"
            )

        # Validate operator
        if filter_item.operator not in STRATEGIES:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid operator: {filter_item.operator}"
            )

        column = ALLOWED_FIELDS[filter_item.field]

        strategy = STRATEGIES[filter_item.operator]

        query = strategy.apply(
            query=query,
            column=column,
            value=filter_item.value
        )


    #Query has been build.

    result =  db.execute(query)

    products = result.scalars().all()# scalar gives count and scalars() gives records

    return {
        "count": len(products),
        "results": products
    }





@router.get("/products/id/{product_id}/html",status_code=status.HTTP_200_OK)
async def get_product(request:Request, db: db_dependency,product_id: int=Path(gt=0)):
    try:
        user = await get_curr_user(request.cookies.get("access_token"))
        if not user:
            #raise HTTPException(status_code=401, detail="Authentication Failed")
            return redirect_to_login()
        product=db.query(Inventory.Products).filter(Inventory.Products.product_id == product_id).first()
        category = db.query(Inventory.Categories.category_id, Inventory.Categories.category_name).all()
        supplier = (db.query(Inventory.Suppliers.supplier_id, Inventory.Suppliers.company_name)\
                    .join(Inventory.Products,Inventory.Products.supplier_id == Inventory.Suppliers.supplier_id)\
                    .filter(Inventory.Products.product_id == product_id)\
                    .first())
        print("supplier",supplier)



        return templates.TemplateResponse(request, "product_detail.html",
                                          {"product": product, "category": category, "supplier": supplier, "user": user})
    except Exception as e:
        # return {"message":str(e)}
        return redirect_to_login()




### ENDPOINTS ###

async def fetch_inventory_data(db:Session,page:int,size:int=10):
    page = max(1, page)
    offset_num = (page - 1) * size
    result_psc = db.query(Inventory.Products, Inventory.Suppliers, Inventory.Categories) \
        .join(Inventory.Categories, \
              Inventory.Products.category_id == Inventory.Categories.category_id) \
        .join(Inventory.Suppliers, \
              Inventory.Products.supplier_id == Inventory.Suppliers.supplier_id) \
        .offset(offset_num).limit(size).all()
    return result_psc




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
async def get_product(user:user_dependency, db: db_dependency,product_id: int=Path(gt=0)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    try:
        #always use first or all at the end of query.
        print("couldn't find it")
        data=db.query(Inventory.Products).filter(Inventory.Products.product_id == product_id).first()
        if not data:
            raise HTTPException(status_code=404, detail="Product not found")
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/{product_name}",status_code=status.HTTP_200_OK)
async def get_product_info(user:user_dependency,db:db_dependency,product_name: str=Path(min_length=2)):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    try:
        print("couldn't find it")
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



@router.get("/products/search/{product_name}")
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
@router.get('/supplier/{id}',status_code=status.HTTP_200_OK)
async def get_supplier_details(user:user_dependency,db:db_dependency,id: int=Path(gt=0)):
        supplier_info =db.query(Inventory.Suppliers).filter(Inventory.Suppliers.supplier_id == id).first();

        return supplier_info;

@router.get('/category/{category_id}',status_code=status.HTTP_200_OK)
async def get_category_details(user:user_dependency,db:db_dependency,category_id: int=Path(gt=0)):
        print("hellllooooooo")
        res= db.query(Inventory.Categories).filter(Inventory.Categories.category_id == category_id).first();
        print(res)
        dependent_list = db.query(Inventory.Suppliers.company_name, Inventory.Suppliers.supplier_id) \
            .select_from(Inventory.Products) \
            .filter(Inventory.Products.category_id == category_id) \
            .join(Inventory.Suppliers, Inventory.Suppliers.supplier_id == Inventory.Products.supplier_id) \
            .distinct().all()

        formatted_data = []

        formatted_data.append({"supplier_name": k, "supplier_id": v} for k, v in dependent_list)
        result={"res":res,"data":formatted_data} #JSON Serialization
        return result




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
               .set_units_in_stock(payload.unit_in_stock)
                .set_category_id(category_id_to_set)
                .set_unit_on_order(payload.unit_on_order)
                .set_reorder_level(payload.reorder_level)
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
        return {"message": "failure", "response":"Product not found"}
        # raise HTTPException(status_code=404, detail="Product not found");


    if (deleted_product.owner_id is not None and deleted_product.owner_id != user["id"]):
        #403 is for found resource but u can't update it.
        owner_username=db.query(Inventory.User).filter(Inventory.User.user_id == deleted_product.owner_id).first().username
        return {"message": "failure", "response": f" Product can only be updated by {owner_username}"}
        # raise HTTPException(status_code=403, detail=f"Product can only be updated by {owner_username}")

    product_name=deleted_product.product_name
    db.delete(deleted_product)
    db.commit()
    return {"message":"success","status":200,"response":f" Successfully deleted product {product_name} "}









