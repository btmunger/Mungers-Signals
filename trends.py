import csv
import sys
import os 

# Working directory for file paths
current_directory = os.getcwd()

def calculate_trends(stock_code): 
    file_path = fr"{current_directory}\stock_reports\{stock_code}_prices.csv"

    with open(file_path, mode="r") as file:
        reader = csv.reader(file)

        high_prices = []
        low_prices = []
        title_line = next(reader)

        for index in range(30):
            curr_line = next(reader)

            if curr_line[0] != index + 1:
                continue
 
            high_prices.append(curr_line[1])
            low_prices.append(curr_line[2])

    return report
