# A project by Brian Munger

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from sys import platform
import os
import csv
import time
import urllib3

from trends import get_trend_report
from ai_analysis import ai_analysis
from ai_train import train_main

# Retrieve operating sys specific path
def path_from_os():
    if platform == "linux" or platform == "linux2" or platform == "darwin":
        return "/dev/null"
    elif platform == "win32":
        return "NUL"
    else:
        print("\nCould not determine operating system. Using default option of Windows.")
        return "NUL"

# Method for setting up the Selenium Webdriver 
def init_webdriver(): 
    # Selenium Options, run headless (in background), ignore errors
    options = Options()
    #options.add_argument("--headless")
    #options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_experimental_option(
        "prefs", {
            # block image loading
            "profile.managed_default_content_settings.images": 2,
        }
    )

    # Make Selenium less detectable as bot activity
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Disable Chronium/Selenium log messages
    options.add_argument("--ignore-certificate-errors")
    options.add_argument('--log-level=3') 
    options.add_argument("--disable-logging")  
    options.add_argument("--disable-speech-api")  
    options.add_argument("--disable-features=MediaSessionService,SpeechRecognition")  

    # Chrome web driver set to Selenium Service
    log_path = path_from_os() # send logs to different places depending on os type
    service = Service(log_path = log_path) 
    driver = webdriver.Chrome(service=service, options=options)

    return driver

# Method for grabbing the data entries table HTML element
def get_Yahoo_data_entries(driver):
    # "./*" = get the child element(s)
    try:
        table = driver.find_element(By.CSS_SELECTOR, "[data-testid='history-table']")
        table_children = table.find_elements(By.XPATH,"./*")
        table_container = table_children[2].find_element(By.XPATH,"./*")

        data_entries_container = table_container.find_elements(By.XPATH,"./*")
        data_entries = data_entries_container[1].find_elements(By.XPATH,"./*")

        return data_entries
    except:
        return None

# Method to get news headlines regarding a certain stoc
def get_stock_news(driver, stock_code):
    #Initalize driver, navigate to Yahoo Finance to get headlines
    url = "https://beta.finance.yahoo.com/quote/" + stock_code + "/"
    driver.get(url)

    news_headline = []
    wait = WebDriverWait(driver, 10)
    story_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='storyitem']")))

    for story_item in story_items:
        try: 
            story_item_children = story_item.find_elements(By.XPATH, "./*")
            if len(story_item_children) < 2:
                continue

            story_item_elements = story_item_children[1].find_elements(By.XPATH, "./*")
            if story_item_elements:
                news_headline.append(story_item_elements[0].text)
        except:
            driver.quit()
            driver = init_webdriver()
            driver.get(url)
            time.sleep(3)

            continue

    #print(news_headline) 
    return news_headline

# Method to attempt to fix connection error
# Reference for the urllib3 library: https://urllib3.readthedocs.io/en/1.26.9/reference/urllib3.exceptions.html
def get_stock_data_with_retry(driver, stock_code, mode):
    retries = 3

    for attempt in range(retries):
        try:
            return get_stock_data(driver, stock_code, mode)
        # Print protocol error, small wait before retrying
        except urllib3.exceptions.ProtocolError as e:
            print(f"ProtocolError on attempt {attempt+1}: {e}")
            time.sleep(4)  
        # Print connection reset error, small wait before retrying
        except ConnectionResetError as e:
            print(f"Connection reset on attempt {attempt+1}: {e}")
            time.sleep(4)
    # If allowed retries is exceeded, print error message
    print(f"Failed to get data for {stock_code} after {retries} attempts.")
    return None

# Method to get stock data over the past month for close, high, low, 
def get_stock_data(driver, stock_code, mode):
    # Initalize driver, navigate to Yahoo Finance to get price data
    print("\n" + fr"Scraping Yahoo Finance for {stock_code} stock data...")
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
    if data_entries == None:
        print(f"\nERROR: Stock code '{stock_code}' not found in Yahoo Finance's Database." + 
                " Enter a valid stock code and try again.\n")
        return None

    # Read stock data entries from the last month 
    days_num = 0
    entry_num = 0

    try:
        curr_entry = data_entries[entry_num].find_elements(By.XPATH, "./*") 
    
        while days_num < 20:
            curr_entry = data_entries[entry_num].find_elements(By.XPATH, "./*") 
            #print(curr_entry[0].text)

            # For last week statistics
            try:
                if days_num < 5:
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

                days_num += 1
            except IndexError:
                pass

            entry_num += 1

        week_open = [p for p in week_open if "Dividend" not in p]
        month_open = [p for p in month_open if "Dividend" not in p]

        news_headline = get_stock_news(driver, stock_code)

        # Organize data, return stats report
        stock_data = [week_open, week_high, week_low, week_close, week_volume,
                    month_open, month_high, month_low, month_close, month_volume,
                    news_headline]
        return stock_data
    except IndexError:
        if mode == 1:
            print(f"\nERROR: Stock code '{stock_code}' not found in Yahoo Finance's Database." + 
                    " Enter a valid stock code and try again.\n")
            display_options()
        elif mode == 2:
            print(f"\nERROR: Stock code '{stock_code}' not found in Yahoo Finance's Database." + 
                    " Skipping for now...\n")
            return None

# Method for getting the desired stock code to check from user
def get_stock_code():
    stock_code = input("\nEnter the stock code you would like analyzed: ")

    # Ensure code with correct length is entered
    if len(stock_code) < 1 or len(stock_code) > 5:
        print("\nInvalid stock code entered. Please enter a valid stock code.")
        return get_stock_code()
    else: 
        return stock_code
    
# Method for loading the saved stock codes from the .csv file
def load_stock_list():
    with open("train_stock_list.csv", "r") as file:
        reader = csv.reader(file)
        stock_list = next(reader)
        #print(stock_list)

    return stock_list
    
# Method for calling the necessary functions for getting the stock analysis 
def manage_option_one():
    stock_code = get_stock_code()
    driver = init_webdriver()
    stock_data = get_stock_data_with_retry(driver, stock_code, 1)

    if stock_data != None:
        get_trend_report(stock_code, stock_data)
        ai_analysis(stock_code)
    
    driver.quit()
    display_options()

# Method for calling the necessary functions for training the AI model
def train_AI():
    stock_list = load_stock_list()
    driver = init_webdriver()

    # For each stock code specified in the CSV file...
    for stock_code in stock_list:
        stock_data = get_stock_data_with_retry(driver, stock_code, 2)
        if stock_data != None:
            get_trend_report(stock_code, stock_data)

    #train_main()

    driver.quit()
    display_options()
    
# Method to display options to the user 
def display_options():
    print("====================================================================")
    print("                Welcome to Munger's Stock Advisor!                  ")
    print("                  Written by Brian Munger, 2025                     ")     
    print("                                                                    ")            
    print("                Options (type the corresponding #):                 ")
    print("                   1. AI Buy / Sell / Hold                          ")
    print("                   2. Train AI Model                                ")                               
    print("                   3. Exit                                          ")     
    print("====================================================================")

    # Gather user input for their mode choice
    gather_mode_input()

# Method to gather user input for the mode they want
def gather_mode_input():
    input_choice = input("Select an option 1-3: ")
    if input_choice == "1":
        manage_option_one()
    elif input_choice == "2":
        train_AI()
    elif input_choice == "3":
        print("\nGoodbye!\n")
    else:
        # Invalid choice, prompt again
        print("Invalid option, please try again.\n")
        gather_mode_input()

if __name__ == "__main__":
    print("")
    display_options()