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

# Method for determining the training label depending on buy/sell count
def determine_training_label(buy_count, sell_count):
    # For reference, there are 16 conditional statments in the auto_label_entry 

    # If the difference between the too is less than 5, mark as hold
    if buy_count - sell_count < 5 or sell_count - buy_count < 5:
        return "hold"
    elif buy_count > sell_count: 
        return "buy"
    elif sell_count > buy_count:
        return "sell"

# Method for labeling an individual entry based on predetermined metrics
def auto_label_entry(entry):
    buy_count = 0
    sell_count = 0

    # Average percent changes
    if entry["avg_percent_changes"]["close_past_week"] > 1.5: buy_count += 1       # +/-1.5%
    elif entry["avg_percent_changes"]["close_past_week"] < -1.5: sell_count += 1
    if entry["avg_percent_changes"]["close_past_month"] > 3: buy_count += 1        # +/-3.0%
    elif entry["avg_percent_changes"]["close_past_month"] < -3: sell_count += 1
    if entry["avg_percent_changes"]["open_past_week"] > 1: buy_count += 1          # +/-1.0%
    elif entry["avg_percent_changes"]["open_past_week"] < -1: sell_count += 1
    if entry["avg_percent_changes"]["open_past_month"] > 2: buy_count += 1         # +/-2.0%
    elif entry["avg_percent_changes"]["open_past_month"] < -2: sell_count += 1
    if entry["avg_percent_changes"]["volume_past_week"] > 20: buy_count += 1       # +20.0%/-10.0%
    elif entry["avg_percent_changes"]["volume_past_week"] < -10: sell_count += 1
    if entry["avg_percent_changes"]["volume_past_month"] > 15: buy_count += 1      # +15.0%/-10.0%
    elif entry["avg_percent_changes"]["volume_past_month"] < -10: sell_count += 1

    # Ranges
    if entry["ranges"]["high_low_range_week"] > 10: buy_count += 1                 # +10.0%/-5.0%
    elif entry["ranges"]["high_low_range_week"] < -5: sell_count += 1
    if entry["ranges"]["high_low_range_month"] > 15: buy_count += 1                # +15.0%/-8.0%
    elif entry["ranges"]["high_low_range_month"] > -8: sell_count += 1

    # Moving Averages
    if entry["moving_avgs"]["sma_difference"] > 2: buy_count += 1                  # +/-2.0%       
    elif entry["moving_avgs"]["sma_difference"] < -2: sell_count += 1
    if entry["moving_avgs"]["sma_ratio"] > 1.02: buy_count += 1                    # 1.02 / 0.98
    elif entry["moving_avgs"]["sma_ratio"] < 0.98: sell_count += 1

    # Standard dev calcs
    if entry["standard_dev_calcs"]["closing_std_week"] < 2 : buy_count += 1        # < 2 / > 4                 
    elif entry["standard_dev_calcs"]["closing_std_week"] > 4 : sell_count += 1
    if entry["standard_dev_calcs"]["closing_std_month"] < 2 : buy_count += 1       # < 2 / > 4                   
    elif entry["standard_dev_calcs"]["closing_std_month"] > 4 : sell_count += 1
    if entry["standard_dev_calcs"]["zscore_week"] >= 0.5 and entry["standard_dev_calcs"]["zscore_week"] <= 1.5: buy_count += 1                       
    elif entry["standard_dev_calcs"]["zscore_week"] < -1.5 : sell_count += 1       # +0.5-1.5/-1.5
    if entry["standard_dev_calcs"]["zscore_month"] >= 0.5 and entry["standard_dev_calcs"]["zscore_week"] <= 2: buy_count += 1                       
    elif entry["standard_dev_calcs"]["zscore_month"] < -1.5 : sell_count += 1      # +0.5-2.0/-1.5

    # Stock news
    if entry["stock_news"]["headline_1"] == "positive": buy_count += 1             # pos / neg / neutral
    elif entry["stock_news"]["headline_1"] == "negative": sell_count += 1
    if entry["stock_news"]["headline_2"] == "positive": buy_count += 1
    elif entry["stock_news"]["headline_2"] == "negative": sell_count += 1

    # Use helper function to determine label
    return determine_training_label(buy_count, sell_count)

# Method for labeling each entry with buy/sell/hold for AI training
def label_entries(processed_entries):
    for entry in processed_entries:
        entry["label"] = auto_label_entry(entry)

    return processed_entries

# Method for training the model
def train_model(data_frame):
    return

# Main method for calling helper functions to train the model
def train_main():
    data = load_all_json()
    if data != -1:
        processed_entries = convert_headlines(data)
        labeled_entries = label_entries(processed_entries)
        data_frame = pd.json_normalize(labeled_entries)

        train_model(data_frame)