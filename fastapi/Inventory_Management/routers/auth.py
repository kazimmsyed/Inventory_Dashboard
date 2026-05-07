#Apirouter allow us to route from #main.py to auth.p file
from fastapi import APIRouter

router = APIRouter()

#doesnt show in docs#, technically a different fastapi application


@router.get("/auth/")
async def get_user():
    return {"username": "authenticated"}