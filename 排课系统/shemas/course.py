from pydantic import BaseModel

class CourseModel(BaseModel):
    title: str
    description: str
    credits: int
    started_time: str
    ended_time: str
    teacher: str
    schedule: str
    room_number: str
    