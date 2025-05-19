import os
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
ENDPOINT = os.getenv("ENDPOINT")
MODEL_NAME = os.getenv("MODEL_NAME")

async def call_ai(prompt: str) -> dict:
    if not API_KEY or not ENDPOINT:
        raise HTTPException(500, "AI API key or endpoint 未配置")
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "你是一个精准的电影推荐机器人"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(ENDPOINT, headers=headers, json=body)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(502, f"AI服务错误: {e.response.status_code} {e.response.text[:200]}")
    except Exception as e:
        raise HTTPException(500, f"调用 AI 服务失败: {str(e)}")