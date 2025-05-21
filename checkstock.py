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

# Selenium Options, run headless (in background), ignore errors
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--ignore-certificate-errors")

# Chrome web driver set to Selenium Service
service = Service(r"C:\Users\btmun\OneDrive\Desktop\StockData\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# Current shares of desired stocks
NVDU_SHARES = 2.01
WBD_SHARES = 5

# Calculate days since started recording data
start_date = datetime.strptime("2025-05-19", "%Y-%m-%d")
today = datetime.today()
days_ran = datetime.strptime(today.strftime("%Y-%m-%d"), "%Y-%m-%d")
delta = days_ran - start_date
days_passed = delta.days

# Method to get the high/low price of the NVDU stock today
def get_stock_range(stock_code): 
    url = "https://beta.finance.yahoo.com/quote/" + stock_code + "/"
    driver.get(url)

    stock_range_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "fin-streamer[data-field='regularMarketDayRange']"))
    )

    stock_range = stock_range_element.text
    parts = stock_range.split(" - ")

    return parts

# Method for writing report to the CSV 
def write_csv(nvdu_low, nvdu_high, wbd_low, wbd_high):
    data = [
        [days_passed, nvdu_high, nvdu_low, wbd_high, wbd_low]
    ]

    with open("stock_prices.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

# Get the NVDU and WBD prices
nvdu_range = get_stock_range("NVDU")
nvdu_low = float(nvdu_range[0])
nvdu_high = float(nvdu_range[1])
wbd_range = get_stock_range("WBD")
wbd_low = float(wbd_range[0])
wbd_high = float(wbd_range[1])

# Finishing tasks
write_csv(nvdu_low, nvdu_high, wbd_low, wbd_high)
driver.quit()