import csv
import sys
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
        prev = data[index - 1]
        curr = data[index]
        change = (curr - prev) / prev * 100
        percent_changes_sum += change

    return percent_changes_sum / len(data)

# Method to find the range between a open/close or high/low
def get_range(x, y, open):
    return (x - y) / open * 100

# Method for calculating the moving average of a particular stock
# Logic credit: https://www.geeksforgeeks.org/how-to-calculate-moving-averages-in-python/
def get_moving_average(data, window):
    moving_averages = []

    for index in range(len(data)):
        if index + 1 < window:
            moving_averages.append(None)
        else:
            window_average = sum(data[index + 1 - window : index + 1])
            moving_averages.append(window_average)
    
    return moving_averages

# Method for calculating the standard deviation of certain arrays
# Logic credit: https://www.geeksforgeeks.org/how-to-calculate-moving-averages-in-python/
def get_std(data, window):
    stds = []
    for index in range(len(data)):
        if index + 1 < window:
            stds.append(None)
        else:
            window_slice = data[index + 1 - window : index + 1]
            std = statistics.stdev(window_slice)
            stds.append(std)

    return stds

# Method for calculating the zscores
def get_zscore(price, ma, std):
    return (price - ma) / std

# Method for calculating trends based on the organized statistics 
def calculate_trends(stock_statistics):
    # Stats array format:
    # stock_statistics = [week_open, week_high, week_low, week_close, week_volume,       0-4
    #              month_open, month_high, month_low, month_close, month_volume]   5-9

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
    opn_clse_range_wk = get_range(pcnt_chng_close_wk, pcnt_chng_open_wk, pcnt_chng_open_wk)
    opn_clse_range_mnth = get_range(pcnt_chng_close_mnth, pcnt_chng_open_mnth, pcnt_chng_open_mnth)
    high_low_range_wk = get_range(get_percent_change(stock_statistics[1]), get_percent_change(stock_statistics[2]), 
                                  pcnt_chng_open_wk)
    high_low_range_mnth = get_range(get_percent_change(stock_statistics[1]), get_percent_change(stock_statistics[2]), 
                                  pcnt_chng_open_mnth)
    range_arr = [opn_clse_range_wk, opn_clse_range_mnth, high_low_range_wk, high_low_range_mnth]

    # Moving average calculations (using closing prices)
    ma_wk = get_moving_average(stock_statistics[3], 5)
    ma_mnth = get_moving_average(stock_statistics[8], 20)
    moving_avg_arr = [ma_wk, ma_mnth, ma_wk - ma_mnth, ma_wk / ma_mnth]

    # STD calculations
    cls_std_wk = get_std(stock_statistics[3], 5)
    cls_std_mnth = get_std(stock_statistics[8], 20)
    zscore_wk = get_zscore(stock_statistics[3][-1], ma_wk, cls_std_wk[-1])
    zscore_mnth = get_zscore(stock_statistics[8][-1], ma_mnth, cls_std_mnth[-1])
    std_array = [cls_std_wk, cls_std_mnth, zscore_wk, zscore_mnth]

    # Format and return the trends report
    trends_report = [pcnt_chng_arr, range_arr, moving_avg_arr, std_array]
    return trends_report

# Method for writing trend reports to a JSON file
def write_trend_json(trend_report):
    return

# Method for writing trend reports to the terminal (only the percentage increases for reference)
def write_terminal_out(stock_code, stats):
    print("====================================================================")
    print(fr"                      Trend report for '{stock_code}'             ")
    print("                                                                    ")
    print("             Trends over the last week | last month:                ")    
    print("====================================================================")
   
# Main function for calculating trends. Calls the appropriate helper functions, prints to the console the report
# Other .py files that need to calculate the trends of a stock should call this function 
def get_trend_report(stock_code, stock_statistics):
    trend_report = calculate_trends(stock_statistics)
    write_trend_json(stock_code, trend_report)
    write_terminal_out(stock_code, trend_report[0])