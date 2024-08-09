from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update

from accounts.auth import accounts_routers
from kundalikcom.kundalikcom import kundalik_router
from database import get_async_session
from KundalikCom.pc import pc_routers

app = FastAPI()
router = APIRouter()

@app.get("/salom-dunyo")
async def root():
    return {"message": "Hello World"}


app.include_router(router)

app.include_router(accounts_routers, prefix="/accounts")