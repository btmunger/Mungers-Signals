# Munger's Signals - Your AI Day Trading Buddy!
## Written by Brian Munger, 2025

### What is Munger's Signals?
Munger's Signals is a personal project that combines Selenium, AI, and Python to deliver advice regarding the stock market. It is designed with short to medium-term trading in mind, providing you with the indicator to buy, sell, or hold your requested stock. 

### Disclaimer
This project is for recreational and educational purposes only and does not constitute financial advice. The stock market is often unpredictable. Do your own research and consult a qualified financial professional before making investment decisions!

### How do I install and use it?
Please consider these notes before installing the project: 
* *NOTE:* This project has only been tested on Windows 10/11. The use of this program on other operating systems is at your on risk!  
* *NOTE:* Python (version 3.13 or greater) is required to run this project; you can install the latest version [here](https://www.python.org/downloads/)! Chrome is also required to run this project; you can install the latest version [here](https://www.google.com/chrome/dr/download/?brand=CHBD&ds_kid=43700082450527897&gclsrc=aw.ds&gad_source=1&gad_campaignid=22852336242&gbraid=0AAAAAoY3CA6-NnGc4wtcEMCDSjo5gQEA-&gclid=Cj0KCQjwqebEBhD9ARIsAFZMbfx2CiNOpPy9cbfIPeC1Jb3JvN9jo_Yc0-prZY9bK0w04HdgnZ7oGQ4aAiMjEALw_wcB).    
* *NOTE:* Upon first run, the program may take a moment to open, as the graphical user interface library may need to be installed.  

To download this project, navigate to the "releases" tab on the right side of this GitHub repository. Located at the bottom of the latest release, download the source code in the zip format. Once downloaded, extract the folder, and run the MungersSignals application (.exe) file. If any required packages are missing, the program will automatically install them. 

Alternatively, feel free to 'git clone' this repository into your workstation! "python ./bootstrap.py" runs the program in the same way the .exe file runs it. If you are encountering any issues with the program, it may be a good idea to run it via the terminal with this command to see if any errors are thrown.  

More detailed installation instructions are located in /docs/INSTALLATION_GUIDE.md.  * 

### How does it work?
There are two different modes of operation: analysis and training.
1. When in analysis mode, the user can enter any valid stock code that they would like analyzed ([stock code lookup](https://stockanalysis.com/symbol-lookup/)). Once entered, the Selenium WebDriver is initialized and scrapes Yahoo Finance's webpage for data regarding that stock from the last month. Some of the statistics gathered are moving averages, average closing and opening numbers, and even news stories. Once this information is collected, trends are calculated and sent to the AI models. One AI model, ProsusAI/finbert, is imported and used to perform "sentiment analysis" on the news stories, returning a positive, negative, or neutral reading. For example, if a news story reads "[stock code] expected to smash earnings predictions", the sentiment AI will return positive. The other model (written by scikit-learn) is custom and trained by me (and you! If you select the next option...)! It takes the previously generated trend report with the updated news sentiment analysis, and based on this data, gives you advice on whether you should buy, sell, or hold the stock.
2. When in training mode, you get to train our custom AI model! The program loads in stock codes from a predefined list titled "train_stock_list.csv" (feel free to add or remove stocks from this list!). Then again, using Selenium Webdriver, the program generates trend reports for each stock, which are in the same format as those generated in option one. Once completed, all of the news stories have their sentiment assigned to them. Then, each trend report is auto-labeled with buy, sell, or hold by an algorithm that compares the trend statistics to predetermined metrics. These trend reports with their labels are fed to the custom model to train it, and the results of the training are saved to the logging directory.

Besides that, PySide6 is used to run the graphical user interface.

### References
Thank you to all of the resources that made this project possible! 
- [Yahoo Finance](https://finance.yahoo.com/) 
- [Google Chrome](https://www.google.com/chrome/dr/download/)
- [Selenium WebDriver](https://www.selenium.dev/documentation/webdriver/)
- [ProsusAI/finbert](https://huggingface.co/ProsusAI/finbert)
- [scikit-learn](https://scikit-learn.org/stable/)
- [PySide6](https://pypi.org/project/PySide6/)

##### Additional documentation is located in the /docs directory. 
