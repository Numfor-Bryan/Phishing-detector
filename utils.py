import pandas as pd
import numpy as np 
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import re
import whois
import socket
import tldextract
from datetime import datetime
from urllib.parse import urlparse

# URL Length Feature
def get_url_length(url):
    try:
        return len(str(url))
    except:
        return 0

# Count Special Characters
def count_special_chars(url):
    special_chars = ['@', '?', '-', '_', '=', '%', '#', '.']
    return sum(str(url).count(char) for char in special_chars)

# Check HTTPS Feature
def check_https(url):
    return 1 if str(url).startswith("https") else 0  # 1 = HTTPS, 0 = HTTP

# Check Domain Age
def get_domain_age(url):
    try:
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}"
        w = whois.whois(domain)
        creation_date = w.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if creation_date is None:
            return -1
        today = datetime.now()
        return (today - creation_date).days
    except Exception as e:
        print(f"WHOIS lookup failed for {url}: {e}")
        return -1

# DNS Lookup Feature
def check_dns_resolution(url):
    try:
        domain_name = urlparse(url).netloc
        if not domain_name:
            return 0
        socket.gethostbyname(domain_name)
        return 1
    except socket.gaierror:
        return 0

# Check Suspicious Keywords
def check_suspicious_keywords(url):
    suspicious_words = ["bank", "secure", "signin", "verify", "account", "password", "update", "paypal", "facebook"]
    return 1 if any(word in str(url).lower() for word in suspicious_words) else 0

# Extract Features from a single URL
def extract_features(url):
    return [
        get_url_length(url),
        count_special_chars(url),
        check_https(url),
        get_domain_age(url),
        check_dns_resolution(url),
        check_suspicious_keywords(url)
    ]


