from dotenv import load_dotenv  # 用于加载 .env 文件
import os

# 加载 .env 文件中的环境变量
load_dotenv()

DATABASE_CONFIG = {
    "db_url": f"postgres://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
    "modules": {"models": ["models"]},  # 模型模块路径
    "generate_schemas": True,               # 自动生成数据库表（开发环境用，生产环境建议关闭）
    "add_exception_handlers": True,         # 添加异常处理器
}

# --------------------------
# 应用配置
# --------------------------
APP_CONFIG = {
    "host": os.getenv("APP_HOST", "0.0.0.0"),  # 默认 0.0.0.0
    "port": int(os.getenv("APP_PORT", 8000)),   # 默认 8000（转换为整数）
    "debug": os.getenv("DEBUG", "True").lower() == "true",  # 默认 True（转换为布尔值）
}

# --------------------------
# AI 配置
# --------------------------
AI_CONFIG = {
    "api_key": os.getenv("AIHUBMIX_API_KEY"),
    "url": os.getenv("url"),
    "model": "deepseek-ai/DeepSeek-R1-Distill-Qwen-7B",
}