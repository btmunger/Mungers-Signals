# A project by Brian Munger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import csv
import sys
import os

# Working directory for file paths
base_dir = os.path.dirname(os.path.abspath(__file__))
stock_list_dir = os.path.join(base_dir, "stock_list.csv")

# Set up mode from arguments if they exist, otherwise assume mode 0
mode = 1
if (len(sys.argv) > 1):
    mode = 0

# Calculate days since started recording data
start_date = datetime.strptime("2025-06-02", "%Y-%m-%d")
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
    options.add_argument('--log-level=3') 

    # Chrome web driver set to Selenium Service
    path = fr"{base_dir}\chromedriver-win64\chromedriver.exe"
    service = Service(path)
    driver = webdriver.Chrome(service=service, options=options)

    return driver

# Method to get the high/low price of the NVDU stock today
def get_stock_data(driver, stock_code): 
    print("\n" + fr"Scraping Yahoo Finance for {stock_code} day high and low share cost..." + "\n")

    # Navigate to Yahoo Finance to get price
    url = "https://beta.finance.yahoo.com/quote/" + stock_code + "/"
    driver.get(url)

    # Select the element with the market day range text
    stock_range_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "fin-streamer[data-field='regularMarketDayRange']"))
    )

    # Get the text from the element, split the text by the '-' character
    stock_range = stock_range_element.text
    parts = stock_range.split(" - ")
    low = float(parts[0])
    high = float(parts[1])

    # Select the element with the closing value
    closing_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "fin-streamer[data-testid='qsp-price']"))
    )
    closing = float(closing_element.text)

    # Select the element with the market volume
    volume_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "fin-streamer[data-field='regularMarketVolume']"))
    )
    volume_text_comma = volume_element.text
    volume = float(volume_text_comma.replace(",", ""))

    # Return array with today's stock data
    todays_stock_data = [high, low, closing, volume]
    return todays_stock_data

# Method for writing report to the CSV 
def write_csv(stock_code, todays_stock_data):
    data = [
        [days_passed, todays_stock_data[0], todays_stock_data[1], 
         todays_stock_data[2], todays_stock_data[3]]
    ]

    file_path = fr"{base_dir}\stock_reports\{stock_code}_prices.csv"

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

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

    # For each stock, find the daily range, and write to CSV
    for i in range(len(stocks)):
        todays_stock_data = get_stock_data(driver, stocks[i])
        write_csv(stocks[i], todays_stock_data)
    
    # Cleanup driver
    driver.quit()

    print("\nDone!\n")
    # If not in regular schedule mode, display the options to user
    if mode != 0:
        display_options()


# Method to display stock adding options to the user
def prompt_add_stock():
    print("\n")
    print("====================================================================")
    print("         Enter the stock code you want to add to be tracked         ")
    print("         For example, NVDA for Nividia, WBD for Warner Bros         ")
    print("         Reference list: https://stockanalysis.com/stocks/          ")
    print("                                                                    ")
    print("              Enter '1' to display the current list                 ")
    print("====================================================================")

    add_stock()
    display_options()

# Method for providing the user with a list of the currently tracked stocks
def display_tracked_stocks():
    stocks = gather_stock_list()
    index = 1

    # Print each stock to the console
    print("\nList of currently tracked stocks:")
    for stock in stocks:
        if index == len(stocks):
            print(stock, end="\n\n")
        else:
            print(stock, end=",")
            index += 1

# Method for adding stocks to be tracked 
def add_stock():
    # No stock code is just 'Y' ;)
    stock_code = input("Enter the stock code or enter '1': ")

    if len(stock_code) < 1 or len(stock_code) > 5:
        print("Invalid stock code length. Enter again\n")
        add_stock()

    # Redirect to display stocks function if 'y' is entered
    if stock_code == '1':
        display_tracked_stocks()
    else:   
        # Append the stock code to the list, then write to CSV
        stocks = gather_stock_list()
        stocks.append(stock_code.upper())

        with open(stock_list_dir, mode="w") as file:
            writer = csv.writer(file)
            writer.writerow(stocks)

        print("\n"  + fr"Successfully added '{stock_code.upper()}' stock to list!")
        print("\n")
    
# Method to display options to the user 
def display_options():
    print("====================================================================")
    print("                Welcome to Munger's Stock Tracker!                  ")
    print("                  Written by Brian Munger, 2025                     ")     
    print("                                                                    ")            
    print("                Options (type the corresponding #):                 ")
    print("                   1. Log daily stock high/low                      ")
    print("                   2. Add to / view tracked stocks                  ")  
    print("                   3. Depict trends in stock data                   ")                               
    print("                   4. Exit                                          ")     
    print("====================================================================")

    # Gather user input for their mode choice
    gather_mode_input()

# Method to gather user input for the mode they want
def gather_mode_input():
    input_choice = input("Select an option 1-4: ")
    if input_choice == "1":
        print("\nLogging daily stock high/low...")
        update_stock_price()
    elif input_choice == "2":
        prompt_add_stock()
    elif input_choice == "3":
        print("Not implemented yet\n") # IMPLEMENT 
        gather_mode_input()
    elif input_choice == "4":
        print("\nGoodbye!\n")
    # Invalid choice, prompt again
    else:
        print("Invalid option, please try again.\n")
        gather_mode_input()

print("")

# Mode 1 = Executable mode, prompts options to user
if (mode == 1):
    display_options()
# Mode 0 = Log daily stock high/low
elif (mode == 0):
    update_stock_price()