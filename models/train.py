import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (mean_squared_error, r2_score)
from sklearn.metrics import mean_squared_error

mlflow.set_tracking_uri("file:./mlruns")

# load dataset
df = pd.read_csv("data/processed/dataset.csv")

# fitur & target
X = df[[
    "vote_average",
    "vote_count",
    "release_year",
    "is_recent",
    "is_popular",
    "genre_count",
    "is_english",
    "is_adult"
]]

y = df["popularity_log"]

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

RMSE_THRESHOLD = 110


def train_model(n_estimators, max_depth):

    with mlflow.start_run():

        # model
        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )

        model.fit(X_train, y_train)

        # prediksi
        y_pred = model.predict(X_test)

        # metric
        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # logging
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)

        print(
            f"Run selesai | n_estimators={n_estimators}, max_depth={max_depth}, RMSE={rmse:.2f}, R2={r2:.4f}"
        )

        return model, rmse


if __name__ == "__main__":

    experiments = [
        (200, 30)
    ]

    best_model = None
    best_rmse = float("inf")

    for n_estimators, max_depth in experiments:

        model, rmse = train_model(
            n_estimators,
            max_depth
        )

        if rmse < best_rmse:
            best_rmse = rmse
            best_model = model

    print(f"Best RMSE: {best_rmse}")

    # validation threshold
    if best_rmse <= RMSE_THRESHOLD:

        print("✅ Model lolos validasi")

        mlflow.sklearn.log_model(
            best_model,
            "model",
            registered_model_name="movie-popularity-model"
        )

    else:
        raise Exception(
            "❌ Model gagal validasi threshold"
        )