import json
import pandas as pd
from datetime import datetime
import os

from transformers import pipeline

# Method for loading all trend report entries  
def load_all_json():
    entries = []

    for file_name in os.listdir('trend_reports'):
        full_path = os.path.join('trend_reports', file_name)
        if os.path.isfile(full_path):
            with open(full_path, "r") as file:
                entries.extend(json.load(file))

    return entries

# Method to convert headlines into positive/negative/neutral labels
# Reference: https://huggingface.co/blog/sentiment-analysis-python and https://huggingface.co/ProsusAI/finbert
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

# Method for labeling each entry with buy/sell/hold for AI training, based on predetermined
# metrics. 
def auto_label_entry(data_frame):
    buy_count = 0
    sell_count = 0

    if buy_count > sell_count:
        return 'buy'
    elif sell_count > buy_count:
        return 'sell'
    else:
        return 'hold'

def label_entries(data_frame):

# Method for training the model
def train_model():
    return

# Main method for calling helper functions to train the model
def train_main():
    data = load_all_json()
    processed_entries = convert_headlines(data)
    data_frame = pd.json_normalize(processed_entries)
    label_entries(data_frame)

    train_model()