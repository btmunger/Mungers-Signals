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

# Set up mode from arguments if they exist, otherwise assume mode 0
mode = 0
if (len(sys.argv) > 1):
    mode = sys.argv[1]

# Current shares of desired stocks
stocks = ["NVDU", "WBD"]

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
    service = Service(r"C:\Users\btmun\OneDrive\Desktop\StockData\chromedriver-win64\chromedriver.exe")
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

    file_path = fr"C:\Users\btmun\OneDrive\Desktop\StockData\{stock_code}_prices.csv"

    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

def log_trends():
    # TODO
    return 

# Method to call helper functions to scrape for stock prices
def update_stock_price():
    driver = init_webdriver()

    for i in range(len(stocks)):
        curr_range = get_stock_range(driver, stocks[i])
        low = float(curr_range[0])
        high = float(curr_range[1])
        write_csv(stocks[i], low, high)

    # Cleanup driver
    driver.quit()
        

# Mode 0 = Log daily stock high/low
if (mode == 0):
    # Log the current prices
    update_stock_price()
# Mode 1 = Log trends in data overtime
elif (mode == 1):
    log_trends()