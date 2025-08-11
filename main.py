# A project by Brian Munger
from install_libraries import install_libs
try:
    from gui.main_gui import run_main_window
except ModuleNotFoundError:
    print("\nFirst time running, installing required libraries...\n")
    install_libs()
    from gui.main_gui import run_main_window

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
    
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import sys
from sys import platform
import csv
import os
import time
import urllib3

from PySide6.QtWidgets import QApplication

# Retrieve operating sys specific path
def path_from_os():
    # Linux or Mac
    if platform == "linux" or platform == "linux2" or platform == "darwin":     
        return "/dev/null"
    # Windows
    elif platform == "win32":
        return "NUL"
    # Not recognized -> default Windows
    else:
        print("\nCould not determine operating system. Using default option of Windows.")
        return "NUL"

# Method for setting up the Selenium Webdriver 
def init_webdriver(): 
    # Selenium Options, run headless (in background), ignore errors
    options = Options()
    options.add_argument("--headless")          # Comment the next two arguments to have the webdriver run on your screen
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_experimental_option(
        "prefs", {
            # Block image loading
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
    log_path = path_from_os() # send logs to different places (dev/null or NUL) depending on os type
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
        # No news headlines exist in the website's HTML
        return None

# Method to get news headlines regarding a certain stoc
def get_stock_news(driver, stock_code):
    #Initalize driver, navigate to Yahoo Finance to get headlines
    url = "https://beta.finance.yahoo.com/quote/" + stock_code + "/"
    driver.get(url)

    news_headline = []
    wait = WebDriverWait(driver, 10)

    # Use helper function to grab a list of the story items for a stock, loop through them
    story_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='storyitem']")))
    for story_item in story_items:  
        # Grab the elements of the current news headline. Sometimes, the headlines have a different HTML structure
        story_item_children = story_item.find_elements(By.XPATH, "./*")
        if len(story_item_children) < 2:
            try:
                story_item_children = story_item.find_element(By.XPATH, "./*") 
                story_item_children_div = story_item_children.find_elements(By.XPATH, "./*")
                if story_item_children_div:
                    news_headline.append(story_item_children_div[0].text)

                continue
            except Exception as ex:
                print(f"Issue with news HTML elements: {ex}\nSkipping current story...")
                continue

        story_item_elements = story_item_children[1].find_elements(By.XPATH, "./*")
        if story_item_elements:
            news_headline.append(story_item_elements[0].text)

    #print(news_headline) 
    return news_headline

# Method to attempt to fix connection error
# Reference for the urllib3 library: https://urllib3.readthedocs.io/en/1.26.9/reference/urllib3.exceptions.html
def get_stock_data_with_retry(driver, stock_code):
    retries = 3

    for attempt in range(retries):
        try:
            return get_stock_data(driver, stock_code)
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
def get_stock_data(driver, stock_code):
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
        print(f"\nERROR: An error occured while generating a trend report for '{stock_code}'. Skipping for now...\n")
        return None

    # Read stock data entries from the last month 
    days_num = 0
    entry_num = 0

    # Try / except used as there will be an element error if the stock code requested does not exist
    try:
        curr_entry = data_entries[entry_num].find_elements(By.XPATH, "./*") 
    
        # Save the last 20 entries
        while days_num < 20:
            curr_entry = data_entries[entry_num].find_elements(By.XPATH, "./*") 
            #print(curr_entry[0].text)

            # Do not save entries that contain dividends or splits
            if "Split" in curr_entry[1].text or "Dividend" in curr_entry[1].text:
                entry_num += 1
                continue 
            else: 
                # For last week statistics
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
                entry_num += 1

        news_headline = get_stock_news(driver, stock_code)

        # Organize data, return stats report
        stock_data = [week_open, week_high, week_low, week_close, week_volume,
                    month_open, month_high, month_low, month_close, month_volume,
                    news_headline]
        return stock_data
    # No stock with the provided code exists
    except IndexError:
        print(f"\nERROR: Stock code '{stock_code}' not found in Yahoo Finance's Database (or some other error occured).\n")
        return None
    
# Method for loading the saved stock codes from the .csv file
def load_stock_list():
    with open("train_stock_list.csv", "r") as file:
        reader = csv.reader(file)
        stock_list = next(reader)
        #print(stock_list)

    return stock_list

# Method for removing prevously generated trend reports
def rm_reports():
    # Create directory if this is first time running
    if not os.path.isdir("trend_reports/"):
        os.mkdir("trend_reports/")

    # Loop through and remove existing reports
    for item_name in os.listdir("trend_reports/"):
        item_path = os.path.join("trend_reports/", item_name)
        os.remove(item_path)

# Method to display options to the terminal 
def display_option_terminal(option):
    print("====================================================================")
    print("                   Welcome to Munger's Signals!                     ")
    print("                  Written by Brian Munger, 2025                     ")     
    print("                                                                    ")            
    print("                           Options:                                 ")
    print("                   1. AI Buy / Sell / Hold                          ")
    print("                   2. Train AI Model                                ")                               
    print(f"\n                      Option selected: {option}                  ")     
    print("====================================================================")

# Method for running the different GUI windows
def run_gui(app):
    # Start main window
    main_window = run_main_window()
    app.exec()
    option = main_window.option_selected
    display_option_terminal(option)

    # Option 1 -> AI recommendation 
    if option == 1:
        from gui.analysis_gui import manage_option_one
        window = manage_option_one()
        window.show()
        app.exec()
        run_gui(app)
    # Option 2 -> Train AI
    elif option == 2:
        from gui.train_gui import manage_option_two
        window = manage_option_two()
        window.show()
        app.exec()
        run_gui(app)
    elif option == -1:
        print("\nUser closed the application. Bye!\n")

# Call main function
if __name__ == "__main__":
    print("")
    # Start GUI
    app = QApplication(sys.argv)
    run_gui(app)