from pydantic import BaseModel

class sign_in_send(BaseModel):
    userid:str

class sign_in_return(BaseModel):
    userid:str
    verify_code:str