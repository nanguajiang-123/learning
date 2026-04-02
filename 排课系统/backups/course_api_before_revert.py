# backup of api/course.py before revert

from fastapi import APIRouter, Depends, HTTPException, status
import random
import string
from datetime import datetime, timedelta
from tortoise.exceptions import DoesNotExist
from passlib.context import CryptContext
from starlette.concurrency import run_in_threadpool
from models.auth import user as UserModel
from models.student import Student
from shemas.course import CourseModel
from core.security import create_access_token
from api.helpter.deps import get_current_user, get_admin_user
from models.course import Course
from typing import List
from api.helpter.schedule import has_conflict

course_router = APIRouter(prefix="/course", tags=["course"])