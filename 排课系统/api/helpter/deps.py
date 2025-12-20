from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from jose import jwt, JWTError
from pydantic import ValidationError
from core.config import settings
import secrets
import logging

logger = logging.getLogger(__name__)
from tortoise.exceptions import DoesNotExist
from models.student import Student

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/signin")
reusable_basic = HTTPBasic()


async def get_current_user(token: str = Depends(reusable_oauth2)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except (JWTError, ValidationError):
        raise credentials_exception

    # Resolve subject to Student (sub can be email or id)
   
    try:
        if "@" in sub:
            user = await Student.get(email=sub)
        else:
            user = await Student.get(id=int(sub))
    except DoesNotExist:
        raise credentials_exception

    return user
    
def get_admin_user(credentials: HTTPBasicCredentials = Depends(reusable_basic)):
    """
    管理员认证，使用数据库密码作为验证（临时 debug）
    """
    # 记录用户名（不记录密码）供排查用
    #logger.debug("Admin login attempt: username=%r", credentials.username)

    correct_username = "admin"
    correct_password = settings.POSTGRES_PASSWORD

    is_correct_username = secrets.compare_digest(credentials.username, correct_username)
    is_correct_password = secrets.compare_digest(credentials.password, correct_password)

    #logger.debug("Admin compare result: username_ok=%s, password_ok=%s", is_correct_username, is_correct_password)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
