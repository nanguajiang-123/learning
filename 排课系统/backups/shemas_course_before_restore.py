# backup of shemas/course.py before restore
from pydantic import BaseModel, Field
from typing import Optional, Literal

class CourseModel(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    credits: int
    teacher: Optional[str] = None
    started_time: Optional[str] = Field(None, example="09:00")
    ended_time: Optional[str] = Field(None, example="10:40")
    # legacy string schedule, e.g. "Mon[1-16;odd] 09:00-10:40;Wed13:30-15:00"
    schedule: Optional[str] = Field(None, example="Mon[1-16;odd]09:00-10:40;Wed13:30-15:00")
    weeks: Optional[str] = Field(None, example="1-16,18")
    week_type: Optional[Literal['odd','even','all']] = Field(None, description="Choose 'odd'|'even'|'all' or leave empty")
    room_number: Optional[str] = Field(None, example="A101")