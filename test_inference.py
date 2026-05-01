import mlflow.pyfunc
import pandas as pd

# load model dari Production
model = mlflow.pyfunc.load_model("models:/movie-popularity-model/Production")

# contoh data 
data = pd.DataFrame([{
    "vote_average": 8.1,
    "vote_count": 2500,
    "release_year": 2024,
    "is_recent": True,
    "is_popular": False
}])

# prediksi
pred = model.predict(data)

print("Hasil prediksi:", pred)