from pydantic import BaseModel


class Question(BaseModel):
    text: str


class Answer(BaseModel):
    question: str
    text: str
    cost_usd: float = 0.0
    retries: int = 0

