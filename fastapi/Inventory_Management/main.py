
from fastapi import FastAPI,Request


from database import engine, SessionLocal
from fastapi.templating import Jinja2Templates
from models import Inventory
from fastapi.staticfiles import StaticFiles

from routers import auth,Inventory_Management
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
Inventory.base.metadata.create_all(bind=engine);
app.include_router(auth.router)
app.include_router(Inventory_Management.router)

templates=Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev server
        "http://127.0.0.1:5173",   # same thing, alternate host
    ],
    allow_credentials=True,        # needed if you send cookies / Authorization
    allow_methods=["*"],           # GET, POST, OPTIONS, etc.
    allow_headers=["*"],           # Authorization, Content-Type, etc.
)


@app.get("/")
def test(request:Request):
    return templates.TemplateResponse(request, "home.html")


