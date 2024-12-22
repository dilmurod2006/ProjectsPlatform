import httpx
import pytest

@pytest.mark.asyncio
async def test_xss():
    url = "http://127.0.0.1:8000/comment"
    payload = {
        "comment": "<script>alert('XSS');</script>"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        
        # XSS hujumi muvaffaqiyatli bo'lsa, skript bajariladi
        assert "<script>" not in response.text
