from fastapi import FastAPI
from schemes import BuySerializer
from database import *

app = FastAPI()
@app.post("/")
async def root(data: BuySerializer):

    return {"message": "Hello World"}

