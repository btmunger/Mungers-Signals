from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox, 
    QLineEdit
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
import ctypes
import time
import sys

# Import functions from stock_tracker.py and ai_analysis.py
from stock_tracker import init_webdriver, get_stock_data_with_retry
from trends import get_trend_report
from ai_analysis import ai_analysis

# Class for running the analysis 
class AnalysisLogic(QThread):
    update_loading = Signal()

    # Create the thread while saving the stock_code
    def __init__(self, stock_code):
        super().__init__()
        self.stock_code = stock_code
    
    # Method for calling the necessary functions for getting AI analysis
    def run(self):
        # Method for calling the necessary functions for gathering the AI analysis
        driver = init_webdriver()
        stock_data = get_stock_data_with_retry(driver, self.stock_code, 1)

        # Do not attempt if no stock data is returned
        if stock_data != None:
            # Redirects to trends.py, then ai_analysis.py
            get_trend_report(self.stock_code, stock_data)
            decision = ai_analysis(self.stock_code)
        
        driver.quit()

# Class for GUI analysis window (option 1)
class AnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window / taskbar icon 
        myappid = u'arbitrary string in unicode' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowIcon(QIcon("gui/icon/logo.ico"))

        # Window title and inital position / size of GUI
        self.setWindowTitle("Munger's Stock Advisor")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # GUI window title / subtitle 
        self.status_label = QLabel()
        self.status_label = QLabel()
        self.status_label.setText(
            "<div style='font-size:20px; font-weight:bold; line-height:1.0;'>"
            "AI Analysis"
            "</div>"
            "<div style='font-size:16px; color:gray; line-height:1.0;'>"
            "Enter the stock code you would like analyzed"
            "</div>"
        )
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        layout.addSpacing(100)

        # Enter stock code text box widget
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("e.g. NVDA")
        self.input_box.setFixedWidth(200)
        self.input_box.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.input_box, alignment=Qt.AlignCenter)

        # Analyze button
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.get_stock_code)
        layout.addWidget(self.analyze_button, alignment=Qt.AlignCenter)
        layout.addSpacing(20)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def get_stock_code(self):
        stock_code = self.input_box.text().strip().upper()

        if not stock_code or len(stock_code) > 5:
            QMessageBox.warning(self, "Input Error", "Please enter a valid stock code.")
            return
        
        self.analyze_button.setEnabled(False)

        # Create and start thread 
        self.thread = AnalysisLogic(stock_code)
        self.thread.update_loading.connect(self.update_status)
        self.thread.finished_analysis.connect(self.analysis_complete)
        self.thread.start()

# Function for managing the first option
def manage_option_one():
    window = AnalysisWindow()
    window.show()
    return window