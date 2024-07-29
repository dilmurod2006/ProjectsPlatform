from fastapi import FastAPI
from schemes import BuySerializer
from database import *
app = FastAPI()
@app.post("/buy_api")
async def root(data: BuySerializer):

    return {"message": "Hello World"}
