import os
import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

mlflow.set_tracking_uri("file:./mlruns")

# load dataset
df = pd.read_csv("data/processed/dataset.csv")

# fitur & target
X = df[
    [
        "vote_average",
        "vote_count",
        "release_year",
        "is_recent",
        "is_popular",
        "genre_count",
        "is_english",
        "is_adult"
    ]
]

y = df["popularity_log"]

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

RMSE_THRESHOLD = 1.0

CURRENT_MODEL_FILE = "best_rmse.txt"
if os.path.exists(CURRENT_MODEL_FILE):
    with open(CURRENT_MODEL_FILE, "r") as f:
        current_rmse = float(f.read())
else:
    current_rmse = float("inf")

def train_model(n_estimators, max_depth):

    with mlflow.start_run(
        run_name=f"RF_{n_estimators}_{max_depth}"
    ) as run:

        model = RandomForestRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            random_state=42
        )

        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        r2 = r2_score(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        mlflow.log_param(
            "n_estimators",
            n_estimators
        )

        mlflow.log_param(
            "max_depth",
            max_depth
        )

        mlflow.log_metric(
            "rmse",
            rmse
        )

        mlflow.log_metric(
            "r2",
            r2
        )

        print(
            f"Run selesai | "
            f"n_estimators={n_estimators}, "
            f"max_depth={max_depth}, "
            f"RMSE={rmse:.4f}, "
            f"R2={r2:.4f}"
        )

        return model, rmse, run.info.run_id


if __name__ == "__main__":

    experiments = [
        (50, 10),
        (100, 20),
        (200, 30)
    ]

    best_model = None
    best_rmse = float("inf")
    best_run_id = None
    best_params = None

    for n_estimators, max_depth in experiments:

        model, rmse, run_id = train_model(
            n_estimators,
            max_depth
        )

        if rmse < best_rmse:

            best_rmse = rmse
            best_model = model
            best_run_id = run_id

            best_params = {
                "n_estimators": n_estimators,
                "max_depth": max_depth
            }

    print(f"Best RMSE: {best_rmse}")
    print(f"Best Parameters: {best_params}")

    if best_rmse <= RMSE_THRESHOLD:
        print("✅ Model lolos validasi")
        if best_rmse < current_rmse:
            print("🚀 Model lebih baik dari versi sebelumnya")
            
            with mlflow.start_run(run_id=best_run_id):
                mlflow.sklearn.log_model(
                    best_model,
                    "model",
                    registered_model_name="movie-popularity-model"
                )
            with open(CURRENT_MODEL_FILE, "w") as f:
                f.write(str(best_rmse))

        else:
            print(
                "⚠️ Model baru tidak lebih baik, "
                "promosi dibatalkan"
            )

    else:
        raise Exception(
            "❌ Model gagal validasi threshold"
        )