from fastapi import FastAPI
from pydantic import BaseModel
from src import predict 

app = FastAPI(
    title="Real-time Anomaly Detection API",
    description="API for detecting anomalies in time-series data using a trained Isolation Forest model.",
    version="1.0.0"
)

class PredictionRequest(BaseModel):
    value: float

@app.get("/", tags=["Status"])
def read_root():
    return {"status": "API is running"}

@app.post("/predict", tags=["Prediction"])
def get_prediction(payload: PredictionRequest):
    """
    Receives a single data point and returns an anomaly prediction.
    """
    prediction = predict.make_prediction(payload.value)
    return prediction