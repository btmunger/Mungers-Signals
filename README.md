# Munger's Signals - Your AI Day Trading Buddy!
## Written by Brian Munger, 2025

### What is Munger's Signals?
Munger's Signals is a personal project that combines Selenium, AI, and Python to deliver advice regarding the stock market. It is designed with short to medium length trading in mind, giving you the indicator to buy, sell, or hold your requested stock. 

### How do I download and use it?

### How does it work?
There are two different modes of operation: analysis and training.
1. When in analysis mode, the user can enter any valid stock code that they would like analyzed (stock code lookup: https://stockanalysis.com/symbol-lookup/). Once entered, the Selenium WebDriver is initialized, and scrapes Yahoo Finance's webpage for data regarding that stock from the last month. Some of the statistics gathered are moving averages, average closing and opening numbers, and even news stories. Once this information is collected, trends are calculated and sent to the AI models. One AI model, ProsusAI/finbert, is imported and used to perform "sentiment analysis" on the news stories, returning a positive, negative, or neutral reading. For example, if a news story reads "[stock code] expected to smash earnings predictions", the sentiment AI will return positive. The other model is custom and trained by me (and you! If you select the next option...)! It takes the previously generated trend report with the updated news sentiment analysis, and based on this data, gives you advice on whether you should buy, sell, or hold the stock.
2. When in training mode, you get to train our custom AI model! The program loads in stock codes from a predefined list titled "train_stock_list.csv" (feel free to add or remove stocks from this list!). Then again, using Selenium Webdriver, the program generates trend reports for each stock, which are in the same format as those generated in option one. Once completed, all of the news stories have their sentiment assigned to them. Then, each trend report is auto-labeled with buy, sell, or hold by an algorithm that compares the trend statistics to predetermined metrics. These trend reports with their labels are fed to the custom model to train it, and the results of the training are saved to the logging directory.

Besides that, PySide6 (https://pypi.org/project/PySide6/) is used to run the graphical user interface.
