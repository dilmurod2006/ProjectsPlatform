from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, update
import uvicorn

from accounts.auth import accounts_routers
from kundalikcom.kundalikcom import kundalik_router
from admins.admin import admin_router
from database import get_async_session
from bot import bot
from settings import (
    API_URL,
    API_DOCS_URL,
    API_REDOC_URL
)

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
            "name": "kundalikcom",
            "description": "kundalikcom api lar foydalanish",
        },
        {
            "name": "admin",
            "description": "admin api lar foydalanish",
        }

    ],
    servers= [{"url": f"{API_URL}"}],
    openapi_url = "/projectsplatform/openapi.json",
    docs_url = API_DOCS_URL,
    redoc_url = API_REDOC_URL,
    redirect_slashes=False,
    license_info={
        "name": "ProjectsPlatform Litsenziyasi",
        "url": "https://your-license-url.com"  # Agar litsenziya URL manzilingiz bo'lsa, uni kiritishingiz mumkin
    },
    include_in_schema = True
)

# include routers
app.include_router(accounts_routers, prefix="/accounts", tags=["accounts"])
app.include_router(kundalik_router, prefix="/kundalikcom", tags=["kundalikcom"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])


# run project
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)