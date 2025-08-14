import joblib
import pandas as pd
from . import config  

try:
    model = joblib.load(config.MODEL_PATH)
    print("Model loaded successfully.")
except FileNotFoundError:
    print(f"Error: Model file not found at {config.MODEL_PATH}")
    model = None

def make_prediction(value: float) -> dict:
    """
    Makes an anomaly prediction using the loaded model.
    """
    if model is None:
        return {"error": "Model not loaded."}

    input_df = pd.DataFrame({'value': [value]})

    prediction_raw = model.predict(input_df)[0]

    is_anomaly = bool(prediction_raw == -1)

    result = {
        "is_anomaly": is_anomaly,
        "predicted_value": int(prediction_raw)
    }

    return result
