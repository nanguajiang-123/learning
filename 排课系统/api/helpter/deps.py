from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session
from core.config import settings
import secrets


reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/signin")
reusable_basic = HTTPBasic()
async def get_current_user(token: str = Depends(reusable_oauth2)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"user_id": user_id}
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
def get_admin_user(credentials: HTTPBasicCredentials = Depends(reusable_basic)):
    """
    管理员认证，使用数据库密码作为验证
    """
    correct_username = "admin"
    correct_password = settings.POSTGRES_PASSWORD

    is_correct_username = secrets.compare_digest(credentials.username, correct_username)
    is_correct_password = secrets.compare_digest(credentials.password, correct_password)

    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect admin credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
