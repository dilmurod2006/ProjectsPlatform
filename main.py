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
<<<<<<< HEAD
app.include_router(accounts_routers, prefix="/accounts")
=======
>>>>>>> 78a12182d4fcea9fab5257eac5df6728010108c6
app.include_router(accounts_routers, prefix="/accounts")