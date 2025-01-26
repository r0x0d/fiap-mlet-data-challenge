from pydantic import BaseModel

class NewsInput(BaseModel):
    title: str
    text: str
    user_id: int

class PredictionOutput(BaseModel):
    prediction: bool
    confidence: float
    user_id: int
    news_title: str