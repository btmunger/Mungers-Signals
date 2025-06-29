import json
from datetime import datetime
import os 
import numpy as np
import statistics

# Working directory for file paths
current_directory = os.getcwd()

# Method to get the average percentage change over a data set
def get_percent_change(data):
    percent_changes_sum = 0
    
    # Find the perecent change between each data point
    for index in range(1, len(data)):
        prev = float(data[index - 1].replace(",", ""))
        curr = float(data[index].replace(",", ""))
        change = (curr - prev) / prev * 100
        percent_changes_sum += change

    pct_chng = round(percent_changes_sum / (len(data) - 1), 2)
    return pct_chng

# Method to find the range between a open/close or high/low
def get_range(x, y):
    if float(y) == 0.0:
        raise Exception("Error calculating range of high/low: Divide by 0 error.")
    range_rounded = round((float(x) - float(y)) / float(y), 2)
    return range_rounded

# Helper function for getting the window avg for moving average calculation
def get_window_average(data, window, index):
    window_sum = 0
    for i in range(index + 1 - window, index + 1):
        window_sum += float(data[i].replace(",", ""))

    return window_sum / window

# Method for calculating the moving average of a particular stock
# Logic credit: https://www.geeksforgeeks.org/how-to-calculate-moving-averages-in-python/
def get_moving_average(data, window):
    moving_averages = []

    for index in range(len(data)):
        if index + 1 < window:
            moving_averages.append(None)
        else:
            window_average = get_window_average(data, window, index)
            moving_averages.append(window_average)
            
    ma_round = round(moving_averages[-1], 2)
    return ma_round

# Method for calculating the standard deviation of certain arrays
# Logic credit: https://www.geeksforgeeks.org/how-to-calculate-moving-averages-in-python/
def get_std(data, window):
    stds = []
    for index in range(len(data)):
        if index + 1 < window:
            stds.append(None)
        else:
            window_slice = [float(x.replace(",", "")) for x in data[index + 1 - window : index + 1]]
            std = statistics.stdev(window_slice)
            stds.append(std)

    std_round = round(stds[-1], 2)
    return std_round

# Method for calculating the zscores
def get_zscore(price, ma, std):
    z_score = round((float(price.replace(",", "")) - ma) / 
                    std, 2)
    return z_score

# Method for calculating trends based on the organized statistics 
def calculate_trends(stock_statistics):
    # Stats array format:
    # stock_statistics = [week_open, week_high, week_low, week_close, week_volume,       0-4
    #              month_open, month_high, month_low, month_close, month_volume,         5-9
    #              stock_news]                                                           10

    # Percent change calculations
    pcnt_chng_close_wk = get_percent_change(stock_statistics[3])
    pcnt_chng_close_mnth = get_percent_change(stock_statistics[8])
    pcnt_chng_open_wk = get_percent_change(stock_statistics[0])
    pcnt_chng_open_mnth = get_percent_change(stock_statistics[5])
    pcnt_chng_volume_wk = get_percent_change(stock_statistics[4])
    pcnt_chng_volume_mnth = get_percent_change(stock_statistics[9])
    pcnt_chng_arr = [pcnt_chng_close_wk, pcnt_chng_close_mnth, pcnt_chng_open_wk, pcnt_chng_open_mnth,
                pcnt_chng_volume_wk, pcnt_chng_volume_mnth]

    # Range calculations
    high_low_range_wk = get_range(max(stock_statistics[1]), min(stock_statistics[2]))
    high_low_range_mnth = get_range(max(stock_statistics[6]), min(stock_statistics[7]))
    range_arr = [high_low_range_wk, high_low_range_mnth]

    # Moving average calculations (using closing prices)
    ma_wk = get_moving_average(stock_statistics[3], 5)
    ma_mnth = get_moving_average(stock_statistics[8], 20)
    moving_avg_arr = [round(ma_wk - ma_mnth, 2), round(ma_wk / ma_mnth, 2)]

    # STD calculations
    cls_std_wk = get_std(stock_statistics[3], 5)
    cls_std_mnth = get_std(stock_statistics[8], 20)
    zscore_wk = get_zscore(stock_statistics[3][-1], ma_wk, cls_std_wk)
    zscore_mnth = get_zscore(stock_statistics[8][-1], ma_mnth, cls_std_mnth)
    std_array = [cls_std_wk, cls_std_mnth, zscore_wk, zscore_mnth]

    # Format and return the trends report
    trend_report = [pcnt_chng_arr, range_arr, moving_avg_arr, std_array, stock_statistics[10]]  # stock_statistics[10] = stock news array
    return trend_report

# Method for formatting the trends entry 
def get_entry(stock_code, trend_report):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "stock_code": stock_code,
        "avg_percent_changes": {
            "close_past_week": trend_report[0][0],
            "close_past_month": trend_report[0][1],
            "open_past_week": trend_report[0][2],
            "open_past_month": trend_report[0][3],
            "volume_past_week": trend_report[0][4],
            "volume_past_month": trend_report[0][5]
        },
        "ranges": {
            "high_low_range_week": trend_report[1][0],
            "high_low_range_month": trend_report[1][1]
        },
        "moving_avgs": {
            "sma_difference": trend_report[2][0],
            "sma_ratio": trend_report[2][1]
        },
        "standard_dev_calcs": {
            "closing_std_week": trend_report[3][0],
            "closing_std_month": trend_report[3][1],
            "zscore_week": trend_report[3][2],
            "zscore_month": trend_report[3][3] 
        },
        "stock_news": {
            "headline_1": trend_report[4][0],
            "headline_2": trend_report[4][1]
        }
    }

    return entry

# Method for writing trend reports to a JSON file
def write_trend_json(stock_code, trend_report):
    new_entry = get_entry(stock_code, trend_report)
    json_name = fr"trend_reports/{stock_code}_reports.json"

    # If the trends report directory does not exist, create it
    if not os.path.exists("trend_reports"):
        os.makedirs("trend_reports")

    # If the trends report file does not exist yet for this stock code, create a new 
    # json file
    if not os.path.exists(json_name):
        with open(json_name, "w") as file:
            json.dump([], file)

    entries = []
    with open(json_name, "r") as file:
        entries = json.load(file)

    entries.append(new_entry)

    with open(json_name, "w") as file:
        json.dump(entries, file, indent=4)

# Method for adding a '+' symbol if there is an increasing trend
def add_symbol(pcnt_chng_array):
    stats = []
    for pcnt_chng in pcnt_chng_array:
        if pcnt_chng > 0: stats.append(f"+{pcnt_chng}")
        else: stats.append(pcnt_chng)
        
    return stats
            
# Method for writing trend reports to the terminal (only the percentage increases for reference)
def write_terminal_out(stock_code, trend_report):
    stats = add_symbol(trend_report)

    print("\n====================================================================")
    print(fr"                      Trend report for '{stock_code}'               ")
    print("                                                                      ")
    print("              Trends over the last week | last month:                 ") 
    print(fr"                   Closing:      {stats[0]}% | {stats[1]}%          ")
    print(fr"                   Open:         {stats[2]}% | {stats[3]}%          ") 
    print(fr"                   Volume:       {stats[4]}% | {stats[5]}%          ")
    print("                                                                      ")
    print(fr"       Additional trends written to trend_reports/{stock_code}.json ") 
    print("====================================================================\n")
   
# Main function for calculating trends. Calls the appropriate helper functions, prints to the console the report
# Other .py files that need to calculate the trends of a stock should call this function 
def get_trend_report(stock_code, stock_statistics):
    trend_report = calculate_trends(stock_statistics)
    write_terminal_out(stock_code, trend_report[0])
    write_trend_json(stock_code, trend_report)