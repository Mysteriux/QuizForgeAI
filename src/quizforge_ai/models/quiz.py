from pydantic import BaseModel
from typing import List, Literal, Optional

class Question(BaseModel):
    question: str
    type: Literal["multiple_choice", "true_false", "short_answer"]
    correct_answer: str
    explanation: str
    difficulty: str
    options: Optional[List[str]] = None

class QuizOutput(BaseModel):
    questions: List[Question]