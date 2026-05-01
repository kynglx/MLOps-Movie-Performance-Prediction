import pandas as pd
import numpy as np
import mlflow
import mlflow.sklearn

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
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
    "is_popular"
]]

y = df["popularity"]

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

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
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        # logging
        mlflow.log_param("n_estimators", n_estimators)
        mlflow.log_param("max_depth", max_depth)

        mlflow.log_metric("rmse", rmse)

        mlflow.sklearn.log_model(model, "model")

        print(f"Run selesai | n_estimators={n_estimators}, max_depth={max_depth}, RMSE={rmse}")

if __name__ == "__main__":
    train_model(100, 5)
    train_model(200, 5)
    train_model(200, 10)