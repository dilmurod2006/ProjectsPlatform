# IQROMIND TEST BOT ROUTER
from fastapi import APIRouter

iqromindtest_bot_router = APIRouter()
@iqromindtest_bot_router.get("/helle")
async def helle():
    return {"message": "hi"}