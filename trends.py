import csv
import sys
import os 

# Working directory for file paths
current_directory = os.getcwd()

def get_trend_slope(data):


def calculate_trends(stock_code): 
    file_path = fr"{current_directory}\stock_reports\{stock_code}_prices.csv"

    week_high = 0, week_low = 0
    month_high = 0, month_low = 0
    week_closing = 0, month_closing = 0

    with open(file_path, mode="r") as file:
        reader = csv.reader(file)

        logs = file.readlines()
        logs_count = -1
        for log in reversed(logs):
            if logs_count == -1:
                logs[0]

            if logs_count >= 7:
                week_high += logs[1]
                week_low += logs[2]
                week_closing += logs[3]
            if logs_count >= 30:
                month_high += logs[1]
                month_low += logs[2]
                month_closing += logs[3]


    trend_report = [get_trend_slope(week_high), get_trend_slope(week_low), get_trend_slope(week_closing),
                    get_trend_slope(month_high), get_trend_slope(month_low), get_trend_slope(month_closing)]
    return trend_report
              
def get_trend_report(stock_code):
    trend_report = calculate_trends(stock_code)
    write_trend_CSV(trend_report)

    # print statements
