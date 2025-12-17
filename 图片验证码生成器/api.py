from fastapi import APIRouter
from captcha_generator import generate_captcha
import time
from fastapi.responses import StreamingResponse
import io
from schemas import sign_in_send, sign_in_return
from models import Captcha
from config import init_db, close_db

app01 = APIRouter()

@app01.post("/")
async def sign_in(info: sign_in_send):
    png, code = generate_captcha()
    # 存储到PostgreSQL，以userid为主键（如存在则更新）
    now = time.time()
    existing = await Captcha.get_or_none(userid=info.userid)
    if existing:
        existing.code = code
        existing.timestamp = now
        await existing.save()
    else:
        await Captcha.create(userid=info.userid, code=code, timestamp=now)
    # 返回图片验证码
    img_byte_arr = io.BytesIO()
    png.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return StreamingResponse(img_byte_arr, media_type="image/png")

@app01.post("/return/")
async def sign_in_return(info: sign_in_return):
    stored = await Captcha.get_or_none(userid=info.userid)
    if stored is None:
        return {"status": "error", "message": "No code found."}
    if time.time() - stored.timestamp > 300:  # 5分钟过期
        await stored.delete()
        return {"status": "error", "message": "Code expired."}
    if stored.code == info.verify_code:
        return {"status": "success", "message": "Verification successful."}
    else:
        return {"status": "error", "message": "Verification failed."}