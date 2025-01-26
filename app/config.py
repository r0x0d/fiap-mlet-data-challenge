import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_uri: str = os.getenv("MODEL_URI", "runs:/0254ba4a642141d7ae60498ec943baca/model")
    mlflow_tracking_uri: str = os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")

settings = Settings()