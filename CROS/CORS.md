# CORS跨域请求
不同源请求时，服务器不可能让任何客户端都能访问，这时需要在响应头里面做一些改变，才能让特定需要的客户端可以成功访问服务器，如果允许某个特定客户端访问某个服务器的所有路由接口，可以加入中间件
```python
@app.middleware("http")
async def CORSMiddleware(request: Request, call_next):
   response = await call_next(request)
   response.headers["Access-Control-Allow-Origin"] = "*"
   return response
```
后续也可以使用fastapi自带的跨域请求中间件
