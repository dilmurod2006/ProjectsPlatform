# import random
# import httpx
# import asyncio
# import time
# import pytest

# def generate_tg_id():
#     return ''.join(random.choices('0123456789', k=16))

# def generate_phone_number():
#     return f"+998{random.randint(90, 99)}{random.randint(1000000, 9999999)}"

# @pytest.mark.asyncio
# async def test_performance():
#     url = "http://127.0.0.1:8000/accounts/for_register_bot_api"
#     payloads = [{"tg_id": generate_tg_id(), "phone": generate_phone_number()} for _ in range(1000)]

#     limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)

#     async with httpx.AsyncClient(limits=limits, timeout=10.0) as async_client:
#         start_time = time.time()

#         tasks = [async_client.post(url, json=payload) for payload in payloads]
#         responses = await asyncio.gather(*tasks)

#         end_time = time.time()
#         print(f"Performance test completed in {end_time - start_time} seconds")

#         for response in responses:
#             assert response.status_code == 200

