# File Structure and Description

docs/
&nbsp;&nbsp;&nbsp;&nbsp;|---COMMON_ERRORS.md
&nbsp;&nbsp;&nbsp;&nbsp;|---FILE_STRUCTURE.md
&nbsp;&nbsp;&nbsp;&nbsp;|---INSTALLATION_GUIDE.md
gui/
&nbsp;&nbsp;&nbsp;&nbsp;|---/icon
&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---icon.rc
&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---icon.res
&nbsp;&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;|---logo.ico
&nbsp;&nbsp;&nbsp;&nbsp;|---analysis_gui.py
&nbsp;&nbsp;&nbsp;&nbsp;|---install_gui.py
&nbsp;&nbsp;&nbsp;&nbsp;|---main_gui.py
&nbsp;&nbsp;&nbsp;&nbsp;|---train_gui.py
/train_log
/trend_reports
.gitignore
ai_analysis.py
ai_train.py
bootstrap.py
install_libraries.py
logic.py
MungersSignals.exe
README.md
train_stock_list.csv
trained_stock_model.pkl
trends.py
wrapper.c

#### Directories
* docs/ is the directory this file is in and contains documentation for this project (besides README).
* gui/ directory holds all of the files required to run the graphical user interface via PySide6. It also incorporates some of the logic for this project, utilizing "[QtThreads](https://doc.qt.io/archives/qt-5.15/thread-basics.html)" and "[Signals](https://doc.qt.io/qt-6/signalsandslots.html)" for logic timing. 
* train_log/ is the directory where logs are saved after each training of the AI model. The logs contain specific information about what information the model was trained on, and what the results were. 

#### Files
* ai_analysis.py is called when the first option, "AI Buy/Sell/Hold," is selected. It contains the main logic for asking the AI model if the user should buy/sell/hold a particular stock based on its newly generated trend report.
* ai_train.py is called when the second option, "Train AI Model," is selected. It contains the main logic for gathering all of the generated trend reports, auto labeling them based on predefined metrics, and sending them to the AI model to train.
* bootstrap.py is the first file called every time the program is ran. It simply ensures the required libraries are downloaded, redirects to install_libraries if this is not the case, and redirects to logic.py. It is worth noting that this file installs PySide6 if it is not previously installed, so that during the installation of the rest of the files, there is some GUI output. 
* install_libraries.py installs the required Python libraries if they are found missing, as the name suggests.
* logic.py is the main file of the project. This file calls the GUI files as needed, and handles the Selenium Webdriver logic for retreiving stock data.
* MungersSignals.exe is the executable file for this project. More information regarding this file and running the project as a whole are located in docs/INSTALLATION_GUIDE.md. 
* README.md contains important information regarding the project. 
* train_stock_list.csv contains all of the stock codes that are used to train the AI model. Feel free to delete or add stock codes to this list as you see fit!
* trained_stock_model.pkl is the main component of this project. It is our trainable AI model that is useed to give stock predictions to the user.
* trends.py calculates trend reports for different stocks codes. This file is utilized in both the analysis and training mode.
* wrapper.c is a small C algorithm I use to make the executable file. Feel free to check it out, although it is not used during program execution. 