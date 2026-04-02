from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app=FastAPI()

#@app.middleware("http")
#async def CORSMiddleware(request: Request, call_next):
#   response = await call_next(request)
#   response.headers["Access-Control-Allow-Origin"] = "*"
#   return response
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#允许的源
    allow_credentials=True,
    allow_methods=["*"],#允许的方法
    allow_headers=["*"],#允许的头
)
    
@app.get("/user")
def get_user():
    return {"name":"John","age":30}