from mlflow.tracking import MlflowClient

MODEL_NAME = "movie-popularity-model"

client = MlflowClient()

# ambil model version terbaru
latest_versions = client.search_model_versions(
    f"name='{MODEL_NAME}'"
)

latest_version = latest_versions[-1].version

# pindahkan ke staging
client.transition_model_version_stage(
    name=MODEL_NAME,
    version=latest_version,
    stage="Staging"
)

print(f"Model version {latest_version} moved to Staging")