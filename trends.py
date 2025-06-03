import csv
import sys
import os 
import numpy as np

# Working directory for file paths
current_directory = os.getcwd()

# Set up mode from arguments if they exist, otherwise assume mode 1
mode = 1
if (len(sys.argv) > 1):
    mode = 0

def get_trend_slope(data):
    x = np.arange(len(data))
    y = np.arrange(data)

    slope, intercept = np.polyfit(x, y, 1)

    return slope

def get_rows_len(file_path):
    with open(file_path, 'r', newline='') as file:
        next(file)  # Skip header
        line_count = sum(1 for _ in file)

    return line_count

def calculate_trends(stock_code): 
    file_path = fr"{current_directory}\stock_reports\{stock_code}_prices.csv"

    week_high = 0
    week_low = 0
    month_high = 0
    month_low = 0
    week_closing = 0
    month_closing = 0
    week_volume = 0
    month_volume = 0

    with open(file_path, mode="r") as file:
        reader = csv.reader(file)

        logs = file.readlines()
        logs_count = -1
        index = 0
        for log in reversed(logs):
            if(index < 31):
                if logs_count == -1:
                    logs_count = get_rows_len(logs)

                if logs_count <= 7 and logs_count > 0:
                    week_high += logs[1]
                    week_low += logs[2]
                    week_closing += logs[3]
                    week_volume += logs[4]
                if logs_count >= 30:
                    month_high += logs[1]
                    month_low += logs[2]
                    month_closing += logs[3]
                    month_volume += logs[4]
            else:
                break


    trend_report = [get_trend_slope(week_high), get_trend_slope(week_low), get_trend_slope(week_closing), get_trend_slope(week_volume),
                    get_trend_slope(month_high), get_trend_slope(month_low), get_trend_slope(month_closing), get_trend_slope(month_volume)]
    return trend_report

def write_trend_CSV(trend_report):
    #implement
    return
   
def get_trend_report(stock_code, trend_report):
    trend_report = calculate_trends(stock_code)
    write_trend_CSV(trend_report)

    if mode == 1:
        print("====================================================================")
        print(fr"                      Trend report for '{stock_code}'             ")
        print("                                                                    ")
        print("             Trends over the last week | last month:                ")    
        print(fr"                     Stock high:    {trend_report[0]} | {trend_report[4]}  ")
        print(fr"                     Stock low:     {trend_report[1]} | {trend_report[5]}  ")
        print(fr"                     Stock closing: {trend_report[2]} | {trend_report[6]}  ")
        print(fr"                     Stock closing: {trend_report[3]} | {trend_report[7]}  ")
        print("====================================================================")