import csv
import sys
import os 
import numpy as np

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

# Method for calculating trends based on the organized statistics 
def calculate_trends(stock_statistics):
    # Stats array format:
    # stock_data = [week_open, week_high, week_low, week_close, week_volume,       0-4
    #              month_open, month_high, month_low, month_close, month_volume]   5-9

    pcnt_chng_close_wk = get_percent_change(stock_statistics[3])
    pcnt_chng_close_mnth = get_percent_change(stock_statistics[8])
    pcnt_chng_open_wk = get_percent_change(stock_statistics[0])
    pcnt_chng_open_mnth = get_percent_change(stock_statistics[5])
    pcnt_chng_volume_wk = get_percent_change(stock_statistics[4])
    pcnt_chng_volume_mnth = get_percent_change(stock_statistics[9])

    trends_report = [pcnt_chng_close_wk, pcnt_chng_close_mnth, pcnt_chng_open_wk, pcnt_chng_open_mnth,
                     pcnt_chng_volume_wk, pcnt_chng_volume_mnth]
    return trends_report

# Method for writing trend reports to a JSON file
def write_trend_json(trend_report):
    return
   
# Main function for calculating trends. Calls the appropriate helper functions, prints to the console the report
# Other .py files that need to calculate the trends of a stock should call this function 
def get_trend_report(stock_code, stock_statistics):
    trend_report = calculate_trends(stock_statistics)
    write_trend_json(trend_report)

    print("====================================================================")
    print(fr"                      Trend report for '{stock_code}'             ")
    print("                                                                    ")
    print("             Trends over the last week | last month:                ")    
    print("====================================================================")