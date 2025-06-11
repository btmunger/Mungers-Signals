# A project by Brian Munger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from trends import get_trend_report
from ai_analysis import get_AI_advice
import os

# Working directory for file paths
base_dir = os.path.dirname(os.path.abspath(__file__))

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

# Method for grabbing the data entries table HTML element
def get_Yahoo_data_entries(driver):
    # "./*" = get the child element(s)
    table = driver.find_element(By.CSS_SELECTOR, "[data-testid='history-table']")
    table_children = table.find_elements(By.XPATH,"./*")
    table_container = table_children[2].find_element(By.XPATH,"./*")

    data_entries_container = table_container.find_elements(By.XPATH,"./*")
    data_entries = data_entries_container[1].find_elements(By.XPATH,"./*")

    return data_entries

# Method to get stock data over the past month for close, high, low, 
def get_stock_data(stock_code):
    # Initalize driver, navigate to Yahoo Finance to get price data
    driver = init_webdriver()
    print("\n" + fr"Scraping Yahoo Finance for {stock_code} stock data..." + "\n")
    url = "https://beta.finance.yahoo.com/quote/" + stock_code + "/history/"
    driver.get(url)

    # Declare variables
    week_open = []
    week_high = []
    week_low = []
    week_close = []
    week_volume = []
    month_open = []
    month_high = []
    month_low = []
    month_close = []
    month_volume = []

    # Use helper function to get the table 
    data_entries = get_Yahoo_data_entries(driver)

    # Read stock data entries from the last month 
    for index in range(20):
        curr_entry = data_entries[index].find_elements(By.XPATH, "./*") 
        # For last week statistics
        if index < 5:
            week_open.append(curr_entry[1].text)
            week_high.append(curr_entry[2].text)
            week_low.append(curr_entry[3].text)
            week_close.append(curr_entry[4].text)
            week_volume.append(curr_entry[6].text)

        # For last month statistics
        month_open.append(curr_entry[1].text)
        month_high.append(curr_entry[2].text)
        month_low.append(curr_entry[3].text)
        month_close.append(curr_entry[4].text)
        month_volume.append(curr_entry[6].text)

    # Organize data, return stats report
    stock_data = [week_open, week_high, week_low, week_close, week_volume,
                  month_open, month_high, month_low, month_close, month_volume]
    return stock_data

# Method for getting the desired stock code to check from user
def get_stock_code():
    stock_code = input("\nEnter the stock code you would like analyzed: ")

    # Ensure code with correct length is entered
    if len(stock_code) < 1 or len(stock_code) > 5:
        print("\nInvalid stock code entered. Please enter a valid stock code.")
        get_stock_code()
    else:
        return stock_code
    
# Method to display options to the user 
def display_options():
    print("====================================================================")
    print("                Welcome to Munger's Stock Advisor!                  ")
    print("                  Written by Brian Munger, 2025                     ")     
    print("                                                                    ")            
    print("                Options (type the corresponding #):                 ")
    print("                   1. AI Buy / Sell / Hold                          ")
    print("                   2. Reflect On Past Decisions                     ")                               
    print("                   3. Exit                                          ")     
    print("====================================================================")

    # Gather user input for their mode choice
    gather_mode_input()

# Method to gather user input for the mode they want
def gather_mode_input():
    input_choice = input("Select an option 1-3: ")
    if input_choice == "1":
        stock_code = get_stock_code()
        stock_data = get_stock_data(stock_code)
        get_trend_report(stock_code, stock_data)
    elif input_choice == "2":
        get_stock_data()
    elif input_choice == "3":
        print("\nGoodbye!\n")
    else:
        # Invalid choice, prompt again
        print("Invalid option, please try again.\n")
        gather_mode_input()

print("")
display_options()