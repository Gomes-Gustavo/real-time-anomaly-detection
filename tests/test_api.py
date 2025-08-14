from fastapi.testclient import TestClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.api.main import app

client = TestClient(app)

def test_read_root():
    """ Test the root endpoint to ensure the API is running. """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "API is running"}

def test_predict_normal_value():
    """ Test the /predict endpoint with a value we know is normal. """
    payload = {"value": 0.13}
    response = client.post("/predict", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["is_anomaly"] is False
    assert data["predicted_value"] == 1

def test_predict_anomaly_value():
    """ Test the /predict endpoint with a value we discovered to be anomalous. """
    payload = {"value": 2.0}
    response = client.post("/predict", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["is_anomaly"] is True
    assert data["predicted_value"] == -1

def test_predict_high_anomaly_value():
    """ Test the /predict endpoint with a high, obvious anomaly value. """
    payload = {"value": 95.0}
    response = client.post("/predict", json=payload)
    data = response.json()

    assert response.status_code == 200
    assert data["is_anomaly"] is True
    assert data["predicted_value"] == -1

def test_predict_invalid_payload():
    """ Test the API's validation by sending a payload with an incorrect key. """
    payload = {"wrong_key": 10.0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422