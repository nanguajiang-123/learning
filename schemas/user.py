from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    """创建用户的请求模型"""
    username: str
    email: EmailStr  # 自动验证邮箱格式


class UserUpdate(BaseModel):
    """更新用户的请求模型"""
    email: EmailStr  # 仅允许更新邮箱


class UserResponse(BaseModel):
    """用户响应模型"""
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True  # 允许从ORM模型直接转换