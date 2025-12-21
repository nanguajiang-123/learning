from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.auth import auth_router
from api.course import course_router
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

import logging
# Minimal logger (verbose logging removed per request)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# CORS（开发时允许所有来源；生产请按需配置）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router)
app.include_router(course_router)


@app.get("/")
async def root():
    return {"message": f"{settings.PROJECT_NAME} is running"}


# Tortoise ORM 初始化
register_tortoise(
    app,
    db_url=settings.get_database_url(),
    modules={"models": ["models.student", "models.course", "models.auth"]},
    generate_schemas=True,  # 开发时可设为 True
    add_exception_handlers=True,
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
