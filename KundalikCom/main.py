from fastapi import FastAPI
from schemes import *
from database import *

# Fast api app yaratish
app = FastAPI()

# Xizmatni sotib olish
@app.post("/buy_api")
async def root(data: Buy):
    token = data.token
    data.months_count

    # userni qidirish tokin buyicha
    user = session.query(PcKundalikCom).filter_by(token=token)
    print(user)

@app.post("/price_months")
async def root(data: PriceMonths):
    n = data.months_count
    if n > 3:
        return 450000*n
    return 420000*n

