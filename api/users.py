from fastapi import APIRouter, HTTPException
from tortoise.exceptions import IntegrityError

from models import User
from schemas import UserCreate, UserUpdate, UserResponse

# 创建路由实例
router = APIRouter(tags=["users"])


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(user_data: UserCreate):
    """创建新用户（返回值判断方式）"""
    # 先检查用户名是否已存在（避免重复创建）
    existing_user = await User.filter(username=user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 再检查邮箱是否已存在
    existing_email = await User.filter(email=user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="邮箱已存在")
    
    # 所有检查通过，创建用户
    user = await User.create(**user_data.model_dump())
    return user


@router.get("/", response_model=list[UserResponse])
async def get_users():
    """获取所有用户"""
    users = await User.all()
    return users




@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """根据ID获取单个用户（返回值判断方式）"""
    # 使用filter().first()查询，无结果返回None
    user = await User.filter(id=user_id).first()
    # 检查是否找到用户
    if not user:
        raise HTTPException(status_code=404, detail=f"用户ID {user_id} 不存在")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate):
    """根据ID更新用户（返回值判断方式）"""
    # 1. 检查用户是否存在
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"用户ID {user_id} 不存在")
    
    # 2. 检查新邮箱是否已被其他用户使用
    existing_email = await User.filter(email=user_data.email).exclude(id=user_id).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="邮箱已被其他用户使用")
    
    # 3. 更新用户信息
    user.email = user_data.email
    await user.save()
    return user


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """根据ID删除用户（返回值判断方式）"""
    # 1. 检查用户是否存在
    user = await User.filter(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"用户ID {user_id} 不存在")
    
    # 2. 删除用户
    await user.delete()
    return None  # 204状态码不需要返回内容