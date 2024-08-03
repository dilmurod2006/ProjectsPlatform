from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update

from accounts.auth import accounts_routers
from database import get_async_session


app = FastAPI()
router = APIRouter()

@app.get("/salom-dunyo")
async def root():
    return {"message": "Hello World"}


app.include_router(router)
app.include_router(accounts_routers, prefix="/accounts")
app.include_router(accounts_routers, prefix="/accounts")