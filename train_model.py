import mlflow
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from mlflow.models.signature import infer_signature

# Dummy training data
data = {
    'text': ['Breaking news: Major event happened', 'Cats are cute animals', 
             'Important political decision', 'Recipe for chocolate cake'],
    'label': [1, 0, 1, 0]
}

df = pd.DataFrame(data)

# MLflow setup
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("News Classification")

with mlflow.start_run():
    # Create and train model
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', LogisticRegression())
    ])
    
    pipeline.fit(df['text'], df['label'])
    
    # Infer signature
    signature = infer_signature(df['text'], pipeline.predict(df['text']))
    
    # Log model with sklearn flavor
    mlflow.sklearn.log_model(
        sk_model=pipeline,
        artifact_path="model",
        signature=signature,
        registered_model_name="news_classifier"
    )
    
    print("✅ Model logged successfully!")