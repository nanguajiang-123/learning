from pydantic import BaseModel, Field, validator
from typing import Optional



class CourseModel(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    credits: int
    started_time: Optional[str] = Field(None, example="09:00")
    ended_time: Optional[str] = Field(None, example="10:40")
    teacher: Optional[str] = None
    schedule: Optional[str] = Field(None, example="Mon[1-16;odd]09:00-10:40;Wed13:30-15:00")
    room_number: Optional[str] = None
