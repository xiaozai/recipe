import httpx
import asyncio

async def test():
    # Test with user's config
    url = 'https://coding.dashscope.aliyuncs.com/v1/chat/completions'
    headers = {
        'Authorization': 'Bearer sk-sp-4bdeb4e88d034c3ea4c7a8fb06d9545c',
        'Content-Type': 'application/json'
    }
    payload = {
        'model': 'qwen3.5-plus',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Hello, who are you?'}
        ],
        'max_tokens': 50
    }
    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            response = await client.post(url, headers=headers, json=payload)
            print('Status:', response.status_code)
            print('Response:', response.text)
        except Exception as e:
            print(f'Error: {e}')

asyncio.run(test())
