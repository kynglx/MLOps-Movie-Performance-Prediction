from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Movie Popularity Prediction API"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.get("/mlflow")
def mlflow_connection():
    return {
        "tracking_uri": os.getenv(
            "MLFLOW_TRACKING_URI"
        )
    }