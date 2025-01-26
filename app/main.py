from fastapi import FastAPI, HTTPException
from starlette_prometheus import metrics, PrometheusMiddleware
from app.models import NewsInput, PredictionOutput
from app.ml_model.model import NewsClassifier
from app.config import settings
from prometheus_client import Counter, Histogram, Gauge
import time

app = FastAPI()

# Add Prometheus middleware
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

# Prometheus metrics
MODEL_PREDICTIONS = Counter(
    'model_predictions_total',
    'Total number of predictions made',
    ['model_name']
)

PREDICTION_LATENCY = Histogram(
    'prediction_latency_seconds',
    'Prediction latency in seconds',
    ['model_name']
)

MODEL_LOAD_STATUS = Gauge(
    'model_load_status',
    'Model load status (1 = loaded, 0 = not loaded)',
    ['model_name']
)

PREDICTION_CONFIDENCE = Histogram(
    'prediction_confidence',
    'Prediction confidence distribution',
    ['model_name']
)

classifier = NewsClassifier()

@app.on_event("startup")
async def load_model():
    try:
        start_time = time.time()
        classifier.load_model()
        MODEL_LOAD_STATUS.labels(model_name='news_classifier').set(1)
        load_time = time.time() - start_time
        print(f"✅ Model loaded successfully in {load_time:.2f} seconds")
    except Exception as e:
        MODEL_LOAD_STATUS.labels(model_name='news_classifier').set(0)
        raise RuntimeError(f"❌ Failed to load model: {str(e)}")

@app.post("/predict", response_model=PredictionOutput)
async def predict_news(item: NewsInput):
    start_time = time.time()
    try:
        prediction, confidence = classifier.predict(item.title, item.text)
        latency = time.time() - start_time
        
        # Update metrics
        MODEL_PREDICTIONS.labels(model_name='news_classifier').inc()
        PREDICTION_LATENCY.labels(model_name='news_classifier').observe(latency)
        PREDICTION_CONFIDENCE.labels(model_name='news_classifier').observe(confidence)
        
        return {
            "prediction": prediction,
            "confidence": confidence,
            "user_id": item.user_id,
            "news_title": item.title
        }
    except Exception as e:
        MODEL_PREDICTIONS.labels(model_name='news_classifier').inc()
        raise HTTPException(status_code=500, detail=str(e))