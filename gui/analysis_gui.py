from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton, QMessageBox, 
    QLineEdit, QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
import ctypes

# Import functions from stock_tracker.py and ai_analysis.py
from logic import init_webdriver, get_stock_data_with_retry
from trends import get_trend_report
from ai_analysis import ai_analysis

# Class for running the analysis 
class AnalysisLogic(QThread):
    no_stock = Signal()
    ai_deciding = Signal()
    finished_analysis = Signal(str)

    # Create the thread while saving the stock_code
    def __init__(self, stock_code):
        super().__init__()
        self.stock_code = stock_code
    
    # Method for calling the necessary functions for getting AI analysis
    def run(self):
        # Method for calling the necessary functions for gathering the AI analysis
        driver = init_webdriver()
        stock_data = get_stock_data_with_retry(driver, self.stock_code)

        if stock_data == None: 
            self.no_stock.emit()
            return

        # Do not attempt if no stock data is returned
        if stock_data != None:
            # Redirects to trends.py, then ai_analysis.py
            get_trend_report(self.stock_code, stock_data)
            self.ai_deciding.emit()
            decision = ai_analysis(self.stock_code)
        
        driver.quit()
        self.finished_analysis.emit(decision)

# Class for GUI analysis window (option 1)
class AnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window / taskbar icon 
        myappid = u'arbitrary string in unicode' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowIcon(QIcon("gui/icon/logo.ico"))

        # Window title and inital position / size of GUI
        self.setWindowTitle("Munger's Signals")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        # GUI window title / subtitle 
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
        self.layout.addWidget(self.status_label)
        self.layout.addSpacing(20)

        # Enter stock code text box widget
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("e.g. NVDA")
        self.input_box.setFixedWidth(200)
        self.input_box.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.input_box, alignment=Qt.AlignCenter)

        # Analyze button
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.get_stock_code)
        self.layout.addWidget(self.analyze_button, alignment=Qt.AlignCenter)
        self.layout.addSpacing(20)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    # Method for getting the user entered stock code from the text box
    def get_stock_code(self):
        self.stock_code = self.input_box.text().strip().upper()

        # Check to see if the stock code is the proper length
        if not self.stock_code or len(self.stock_code) > 5:
            QMessageBox.warning(self, "Input Error", "Please enter a valid stock code.")
            return
        self.analyze_button.setEnabled(False)

        # Edit title text and remove button/text field
        self.status_label.setText(
            "<div style='font-size:20px; font-weight:bold; line-height:1.0;'>"
            f"Gathering Stock Data For {self.stock_code}"
            "</div>"
            "<div style='font-size:16px; font-style:italic; color:gray; line-height:1.0;'>"
            "The AI will make a decision based on this data..."
            "</div>"
        )
        self.input_box.setParent(None)
        self.analyze_button.setParent(None)
        self.input_box = None
        self.analyze_button = None

        # Create progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.progress_bar)
        
        # Create and start thread 
        self.thread = AnalysisLogic(self.stock_code)
        self.thread.no_stock.connect(self.no_stock_error)
        self.thread.ai_deciding.connect(self.update_title_deciding)
        self.thread.finished_analysis.connect(self.analysis_complete)
        self.thread.start()

    # Method for displaying an error when the requested stock is not found
    def no_stock_error(self):
        # Edit title text to display error, hide progress bar
        self.status_label.setText(
            "<div style='font-size:20px; font-weight:bold; line-height:1.0;'>"
            f"{self.stock_code} not found in Yahoo Finance's database"
            "</div>"
            "<div style='font-size:16px; font-style:italic; color:gray; line-height:1.0;'>"
            "Try again with a valid stock code:"
            "</div>"
        )
        self.progress_bar.setParent(None)
        self.progress_bar = None

        # Input box
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("e.g. NVDA")
        self.input_box.setFixedWidth(200)
        self.input_box.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.input_box, alignment=Qt.AlignCenter)

        # Analyze button
        self.analyze_button = QPushButton("Analyze")
        self.analyze_button.clicked.connect(self.get_stock_code)
        self.layout.addWidget(self.analyze_button, alignment=Qt.AlignCenter)
        self.layout.addSpacing(20)

    # Method for updating the GUI title after the stock data is gathered
    def update_title_deciding(self):
        self.status_label.setText(
            "<div style='font-size:20px; font-weight:bold; line-height:1.0;'>"
            f"Retrieved stock data for {self.stock_code}!"
            "</div>"
            "<div style='font-size:16px; font-style:italic; color:gray; line-height:1.0;'>"
            "Asking our AI model if you should buy, sell, or hold this stock..."
            "</div>"
        )

    # Method to display the analysis result
    def analysis_complete(self, decision):
        # Edit title text and remove button/text field
        self.status_label.setText(
            "<div style='font-size:20px; font-weight:bold; line-height:1.0;'>"
            f"You should {decision} {self.stock_code}."
            "</div>"
            "<div style='font-size:16px; font-style:italic; color:gray; line-height:1.0;'>"
            "Remember - take this advice with a grain of salt!"
            "</div>"
        )
        self.progress_bar.setParent(None)
        self.progress_bar = None

        # Return home button
        self.return_home = QPushButton("Done")
        self.return_home.clicked.connect(self.close_window)
        self.layout.addWidget(self.return_home, alignment=Qt.AlignCenter)
        self.layout.addSpacing(20)

    # Method for returning to the home screen
    def close_window(self):
        self.return_home.setEnabled(False)
        self.close()
        
# Function for managing the first option
def manage_option_one():
    # Start GUI
    window = AnalysisWindow()
    window.show()
    return window