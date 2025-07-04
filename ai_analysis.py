import json
import pandas as pd
import os
from datetime import datetime

trained_model_name = "trained_stock_model.pkl"

# Method to convert headlines into positive/negative/neutral labels
# Reference: https://huggingface.co/blog/sentiment-analysis-python and https://huggingface.co/ProsusAI/finbert
def headlines_pos_neg(entry):
    from transformers import pipeline
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

# Method for analyzing stock 
def analyze_stock(data_frame, stock_code):
    import joblib

    # Ensure trained model exists, load it
    if not os.path.exists(trained_model_name):
        print("\nTrained model does not yet exist. Please train model (option 2)...\n")
        return
    model = joblib.load(trained_model_name)

    # Select features
    feature_columns = [
        "avg_percent_changes.close_past_week",
        "avg_percent_changes.close_past_month",
        "avg_percent_changes.open_past_week",
        "avg_percent_changes.open_past_month",
        "avg_percent_changes.volume_past_week",
        "avg_percent_changes.volume_past_month",
        "ranges.high_low_range_week",
        "ranges.high_low_range_month",
        "moving_avgs.sma_difference",
        "moving_avgs.sma_ratio",
        "standard_dev_calcs.closing_std_week",
        "standard_dev_calcs.closing_std_month",
        "standard_dev_calcs.zscore_week",
        "standard_dev_calcs.zscore_month",
        "headline_sentiment.headline_1",
        "headline_sentiment.headline_2"
    ]

    # Input features
    x_features = data_frame[feature_columns]
    prediction = model.predict(x_features)[0]

    # Map result to label
    label_map = {1: "buy", 0: "hold", -1: "sell"}
    predicted_label = label_map.get(prediction, "unknown")

    print(f"\nPrediction for {stock_code}: {predicted_label.upper()}\n")

# Main method for the AI analysis portion of the project
def ai_analysis(stock_code):
    entry = load_json(stock_code)
    processed_entry = headlines_pos_neg(entry)
    data_frame = pd.json_normalize(processed_entry)

    # Map pos / neu / neg to 1 / 0 / -1 
    data_frame["headline_sentiment.headline_1"] = data_frame["headline_sentiment.headline_1"].map({"positive": 1, "neutral": 0, "negative": -1})
    data_frame["headline_sentiment.headline_2"] = data_frame["headline_sentiment.headline_2"].map({"positive": 1, "neutral": 0, "negative": -1})

    analyze_stock(data_frame, stock_code)

if __name__ == "__main__":
    stock_code = input("Enter stock code to analyze with last report: ")
    ai_analysis(stock_code)