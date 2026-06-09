from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import Response

from prometheus_client import Counter
from prometheus_client import Histogram
from prometheus_client import Gauge
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST

import mlflow
import mlflow.pyfunc
import pandas as pd
import os
import time
import socket

app = FastAPI()

# =========================
# PROMETHEUS METRICS
# =========================

REQUEST_COUNT = Counter(
    "movie_api_requests_total",
    "Total API Requests"
)

REQUEST_LATENCY = Histogram(
    "movie_api_latency_seconds",
    "API Latency"
)

LAST_PREDICTION = Gauge(
    "movie_last_prediction",
    "Latest Prediction Value"
)

# =========================
# LOAD MODEL FROM MLFLOW
# =========================

mlflow.set_tracking_uri(
    os.getenv(
        "MLFLOW_TRACKING_URI",
        "http://mlflow-server:5000"
    )
)

model = mlflow.pyfunc.load_model(
    "models:/movie-popularity-model/latest"
)

# =========================
# INPUT SCHEMA
# =========================

class MovieInput(BaseModel):
    vote_average: float
    vote_count: int
    release_year: int
    is_recent: int
    is_popular: int
    genre_count: int
    is_english: int
    is_adult: int

# =========================
# ENDPOINTS
# =========================

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
        "status": "healthy",
        "container": socket.gethostname()
    }


@app.get("/mlflow")
def mlflow_connection():

    REQUEST_COUNT.inc()

    return {
        "tracking_uri": os.getenv(
            "MLFLOW_TRACKING_URI"
        )
    }


@app.post("/predict")
def predict(data: MovieInput):

    REQUEST_COUNT.inc()

    start_time = time.time()

    input_df = pd.DataFrame([{
        "vote_average": data.vote_average,
        "vote_count": data.vote_count,
        "release_year": data.release_year,
        "is_recent": data.is_recent,
        "is_popular": data.is_popular,
        "genre_count": data.genre_count,
        "is_english": data.is_english,
        "is_adult": data.is_adult
    }])

    prediction = model.predict(input_df)

    latency = time.time() - start_time

    REQUEST_LATENCY.observe(latency)

    LAST_PREDICTION.set(
        float(prediction[0])
    )

    return {
        "predicted_popularity": float(
            prediction[0]
        ),
        "latency_seconds": latency
    }


@app.get("/metrics")
def metrics():

    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )