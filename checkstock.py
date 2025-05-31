# A project by Brian Munger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import csv
import sys
import os

# Working directory for file paths
current_directory = os.getcwd()
stock_list_dir = fr"{current_directory}\stock_list.csv"

# Set up mode from arguments if they exist, otherwise assume mode 0
mode = -1
if (len(sys.argv) > 1):
    mode = sys.argv[1]

# Calculate days since started recording data
start_date = datetime.strptime("2025-05-19", "%Y-%m-%d")
today = datetime.today()
days_ran = datetime.strptime(today.strftime("%Y-%m-%d"), "%Y-%m-%d")
delta = days_ran - start_date
days_passed = delta.days

# Method for setting up the Selenium Webdriver 
def init_webdriver(): 
    # Selenium Options, run headless (in background), ignore errors
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")

    # Chrome web driver set to Selenium Service
    service = Service(r"{current_directory}\chromedriver-win64\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    return driver

# Method to get the high/low price of the NVDU stock today
def get_stock_range(driver, stock_code): 
    url = "https://beta.finance.yahoo.com/quote/" + stock_code + "/"
    driver.get(url)

    stock_range_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "fin-streamer[data-field='regularMarketDayRange']"))
    )

    stock_range = stock_range_element.text
    parts = stock_range.split(" - ")

    return parts

# Method for writing report to the CSV 
def write_csv(stock_code, low, high):
    data = [
        [days_passed, high, low]
    ]

    file_path = fr"{current_directory}\{stock_code}_prices.csv"

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

def log_trends():
    # TODO
    return 

# Set the stock list from the stocks listed in the CSV file
def gather_stock_list():
    with open(stock_list_dir, mode="r", newline="") as file:
        reader = csv.reader(file)
        stocks = next(reader)

    return stocks

# Method to call helper functions to scrape for stock prices
def update_stock_price():
    # Helper functions to gather the stocks list and driver object
    stocks = gather_stock_list()
    driver = init_webdriver()

    for i in range(len(stocks)):
        curr_range = get_stock_range(driver, stocks[i])
        low = float(curr_range[0])
        high = float(curr_range[1])
        write_csv(stocks[i], low, high)

    # Cleanup driver
    driver.quit()

def prompt_add_stock():
    print("\n")
    print("====================================================================")
    print("         Enter the stock code you want to add to be tracked         ")
    print("         For example, NVDA for Nividia, WBD for Warner Bros         ")
    print("         Reference list: https://stockanalysis.com/stocks/          ")
    print("                                                                    ")
    print("              Enter 'y' to display the current list                 ")
    print("====================================================================")

    add_stock()
    display_options()

def display_tracked_stocks():
    stocks = gather_stock_list()
    index = 1

    print("\nList of currently tracked stocks:")

    for stock in stocks:
        if index == len(stocks):
            print(stock, end="\n\n")
        else:
            print(stock, end=",")
            index += 1

def add_stock():
    # No stock code is just 'Y' ;)
    stock_code = input("Enter the stock code or enter 'y': ")

    if len(stock_code) < 1 or len(stock_code) > 5:
        print("Invalid stock code length. Enter again\n")
        add_stock()

    if stock_code == 'y' or stock_code == 'Y':
        display_tracked_stocks()
    else:   
        with open(stock_list_dir, mode="r", newline="") as file:
            reader = csv.reader(file)
            stocks = next(reader)
        
        stocks.append(stock_code.upper())

        with open(stock_list_dir, mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(stocks)

        print("\n")
    
# Method to display options to the user 
def display_options():
    print("====================================================================")
    print("                Welcome to Munger's Stock Tracker!                  ")
    print("                  Written by Brian Munger, 2025                     ")     
    print("                                                                    ")            
    print("                Options (type the corresponding #):                 ")
    print("                   1. Log daily stock high/low                      ")
    print("                   2. Add new stock to track                        ")  
    print("                   3. Depict trends in stock data                   ")                               
    print("                   4. Exit                                          ")     
    print("====================================================================")

    # Gather user input for their mode choice
    gather_mode_input()

# Method to gather user input for the mode they want
def gather_mode_input():
    input_choice = input("Select an option 1-4: ")
    if input_choice == "1":
        print("Logging daily stock high/low...")
        update_stock_price()
    elif input_choice == "2":
        prompt_add_stock()
    elif input_choice == "3":
        print("Not implemented yet\n") # IMPLEMENT 
        gather_mode_input()
    elif input_choice == "4":
        print("Goodbye!\n")
    # Invalid choice, prompt again
    else:
        print("Invalid option, please try again.\n")
        gather_mode_input()

print("")

# Mode -1 = Executable mode, prompts options to user
if (mode == -1):
    display_options()
# Mode 0 = Log daily stock high/low
elif (mode == 0):
    update_stock_price()
# Mode 1 = Log trends in data overtime
elif (mode == 1):
    # IMPLEMENT 
    log_trends()