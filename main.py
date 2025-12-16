from fastapi import FastAPI
from tortoise import Tortoise
from config import DATABASE_CONFIG, APP_CONFIG
from api import users_router, ai_router

app = FastAPI()

# 注册路由
app.include_router(users_router, prefix="/users")
app.include_router(ai_router, prefix="/ai")

@app.on_event("startup")
async def startup():
    await Tortoise.init(config=DATABASE_CONFIG)

@app.on_event("shutdown")
async def shutdown():
    await Tortoise.close_connections()

@app.get("/")
def root():
    return {"message": "Welcome to the API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=APP_CONFIG["host"], port=APP_CONFIG["port"])



