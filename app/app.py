from fastapi import FastAPI
from prometheus_client import Counter
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi.responses import Response
import os

app = FastAPI()

REQUEST_COUNT = Counter(
    "movie_api_requests_total",
    "Total API Requests"
)

@app.get("/")
def home():
    REQUEST_COUNT.inc()

    return {
        "message": "Movie Popularity Prediction API"
    }

@app.get("/health")
def health():
    REQUEST_COUNT.inc()

    return {
        "status": "healthy"
    }

@app.get("/mlflow")
def mlflow_connection():
    REQUEST_COUNT.inc()

    return {
        "tracking_uri": os.getenv(
            "MLFLOW_TRACKING_URI"
        )
    }

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )