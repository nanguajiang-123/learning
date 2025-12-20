
from pydantic import BaseModel, EmailStr


class send_code_request(BaseModel):
    id: int
    code: str

class SignUpModel(BaseModel):
    username: str
    new_password: str
    repeat_password: str
    email: EmailStr
    code: str
    grade: int 

class SignInModel(BaseModel):
    username: str
    password: str


