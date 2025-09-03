from typing import TypedDict, Optional
from datetime import datetime

class QuestionData(TypedDict):
    text: str

class AnswerData(TypedDict):
    text: str
    user_id: str

class QuestionResponse(TypedDict):
    id: int
    text: str
    created_at: datetime
    answers_count: int

class AnswerResponse(TypedDict):
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime

class QuestionDetailResponse(TypedDict):
    id: int
    text: str
    created_at: datetime
    answers: list[AnswerResponse]
