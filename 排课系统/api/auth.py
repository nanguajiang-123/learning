from fastapi import APIRouter, Depends, HTTPException, status
import random
import string
from datetime import datetime, timedelta
from tortoise.exceptions import DoesNotExist
from passlib.context import CryptContext
from starlette.concurrency import run_in_threadpool
from shemas.auth import SignUpModel
from fastapi.security import OAuth2PasswordRequestForm
from models.auth import user as UserModel
from models.student import Student
from core.security import create_access_token
from api.helpter.deps import get_current_user
from tortoise.transactions import in_transaction

auth_router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def generate_verification_code():
   return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@auth_router.post("/send_code")
async def send_verification_code(req: int):
    code = generate_verification_code()
    sent_at = datetime.utcnow()

    # 使用 Tortoise ORM 的事务确保原子更新/创建
    async with in_transaction() as conn:
        u = await UserModel.get_or_none(email=req)
        if u:
            u.code = code
            u.code_sent_at = sent_at
            await u.save(using_db=conn)
        else:
            await UserModel.create(email=req, code=code, code_sent_at=sent_at, using_db=conn)


    return {"code":code, "sent_at": sent_at, "message": "verification code sent successfully"}



@auth_router.post("/signup")
async def sign_up(signup_data: SignUpModel):
    if signup_data.new_password != signup_data.repeat_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )
    try:
        u = await UserModel.get(email=signup_data.email)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 验证码有效期 10 分钟
    if not u.code or u.code != signup_data.code or not u.code_sent_at or (datetime.utcnow() - u.code_sent_at) > timedelta(minutes=1):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired verification code")

    # 哈希密码（在线程池中运行以避免阻塞事件循环）
    hashed = await run_in_threadpool(pwd_context.hash, signup_data.new_password)

    student, created = await Student.get_or_create(email=signup_data.email, defaults={
        "name": signup_data.username,
        "password_hash": hashed,
        "code_sent_at": u.code_sent_at
    })
    if not created:
        student.name = signup_data.username
        student.password_hash = hashed
        student.code_sent_at = u.code_sent_at
        await student.save()

    # 验证通过后清除 user 表中的验证码
    u.code = None
    u.code_sent_at = None
    await u.save()

    return {"message": "User registered successfully", "student_id": student.id}



@auth_router.post("/signin")
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        student = await Student.get(name=form_data.username)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 验证密码（在线程池中运行以避免阻塞事件循环）
    valid_password = await run_in_threadpool(pwd_context.verify, form_data.password, student.password_hash)
    if not valid_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create JWT access token
    subject = student.email if student.email else str(student.id)
    access_token = create_access_token({"sub": subject})
    return {"access_token": access_token, "token_type": "bearer"}




@auth_router.get("/me")
async def read_me(current_user: Student = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email, "name": current_user.name}





#忘记密码
@auth_router.post("/forgot_password")   
async def forgot_password(req:SignUpModel):
    try:
        student = await Student.get(email=req.email)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 验证码有效期 10 分钟
    if not student.code or student.code != req.code or not student.code_sent_at or (datetime.utcnow() - student.code_sent_at) > timedelta(minutes=10):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired verification code")

    if req.new_password != req.repeat_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Passwords do not match"
        )

    # 哈希新密码（在线程池中运行以避免阻塞事件循环）
    hashed = await run_in_threadpool(pwd_context.hash, req.new_password)
    student.password_hash = hashed
    await student.save()

    # 验证通过后清除验证码
    student.code = None
    student.code_sent_at = None
    await student.save()

    return {"message": "Password reset successfully"}




#查询所有课程
@auth_router.get("/")
async def read_courses(user: dict = Depends(get_current_user)):
    user_id = user.get("user_id")
    try:
        # sub 可以是 email 或 id（字符串），尝试按 email 查找，否则按 id 查找
        if "@" in user_id:
            student = await Student.get(email=user_id)
        else:
            student = await Student.get(id=int(user_id))
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    # 获取该学生的所有课程（反向关系 related_name='courses'）
    courses = await student.courses.all()
    course_list = [
        {"id": c.id, "title": c.title, "description": c.description, "credits": c.credits}
        for c in courses
    ]

    return {"user_id": user_id, "courses": course_list}








    