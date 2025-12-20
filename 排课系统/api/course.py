from fastapi import APIRouter, Depends, HTTPException, status
import random
import string
from datetime import datetime, timedelta
from tortoise.exceptions import DoesNotExist
from passlib.context import CryptContext
from starlette.concurrency import run_in_threadpool
from models.auth import user as UserModel
from models.student import Student
from core.security import create_access_token
from api.helpter.deps import get_current_user, get_admin_user
from models.course import Course

course_router = APIRouter(prefix="/course", tags=["course"])

#获取课程详情
@course_router.get("/{course_id}")
async def get_course_details(course_id: int, user: dict = Depends(get_current_user)):    
    try:
        course_obj = await Course.get(id=course_id)
        return {
            "id": course_obj.id,
            "title": course_obj.title,
            "description": course_obj.description,
            "credits": course_obj.credits,
            "created_at": course_obj.created_at,
            "updated_at": course_obj.updated_at
        }
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    
#查询课程所包含的学生
@course_router.get("/{course_id}/students")
async def get_course_students(course_id: int, user: dict = Depends(get_current_user)):
    try:
        course_obj = await Course.get(id=course_id).prefetch_related('students')
        students = await course_obj.students.all()
        return [{"id": student.id, "name": student.name, "email": student.email} for student in students]
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    



#学生选课
@course_router.post("/enroll/{course_id}")
async def enroll_in_course(course_id: int, user: dict = Depends(get_current_user)):
    user_id = user.get("user_id")
    try:
        # sub 可以是 email 或 id（字符串），尝试按 email 查找，否则按 id 查找
        if "@" in user_id:
            student = await Student.get(email=user_id)
        else:
            student = await Student.get(id=int(user_id))
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        course_obj = await Course.get(id=course_id)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # 将学生添加到课程的学生列表中
    await course_obj.students.add(student)
    await student.courses.add(course_obj)

    return {"message": f"Enrolled in course {course_obj.title} successfully."}


#学生退课
@course_router.post("/drop/{course_id}")
async def drop_course(course_id: int, user: dict = Depends(get_current_user)):
    user_id = user.get("user_id")
    try:
        # sub 可以是 email 或 id（字符串），尝试按 email 查找，否则按 id 查找
        if "@" in user_id:
            student = await Student.get(email=user_id)
        else:
            student = await Student.get(id=int(user_id))
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    try:
        course_obj = await Course.get(id=course_id)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # 将学生从课程的学生列表中移除
    await course_obj.students.remove(student)
    await student.courses.remove(course_obj)

    return {"message": f"Dropped course {course_obj.title} successfully."}


#管理员添加新课程
@course_router.post("/add")
async def add_course(title: str, description: str, credits: int, user: dict = Depends(get_admin_user)):

    new_course = await Course.create(
        title=title,
        description=description,
        credits=credits
    )
    return {
        "message": "Course added successfully",
        "course": {
            "id": new_course.id,
            "title": new_course.title,
            "description": new_course.description,
            "credits": new_course.credits
        }
    }

#更新课程信息（管理员权限）
@course_router.put("/update/{course_id}")
async def update_course(course_id: int, title: str = None, description: str = None, credits: int = None, admin: str = Depends(get_admin_user)):
    """仅管理员可更新课程，admin 参数由 get_admin_user 提供（用户名）"""
    try:
        course_obj = await Course.get(id=course_id)
        if title:
            course_obj.title = title
        if description:
            course_obj.description = description
        if credits is not None:
            course_obj.credits = credits
        await course_obj.save()
        return {"message": "Course updated successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")
    

#删除课程（管理员权限）
@course_router.delete("/delete/{course_id}")
async def delete_course(course_id: int, admin: str = Depends(get_admin_user)):
    """仅管理员可删除课程，admin 参数由 get_admin_user 提供（用户名）"""
    try:
        course_obj = await Course.get(id=course_id)
        await course_obj.delete()
        return {"message": "Course deleted successfully"}
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")


