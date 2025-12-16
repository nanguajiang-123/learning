from pydantic import BaseModel


class ReqAns(BaseModel):
    question: str