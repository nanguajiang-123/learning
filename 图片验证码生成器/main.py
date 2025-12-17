from fastapi import FastAPI
from captcha_generator import generate_captcha
from dotenv import load_dotenv
from api import app01
from config import init_db, close_db
import logging

load_dotenv()  # 加载.env文件

app = FastAPI()
app.include_router(app01)

@app.on_event("startup")
async def startup_event():
    try:
        await init_db()
    except Exception:
        logging.exception("Failed to initialize database (Tortoise)")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()



