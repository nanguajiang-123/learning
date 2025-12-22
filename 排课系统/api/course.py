from fastapi import APIRouter, Depends, HTTPException, status
from tortoise.exceptions import DoesNotExist
from starlette.concurrency import run_in_threadpool
from models.auth import user as UserModel
from models.student import Student
from shemas.course import CourseModel
from api.helpter.deps import get_current_user, get_admin_user
from models.course import Course
from api.helpter.schedule import has_conflict
from typing import List
import logging
from api.ai import get_answer

course_router = APIRouter(prefix="/course", tags=["course"])

#获取课程详情
@course_router.get("/{course_id}")
async def get_course_details(course_id: int, user: dict = Depends(get_current_user)):    
    try:
        course_obj = await Course.get(id=course_id)
        # try to parse stored schedule JSON (new format); if not JSON, return raw value
        schedule_val = course_obj.schedule
        schedule_parsed = None
        try:
            import json
            if schedule_val and schedule_val.strip().startswith('['):
                schedule_parsed = json.loads(schedule_val)
            else:
                schedule_parsed = schedule_val
        except Exception:
            schedule_parsed = schedule_val
        return {
            "id": course_obj.id,
            "title": course_obj.title,
            "description": course_obj.description,
            "credits": course_obj.credits,
            "created_at": course_obj.created_at,
            "updated_at": course_obj.updated_at,
            "schedule": schedule_parsed
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
async def enroll_in_course(course_id: int, current_user: Student = Depends(get_current_user)):
    """学生选课：使用当前认证的 Student 对象并检测冲突"""
    student = current_user

    try:
        course_obj = await Course.get(id=course_id)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # 检查与学生已选课程是否有时间冲突
    target_sched = course_obj.schedule
    conflicts = []
    recommendations = []
    if target_sched:
        course: List[Course] = await student.courses.all()
        for c in course:
            if c.schedule and has_conflict(target_sched, c.schedule):
                conflicts.append({"course_id": c.id, "title": c.title, "schedule": c.schedule})
                if conflicts:
                    #筛选同名或同教师的课程作为推荐
                    course_recommendations1 : List[Course]=await Course.filter(title=course_obj.title).exclude(id__in=[c["course_id"] for c in conflicts]).all()
                    for rec in course_recommendations1:
                        if not has_conflict(target_sched, rec.schedule):
                            recommendations.append({"course_id": rec.id, "title": rec.title, "schedule": rec.schedule})
                    course_recommendations2 : List[Course]=await Course.filter(teacher=course_obj.teacher).exclude(title=course_obj.title).all()        
                    for rec in course_recommendations2:
                        if not has_conflict(target_sched, rec.schedule):
                            recommendations.append({"course_id": rec.id, "title": rec.title, "schedule": rec.schedule}) 
                    answer=get_answer(f"学生选课时遇到时间冲突，已选课程：{conflicts}。请推荐一些可选课程：{recommendations}。请给出简短建议。")
                    if not recommendations:
                        #如无同名或同教师课程，推荐所有无冲突课程
                        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"message": "Schedule conflict", "conflicts": conflicts})
                    return {
                        "message": "Schedule conflict detected",
                        "conflicts": conflicts,
                        "recommendations": answer
                    }

                    
    
        # 如果已经选过，返回 400
    exists = await student.courses.filter(id=course_obj.id).exists()
    if exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already enrolled in this course")

    await student.courses.add(course_obj)

    return {"message": f"Enrolled in course {course_obj.title} successfully."}










#学生退课
@course_router.post("/drop/{course_id}")
async def drop_course(course_id: int, current_user: Student = Depends(get_current_user)):
    """学生退课：使用当前认证的 Student 对象"""
    student = current_user

    try:
        course_obj = await Course.get(id=course_id)
    except DoesNotExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Course not found")

    # 如果学生未选此课，返回 400
    exists = await student.courses.filter(id=course_obj.id).exists()
    if not exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enrolled in this course")

    await student.courses.remove(course_obj)

    return {"message": f"Dropped course {course_obj.title} successfully."}





#管理员添加新课程
@course_router.post("/add")
async def add_course(course_in: CourseModel, user: dict = Depends(get_admin_user)):
    # 检查是否存在相同标题的课程
    logger = logging.getLogger(__name__)
    try:
        existing = await Course.filter(id=course_in.id).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Course with this title already exists")
        new_course = await Course.create(
            id=course_in.id,
            title=course_in.title,
            description=course_in.description,
            credits=course_in.credits,
            teacher=course_in.teacher,
            schedule=course_in.schedule,
            room_number=course_in.room_number,

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
    except HTTPException:
        # 已经是有意义的 HTTP 错误，直接抛出
        raise
    except Exception as e:
        # Log the error with payload (safe fields) and stack trace for debugging
        try:
            payload = {k: v for k, v in (course_in.dict() if hasattr(course_in, 'dict') else {}) .items() if k not in ('password',)}
        except Exception:
            payload = getattr(course_in, 'title', None)
        logger.exception("Error adding course title=%r payload=%r", getattr(course_in, 'title', None), payload)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error while adding course")
    


    



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


