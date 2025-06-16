# A project by Brian Munger

import json
import pandas as pd
from datetime import datetime

# Method to return to retrieve a json file and return the most up to date entry
def load_json(stock_code):
    json_name = fr"trend_reports/{stock_code}_reports.json"

    with open(json_name, "r") as file:
        data = json.load(json_name)
    
    latest_entry = max(data, key=lambda x: datetime.fromisoformat(x["timestamp"]))

    return latest_entry


# Main method for the AI analysis portion of the project
def ai_analysis(stock_code):
    entry = load_json