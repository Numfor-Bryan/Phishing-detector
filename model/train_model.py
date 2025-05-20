import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import joblib
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import extract_features

def load_dataset(csv_file):
    df = pd.read_csv(csv_file)

    # Ensure 'url' and 'status' columns exist
    df = df.dropna(subset=["url", "status"])
    df["label"] = df["status"].map({"phishing": 1, "legitimate": 0})

    features = df["url"].apply(extract_features)
    X = list(features)
    y = df["status"].values
    return X, y

if __name__ == "__main__":
    print("Loading data...")
    X, y = load_dataset("phishing_data.csv")

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training model...")
    model = XGBClassifier()
    model.fit(X_train, y_train)

    print("Saving model...")
    joblib.dump(model, "model/xgb_model.pkl")
    print("Model saved to model/xgb_model.pkl")
