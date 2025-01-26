import mlflow
from prometheus_client import Counter, Gauge
from app.config import settings

MODEL_LOAD_ATTEMPTS = Counter(
    'model_load_attempts_total',
    'Total number of model load attempts',
    ['model_name']
)

MODEL_LOAD_ERRORS = Counter(
    'model_load_errors_total',
    'Total number of model load errors',
    ['model_name']
)

class NewsClassifier:
    def __init__(self):
        self.model = None
        self.model_loaded = False
        
    def load_model(self):
        MODEL_LOAD_ATTEMPTS.labels(model_name='news_classifier').inc()
        try:
            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
            # Load the model as sklearn flavor to access all methods
            self.model = mlflow.sklearn.load_model(settings.model_uri)
            self.model_loaded = True
        except Exception as e:
            MODEL_LOAD_ERRORS.labels(model_name='news_classifier').inc()
            raise RuntimeError(f"Error loading model: {str(e)}")
    
    def predict(self, title: str, text: str) -> tuple:
        if not self.model_loaded:
            raise RuntimeError("Model not loaded")
            
        combined_text = f"{title} {text}"
        
        # Make prediction
        prediction = self.model.predict([combined_text])
        
        # Get confidence score
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba([combined_text])
            confidence = float(max(proba[0]))
        else:
            # If no predict_proba, use a default confidence of 1.0
            confidence = 1.0
            
        return bool(prediction[0]), confidence