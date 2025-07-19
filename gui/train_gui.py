from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QRadioButton, QPushButton, QMessageBox, 
    QButtonGroup, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
import ctypes
import sys

# Import functions from stock_tracker.py, trends.py, and ai_train.py
from stock_tracker import rm_reports, load_stock_list, init_webdriver, get_stock_data_with_retry
from trends import get_trend_report
from ai_train import train_main

# Class for running the training 
class TrainLogic(QThread):
    progress_updated = Signal(int, int)
    finished = Signal()

    # Method for calling the necessary functions for training the AI model
    def run(self):
        # Following three function calls redirect to stock_tracker.py
        rm_reports()
        stock_list = load_stock_list()
        driver = init_webdriver()

        completed = 0
        total = len(stock_list)

        # For each stock code specified in the CSV file...
        for stock_code in stock_list:
            # Redirects to stock_tracker.py
            stock_data = get_stock_data_with_retry(driver, stock_code, 2)
            if stock_data != None:
                # Redirects to trends.py
                get_trend_report(stock_code, stock_data)
                completed += 1
                self.progress_updated.emit(completed, total)

        # Redirects to ai_train.py
        train_main()
        driver.quit()
        self.finished.emit()

# Class for GUI train window (option 2)
class TrainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window / taskbar icon 
        myappid = u'arbitrary string in unicode' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowIcon(QIcon("gui/icon/logo.ico"))

        # Window title and inital position / size of GUI
        self.setWindowTitle("Munger's Stock Advisor")
        self.setGeometry(100, 100, 400, 300)

        # Initalize result variable for determining if stock reports were successfully gathered
        self.result = 0

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.status_label = QLabel("Starting training...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px;")
        layout.addWidget(self.status_label)

        self.progress_label = QLabel("Progress: 0 / 0")
        self.progress_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.progress_label)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        layout.addWidget(self.cancel_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.thread = TrainLogic()
        self.thread.progress_updated.connect(self.update_progress)
        self.thread.finished.connect(self.training_complete)
        self.thread.start()

    def update_progress(self, completed, total): 
        self.progress_label.setText(f"Progress: {completed} / {total}")
        self.status_label.setText(f"Saving trend report {completed} of {total}...")
        
    def training_complete(self):
        self.status_label.setText("Training complete.")

# Function for managing the second option. Logic located in this file to update the GUI
def manage_option_two():
    window = TrainWindow()
    window.show()
    return window