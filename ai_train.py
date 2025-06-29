import json
import pandas as pd
from datetime import datetime
import os

entries_num = 0
trained_model_name = "trained_stock_model.pkl"

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

    print("\nLoaded all trend reports. ")
    return entries

# Method to convert headlines into positive/negative/neutral labels
# Reference: https://huggingface.co/blog/sentiment-analysis-python and https://huggingface.co/ProsusAI/finbert
def convert_headlines(data):
    from transformers import pipeline
    sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert")

    processed_entries = []

    for entry in data:
        updated_sentiment = {}
        for key, headline in entry["stock_news"].items():
            result = sentiment_pipeline(headline)[0]
            updated_sentiment[key] = result["label"]

        entry["headline_sentiment"] = updated_sentiment
        processed_entries.append(entry)

    print("\nConverted headlines to positive / negative / neutral sentiments. ")
    return processed_entries

# Method for determining the training label depending on buy/sell count
def determine_training_label(buy_count, sell_count):
    # For reference, there are 16 conditional statments in the auto_label_entry
    #print(f"buy_count: {buy_count} sell_count: {sell_count}") 

    # If the difference between the too is less than 5, mark as hold
    if abs(buy_count - sell_count) < 2:
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
    if entry["standard_dev_calcs"]["zscore_month"] >= 0.5 and entry["standard_dev_calcs"]["zscore_month"] <= 2: buy_count += 1                       
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
    global entries_num

    for entry in processed_entries:
        entry["label"] = auto_label_entry(entry)
        entries_num += 1

    print(f"\nLabeled {entries_num} entries with training indicators. ")
    return processed_entries

# Method for training the model
def train_model(data_frame):
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import SGDClassifier
    from sklearn.metrics import classification_report
    import joblib

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
    y_features = data_frame["label"].map({"buy": 1, "hold": 0, "sell": -1})

    # **Train/test split**
    # test_size: controls how much of the data is used for testing (instead of training)
    # .20 would indicate 20% of data for testing, 80% of data for training
    # random_state: seed number for random shuffling of data before splitting
    # set this to get the same split every time
    x_train, x_test, y_train, y_test = train_test_split(
        x_features, y_features, test_size=0.2, random_state=42
        )
    
    # Random forest classifier (to improve predicition accuracy)
    # Works by training multiple decision trees on random subsets of features listed above
    if not os.path.exists(trained_model_name):
        model = SGDClassifier(loss="log_loss", random_state=32)
        model.partial_fit(x_train, y_train, classes=[1,0,-1])
    else:
        model = joblib.load(trained_model_name)
        model.partial_fit(x_features, y_features)

    # Generate predictions from a trained machine model
    y_pred = model.predict(x_test)
    print(classification_report(y_test, y_pred, zero_division=0))

    # Save model, print success message 
    joblib.dump(model, trained_model_name)
    print(fr"Model trained on {entries_num} entries, saved as {trained_model_name}")

# Main method for calling helper functions to train the model
def train_main():
    data = load_all_json()
    if data != -1:
        processed_entries = convert_headlines(data)
        labeled_entries = label_entries(processed_entries)
        data_frame = pd.json_normalize(labeled_entries)

        data_frame["headline_sentiment.headline_1"] = data_frame["headline_sentiment.headline_1"].map({"positive": 1, "neutral": 0, "negative": -1})
        data_frame["headline_sentiment.headline_2"] = data_frame["headline_sentiment.headline_2"].map({"positive": 1, "neutral": 0, "negative": -1})

        train_model(data_frame)

if __name__ == "__main__":
    train_main()