# Backup of main.py before removing verbose logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from api.auth import auth_router
from api.course import course_router
from tortoise.contrib.fastapi import register_tortoise
from tortoise import Tortoise

# Configure application logging: console + rotating file
import logging
from logging.handlers import RotatingFileHandler
import os
LOG_DIR = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s')

# console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
logger.addHandler(ch)

# rotating file handler
fh = RotatingFileHandler(os.path.join(LOG_DIR, 'app.log'), maxBytes=5 * 1024 * 1024, backupCount=5)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

app = FastAPI(title=settings.PROJECT_NAME, openapi_url=f"{settings.API_V1_STR}/openapi.json")

# ... rest omitted for brevity ...