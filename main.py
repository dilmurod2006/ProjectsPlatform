from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
import uvicorn

from accounts.auth import accounts_routers
from admins.admin import admin_router
from kundalikcom.kundalikcom import kundalik_router
from iqromindtest.iqromindtest import iqromind_router
from database import get_async_session
from settings import (
    API_URL,
    API_DOCS_URL,
    API_REDOC_URL
)
from starlette.middleware.cors import CORSMiddleware
# API_URL = "http://localhost:8000"
# Loyiha haqida
loyiha_haqida = """
Projects Platform 
Mualliflar: Amonov Dilmurod va Boynazarov Bexruz
"""

app = FastAPI(
    debug=True,
    title="Projects Platform",
    description=loyiha_haqida,
    version="1.0.0",
    openapi_tags=[
        {
            "name": "accounts",
            "description": "Account api lar foydalanish",
            
        },
        {
            "name": "admin",
            "description": "admin api lar foydalanish",
        },
        {
            "name": "kundalikcom",
            "description": "kundalikcom api lar foydalanish",
        },
        {
            "name": "iqromindtest",
            "description": "iqromindtest api lar foydalanish",
        },
        {
            "name": "iqromindtestbot",
            "description": "iqromindtestbot api lar foydalanish",
        }

    ],
    servers= [{"url": f"{API_URL}"}, {"url": f"http://localhost:8000"}],
    openapi_url = "/projectsplatform/openapi.json",
    docs_url = API_DOCS_URL,
    redoc_url = API_REDOC_URL,
    redirect_slashes=False,
    license_info={
        "name": "ProjectsPlatform Litsenziyasi",
        "url": "https://projectsplatform.uz"  # Agar litsenziya URL manzilingiz bo'lsa, uni kiritishingiz mumkin
    },
    include_in_schema = True
)

# CORS-ni faqat kerakli domenlarga ruxsat berish
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=["https://api.prjectsplatform.uz","https://projectsplatform.uz","www.projectsplatform.uz","www.api.prjectsplatform.uz"],  # Faol domenlar ro'yxati
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],  # Kerakli metodlarni belgilash
    allow_headers=["*"],  # Barcha headerlarga ruxsat beradi
)



# include routers
app.include_router(accounts_routers, prefix="/accounts", tags=["accounts"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
app.include_router(kundalik_router, prefix="/kundalikcom", tags=["kundalikcom"])
app.include_router(iqromind_router, prefix="/iqromindtest", tags=["iqromindtest"])


# run project
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
