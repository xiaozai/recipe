import httpx
import asyncio

async def test():
    # Test SiliconCloud API
    url = 'https://api.siliconflow.cn/v1/chat/completions'
    headers = {
        'Authorization': 'Bearer ysk-sp-4bdeb4e88d034c3ea4c7a8fb06d9545c',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'Qwen/Qwen2.5-7B-Instruct',
        'messages': [{'role': 'user', 'content': 'Hello'}],
        'max_tokens': 10
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        print('Status:', response.status_code)
        print('Response:', response.text[:500])

asyncio.run(test())
