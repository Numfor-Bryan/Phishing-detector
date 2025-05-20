import pandas as pd
from utils import extract_features
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import xgboost as xgb
import joblib

def load_dataset(filepath):
    df = pd.read_csv(filepath)
    df = df.dropna(subset=["url", "status"])
    X = df["url"].apply(extract_features).tolist()
    y = df["status"]
    return X, y

def main():
    print("Loading dataset...")
    X, y = load_dataset("phishing_data.csv")

    print("Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training XGBoost model...")
    model = xgb.XGBClassifier(eval_metric='logloss')
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {acc:.4f}")
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    print("Saving model to model/xgb_model.pkl...")
    joblib.dump(model, "model/xgb_model.pkl")
    print("Done!")

if __name__ == "__main__":
    main()
