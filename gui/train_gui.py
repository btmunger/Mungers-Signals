from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,  
    QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
import ctypes
import time

# Import functions from stock_tracker.py, trends.py, and ai_train.py
from main import rm_reports, load_stock_list, init_webdriver, get_stock_data_with_retry
from trends import get_trend_report
from ai_train import train_main

# Class for running the training 
class TrainLogic(QThread):
    start = Signal(int)
    progress_updated = Signal(int, int)
    updated_time_rem = Signal(int)
    finished = Signal()

    # Method for calling the necessary functions for training the AI model
    def run(self):
        # Following three function calls redirect to stock_tracker.py
        rm_reports()
        stock_list = load_stock_list()
        driver = init_webdriver()

        completed = 0
        time_arr = []
        total = len(stock_list)

        self.start.emit(5)

        # For each stock code specified in the CSV file...
        for stock_code in stock_list:
            start_time = time.perf_counter()

            # Redirects to stock_tracker.py
            stock_data = get_stock_data_with_retry(driver, stock_code)
            if stock_data != None:
                # Redirects to trends.py
                get_trend_report(stock_code, stock_data)

            # Update progress bar
            completed += 1
            self.progress_updated.emit(completed, total)

            # Update the time remaining text
            end_time = time.perf_counter()
            print(end_time-start_time)
            time_arr.append(end_time-start_time)
            avg_time = sum(time_arr) / len(time_arr)
            self.updated_time_rem.emit(avg_time * (total - completed)) # total - completed = remaining stock reports to generate

        # Cleanup driver, switch GUI text
        driver.quit()
        self.progress_updated.emit

        # Redirects to ai_train.py
        train_main()
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
        self.setWindowTitle("Munger's Signals")
        self.setGeometry(100, 100, 400, 300)

        # Initalize result variable for determining if stock reports were successfully gathered
        self.result = 0

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # GUI window title / subtitle 
        self.status_label = QLabel()
        self.status_label.setText(
            "<div style='font-size:20px; font-weight:bold; line-height:1.0;'>"
            "Gathering Stock Reports For Training"
            "</div>"
            "<div style='font-size:16px; font-style:italic; color:gray; line-height:1.0;'>"
            "This may take a while..."
            "</div>"
        )
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        layout.addSpacing(100)

        # Progress bar widget
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(300)
        layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Time remaining widget
        self.time_remaining = QLabel()
        self.time_remaining.setText("Around 0 minutes remaining")
        self.time_remaining.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.time_remaining)
        layout.addSpacing(100)

        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        self.cancel_button.setMaximumWidth(100)
        layout.addWidget(self.cancel_button, alignment=Qt.AlignCenter)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Create and start thread 
        self.thread = TrainLogic()
        self.thread.start(self.init_time_rem)
        self.thread.progress_updated.connect(self.update_progress)
        self.thread.updated_time_rem.connect(self.update_time_rem)
        self.thread.finished.connect(self.report_complete)
        self.thread.start()

    # Method for setting the time remaining when the training starts
    def init_time_rem(self, time_rem):
        self.time_remaining.setText(f"{time_rem} minutes remaining")

    # Method for updating the progress bar
    def update_progress(self, completed, total): 
        # Determine the progress by dividing completed reports by total
        progress = round((completed / total) * 100, 2)
        print(f"{progress}% done")
        self.progress_bar.setValue(progress)

    # Method for updating the time remaining text
    def update_time_rem(self, avg_time):
        avg_time_mins = round(avg_time / 60 )
        if avg_time_mins > 1:
            self.time_remaining.setText(f"{avg_time_mins} minutes remaining")
        else:
            self.time_remaining.setText("Less than a minute remaining")
        
    # Method for hiding certain widgets when report gathering is complete
    def report_complete(self):
        self.status_label.setText(
            "<div style='font-size:20px; font-weight:bold; line-height:1.0;'>"
            "Reports gathered, training model now..."
            "</div>"
        )

        # Hide progress bar and time remaining text
        self.progress_bar.hide()
        self.time_remaining.hide()

# Function for managing the second option
def manage_option_two():
    window = TrainWindow()
    window.show()
    return window