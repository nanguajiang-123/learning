from fastapi import APIRouter
import os
from openai import OpenAI
from shemas.ai import ReqAns
import requests
import json
import dotenv
from starlette.concurrency import run_in_threadpool

# Load .env into process environment (if present)
dotenv.load_dotenv()

router = APIRouter(tags=["ai"])

def get_answer(question: str) -> str:
    api_key = os.getenv("OPENAI_AI_KEY")
    if not api_key:
        raise RuntimeError("缺少 OPENAI_AI_KEY 环境变量")

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
                    "content": question
                },
                {
                    "role": "system",
                    "content": "你是一个教学助理，回答要简洁明了。推荐别人课程时，只需给出课程id，课程标题，课程老师，课程时间段，课程地点以及推荐理由，不要包含其他内容。"
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
    # Run synchronous network call in threadpool to avoid blocking the event loop
    answer = await run_in_threadpool(get_answer, req.question)
    return {"answer": answer}