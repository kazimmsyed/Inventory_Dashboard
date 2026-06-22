#Apirouter allow us to route from #main.py to auth.p file
from datetime import timedelta, datetime, timezone

from cryptography.hazmat.decrepit.ciphers import algorithms
from fastapi import Depends, APIRouter, HTTPException, Request, Path
from typing import List, Dict, Any, Annotated

from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer # to have secure forms on Swagger
from jose import jwt,JWTError
from fastapi.templating import Jinja2Templates
#local imports
from models import Inventory
from schemas.User import UserRequest,Token
from schemas.User import UserBuilder

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)
#doesn't show in docs#, technically a different fastapi application
SECRET_KEY="c7a4a67b2f1b2e1d755f2b4ce07cb980fb784970e8d322b71d3ca65c9043479b"
ALGORITHM="HS256"
bycrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")#hashing algo
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")





def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close();

db_dependency=Annotated[Session,Depends(get_db)]
templates=Jinja2Templates(directory="templates")
###PAGES###

@router.get("/login")
def render_login_page(request:Request):
    return templates.TemplateResponse(request, "login.html")

@router.get("/register")
def render_login_page(request:Request):
    return templates.TemplateResponse(request, "register.html")


###Endpoints###
@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user:UserRequest):
    user = UserBuilder().set_name(create_user.first_name,create_user.last_name) \
                    .set_identity(create_user.email, create_user.username)\
                    .set_password(bycrypt_context.hash(create_user.hashed_password))\
                    .build();
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_access_token(username:str,user_id:int, expires_delta:timedelta):
    encoded_jwt = {"sub":username,"id":user_id}
    expires=datetime.now(timezone.utc) + expires_delta
    encoded_jwt.update({"exp":expires})
    return jwt.encode(encoded_jwt,SECRET_KEY,algorithm=ALGORITHM)
    #just like hmac it involves the secret key and algo
    #It verifies the server and when passed in with Http method from Client to Server
    #The server recognizes the jwt and unpacks the data
    # the fact that it can unpack means it wasnt altered.
    # And if the criteria in the token met, quick access is given
    # token is sent throught TLS, there is no more security needed than that.

#for every future req, we will execute this first to verify the token
async def get_curr_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id:int = payload.get("id")
        #user id can be zero.
        if username is None and user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return {'username':username,'id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials")
    except Exception as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"{err} went wrong")

def authenticate_user(db:db_dependency,user_name:str, password:str):
    user = db.query(Inventory.User).filter(Inventory.User.username == user_name).first()
    if not user:
        return False
    print(user.hashed_password)
    if not bycrypt_context.verify(password, user.hashed_password):
        return False
    return user




@router.post("/token",response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm,Depends()],
                                 db:db_dependency):
    user = authenticate_user(db,form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    token=create_access_token(user.username, user.user_id,timedelta(minutes=180))
    return {'access_token':token,'token_type':'bearer'}

@router.get("/user/{username}",status_code=status.HTTP_200_OK)
async def get_user(db:db_dependency,username:str=Path(min_length=4)):
    #use exists() over first(), it doesnt load the whole object
    user_exists=db.query(Inventory.User).filter(Inventory.User.username == username).exists()
    #above is just a sql stmt prepartion.
    if db.query(user_exists).scalar():
        # A user with that username already exist
        #Technically correct, but interferes with Network tab.
        #raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Authentication Failed")
        return {"available":False,"message":"Username is taken"}
    return {"available":True,"message":"Username is available"}