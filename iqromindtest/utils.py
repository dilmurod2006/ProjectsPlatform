
from sqlalchemy.ext.asyncio import AsyncSession
import requests
from sqlalchemy import(
    select,
    delete
)
from bs4 import BeautifulSoup
from urllib.parse import unquote
from fastapi import Depends, HTTPException
from typing import Dict
from models.models import loginsdata


def months_size_price(month: int, year: int, months_count: int) -> int:
    return month*(months_count%12) + year*(months_count//12)


