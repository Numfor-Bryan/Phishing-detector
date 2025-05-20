import pandas as pd
from sklearn.model_selection import train_test_split
from utils import get_url_length, count_special_chars, check_https, get_domain_age, check_dns_resolution, check_suspicious_keywords

# Load dataset 
df = pd.read_csv("phishing_data.csv")
# Drop missing or NaN URLs
df = df.dropna(subset=["url"])
# Ensure all URLs are strings
df["url"] = df["url"].astype(str)

df["url_length"] = df["url"].apply(get_url_length)

df["special_chars"] = df["url"].apply(count_special_chars)
df["https"] = df["url"].apply(check_https)
df["domain_age"] = df["url"].apply(get_domain_age)
df["dns"] = df["url"].apply(check_dns_resolution)
df["suspicious_keywords"] = df["url"].apply(check_suspicious_keywords)

# Select features and labels
X = df[["url_length", "special_chars", "https", "domain_age", "dns", "suspicious_keywords"]]
df["status"] = df["status"].apply(lambda x: 1 if x == "phishing" else 0)
y = df["status"].map({"legitimate": 0, "phishing": 1})# 1 = Phishing, 0 = Legitimate

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
