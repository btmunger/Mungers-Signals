import json
import pandas as pd
from datetime import datetime
import os

from transformers import pipeline

# Method for loading all trend report entries  
def load_all_json():
    entries = []
    entries_added = 0

    for file_name in os.listdir('trend_reports'):
        full_path = os.path.join('trend_reports', file_name)
        if os.path.isfile(full_path):
            with open(full_path, "r") as file:
                entries.extend(json.load(file))
                entries_added += 1

    if entries_added == 0:
        print("\nNo entries found, could not train model")
        return -1

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

# Method for labeling an individual entry based on predetermined metrics
def auto_label_entry(entry):
    buy_count = 0
    sell_count = 0

    # Average percent changes
    if entry["avg_percent_changes"]["close_past_week"] > .5: buy_count += 1
    elif entry["avg_percent_changes"]["close_past_week"] < -.5: sell_count += 1
    if entry["avg_percent_changes"]["close_past_month"] > 1: buy_count += 1
    elif entry["avg_percent_changes"]["close_past_month"] < -1: sell_count += 1
    if entry["avg_percent_changes"]["open_past_week"] > .5: buy_count += 1
    elif entry["avg_percent_changes"]["open_past_week"] < -.5: sell_count += 1
    if entry["avg_percent_changes"]["open_past_month"] > 1: buy_count += 1
    elif entry["avg_percent_changes"]["open_past_month"] < -1: sell_count += 1
    if entry["avg_percent_changes"]["volume_past_week"] > 5: buy_count += 1
    elif entry["avg_percent_changes"]["volume_past_week"] < -5: sell_count += 1

    # Ranges

    # Moving Averages

    # Standard dev calcs

    # Stock news
    if entry["stock_news"]["headline_1"] == "positive": buy_count += 1 
    else: sell_count += 1
    if entry["stock_news"]["headline_2"] == "positive": buy_count += 1
    else: sell_count += 1

    if buy_count > sell_count:
        return 'buy'
    elif sell_count > buy_count:
        return 'sell'
    else:
        return 'hold'

# Method for labeling each entry with buy/sell/hold for AI training
def label_entries(processed_entries):
    for entry in processed_entries:
        entry["label"] = auto_label_entry(entry)

    return processed_entries

# Method for training the model
def train_model():
    return

# Main method for calling helper functions to train the model
def train_main():
    data = load_all_json()
    if data != -1:
        processed_entries = convert_headlines(data)
        labeled_entries = label_entries(processed_entries)
        data_frame = pd.json_normalize(labeled_entries)

        train_model()