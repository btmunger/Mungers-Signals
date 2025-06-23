import json
import pandas as pd
from datetime import datetime

from transformers import pipeline

# Method to convert headlines into positive/negative/neutral labels
# Reference: https://huggingface.co/blog/sentiment-analysis-python and https://huggingface.co/ProsusAI/finbert
def headlines_pos_neg(entry):
    sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert") # Finbert model is great with finances, use this instead of default model
    updated_sentiment = {}

    # Mark each headline as positive, negative, neutral
    for key, headline in entry["stock_news"].items():
        result = sentiment_pipeline(headline)[0]
        updated_sentiment[key] = result["label"]

    # Update the entry with pos/neg/neu for the headline, return new entry
    entry["headline_sentiment"] = updated_sentiment
    return entry

# Method to return to retrieve a json file and return the most up to date entry
def load_json(stock_code):
    json_name = fr"trend_reports/{stock_code}_reports.json"

    with open(json_name, "r") as file:
        data = json.load(file)
    
    # Return the last entry
    latest_entry = max(data, key=lambda x: datetime.fromisoformat(x["timestamp"]))
    return latest_entry


# Main method for the AI analysis portion of the project
def ai_analysis(stock_code):
    entry = load_json(stock_code)
    entry = headlines_pos_neg(entry)
    data_frame = pd.json_normalize(entry)