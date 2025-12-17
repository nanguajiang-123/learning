from tortoise import Tortoise
from dotenv import load_dotenv
import os

load_dotenv()

async def init_db():
    await Tortoise.init(
        db_url=f"postgres://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}",
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()

async def close_db():
    await Tortoise.close_connections()