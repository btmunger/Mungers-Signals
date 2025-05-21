from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import csv

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--ignore-certificate-errors")

service = Service(r"C:\Users\btmun\OneDrive\Desktop\StockChecker\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

NVDU_SHARES = 2.01
WBD_SHARES = 5

start_date = datetime.strptime("2025-05-19", "%Y-%m-%d")
today = datetime.today()
days_ran = datetime.strptime(today.strftime("%Y-%m-%d"), "%Y-%m-%d")
delta = days_ran - start_date
days_passed = delta.days

def get_NVDU_range(): 
    driver.get("https://beta.finance.yahoo.com/quote/NVDU/")

    nvdu_range_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "fin-streamer[data-field='regularMarketDayRange']"))
    )

    nvdu_range = nvdu_range_element.text
    parts = nvdu_range.split(" - ")
    global nvdu_low
    global nvdu_high
    nvdu_low = float(parts[0])
    nvdu_high = float(parts[1])

def get_WBD_range():
    driver.get("https://beta.finance.yahoo.com/quote/WBD/")

    wbd_range_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "fin-streamer[data-field='regularMarketDayRange']"))
    )

    wbd_range = wbd_range_element.text
    parts = wbd_range.split(" - ")

    global wbd_low
    global wbd_high
    wbd_low = float(parts[0])
    wbd_high = float(parts[1])


def write_csv():
    global nvdu_high
    global nvdu_low
    global wbd_high
    global wbd_low

    data = [
        [days_passed, nvdu_high, nvdu_low, wbd_high, wbd_low]
    ]

    with open("stock_prices.csv", mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(data)

get_NVDU_range()
get_WBD_range()
write_csv()

driver.quit()