from fastapi import APIRouter
import os
from openai import OpenAI
from schemas import ReqAns
import requests
import json

router = APIRouter(tags=["ai"])

def get_answer(req: ReqAns) -> str:
    api_key = os.getenv("AIHUBMIX_API_KEY")
    if not api_key:
        raise RuntimeError("缺少 AIHUBMIX_API_KEY 环境变量")

    response = requests.post(
        url=os.getenv("url"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=json.dumps({
            "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
            "messages": [
                {
                    "role": "user",
                    "content": req.question
                },
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides concise answers."
                }
            ],
        })
    )

    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        raise RuntimeError(f"API 请求失败: {response.status_code} - {response.text}")

@router.post("/", response_model=dict)
async def request_answers(req: ReqAns):
    answer = get_answer(req)
    return {"answer": answer}