import json
import pandas as pd
from datetime import datetime

from transformers import pipeline

def load_all_json(stock_code):
    json_name = fr"trend_reports/{stock_code}_reports.json"
    with open(json_name, "r") as file:
        entrys = json.load(file)
    return entrys

def convert_headlines(data):
    sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

    processed_entries = []

    for entry in data:
        updated_sentiment = {}
        for key, headline in entry["stock_news"].items():
            result = sentiment_pipeline(headline)[0]
            updated_sentiment[key] = result["label"]

        entry["headline_sentiment"] = updated_sentiment
        processed_entries.append(entry)

    return processed_entries


def auto_label():


def train_model():

def train_main(stock_code):
    data = load_all_json(stock_code)
    processed_entries = convert_headlines(data)
    data_frame = pd.json_normalize(processed_entries)

    train_model()