from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
from utils import extract_features
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI()

# Load the trained model
model = joblib.load("model/xgb_model.pkl")

# Initialize the FastAPI app
app = FastAPI()

# Allow CORS for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input data model
class URLRequest(BaseModel):
    url: str

# Root route
@app.get("/")
def read_root():
    return {"message": "Phishing Detection API is live"}

# Prediction route
@app.post("/predict")
def predict_url(data: URLRequest):
    features = extract_features(data.url)
    prediction = model.predict([features])[0]
    probabilities = model.predict_proba([features])[0] 
    result = "Phishing" if prediction == 1 else "Legitimate"
    return {
        "url": data.url,
        "prediction": result,
        "raw_prediction": int(prediction),
        "confidence": float(max(probabilities)),
        "features": {
        "url_length": features[0],
        "special_char_count": features[1],
        "uses_https": features[2],
        "domain_age_days": features[3],
        "dns_resolves": features[4],
        "has_suspicious_keywords": features[5],
        },
        "timestamp": datetime.now().isoformat()
    }
