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
    start_time = Signal(int)
    progress_updated = Signal(int, int)
    updated_time_rem = Signal(int)
    finished = Signal()

    # Create the thread and initalize the continue_train variable
    def __init__(self):
        super().__init__()
        self.continue_train = True

    # Method for calling the necessary functions for training the AI model
    def run(self):
        # Following three function calls redirect to stock_tracker.py
        rm_reports()
        stock_list = load_stock_list()
        driver = init_webdriver()

        completed = 0
        time_arr = []
        total = len(stock_list)

        self.start_time.emit(total * .20)

        # For each stock code specified in the CSV file...
        for stock_code in stock_list:
            if self.continue_train:
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
                time_arr.append(end_time-start_time)
                avg_time = sum(time_arr) / len(time_arr)
                self.updated_time_rem.emit(avg_time * (total - completed)) # total - completed = remaining stock reports to generate
            else:
                print("\nTraining canceled by user, returning to main GUI...\n")
                break

        # Cleanup driver
        driver.quit()

        # Emit signal that reports were generated
        if self.continue_train:
            self.finished.emit()

    # Stop the training
    def stop(self):
        self.continue_train = False

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

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

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
        self.layout.addWidget(self.status_label)
        self.layout.addSpacing(100)

        # Progress bar widget
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(300)
        self.layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Time remaining widget
        self.time_remaining = QLabel()
        self.time_remaining.setText("0 minutes remaining")
        self.time_remaining.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_remaining)
        self.layout.addSpacing(100)

        # Cancel button  
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.stop_training)
        self.cancel_button.setMaximumWidth(100)
        self.layout.addWidget(self.cancel_button, alignment=Qt.AlignCenter)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

        # Create and start thread 
        self.thread = TrainLogic()
        self.thread.start_time.connect(self.init_time_rem)
        self.thread.progress_updated.connect(self.update_progress)
        self.thread.updated_time_rem.connect(self.update_time_rem)
        self.thread.finished.connect(self.reports_complete)
        #self.thread.done_training.connect(self.training_complete)
        self.thread.start()

    # Method for setting the time remaining when the training starts
    def init_time_rem(self, time_rem):
        self.time_remaining.setText(f"{time_rem} minutes remaining")

    # Method for ending the training process when the user presses the cancel button
    def stop_training(self):
       self.thread.stop()
       self.close()

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
    def reports_complete(self):
        self.status_label.setText(
            "<div style='font-size:20px; font-weight:bold; line-height:1.0;'>"
            "Reports gathered, training model now..."
            "</div>"
        )

        # Hide time remaining text
        self.time_remaining.hide()

        # Reset progress bar
        if self.progress_bar != None:
            self.progress_bar.setTextVisible(False)
            self.progress_bar.setRange(0,0)

        # Redirects to ai_train.py
        output = train_main()
        self.status_label.setText(
            "<div style='font-size:20px; font-weight:bold; line-height:1.0;'>"
            f"AI Model Trained On {output[0]} Entries"
            "</div>"
            "<div style='font-size:16px; color:gray; line-height:1.0;'>"
            f"Model is saved as '{output[1]}'"
            "</div>"
        )

        # Remove cancel button and progress bar
        if self.cancel_button != None:
            self.cancel_button.setParent(None)
            self.cancel_button = None
        if self.progress_bar != None:
            self.progress_bar.setParent(None)
            self.progress_bar = None

        # Return home button
        if not hasattr(self, 'return_home'):
            self.return_home = QPushButton("Done")
            self.return_home.clicked.connect(self.close_window)
            self.layout.addWidget(self.return_home, alignment=Qt.AlignCenter)
            self.layout.addSpacing(20)

    # Method for returning to the home screen
    def close_window(self):
        self.return_home.setEnabled(False)
        self.close()

# Method for managing the second option
def manage_option_two():
    window = TrainWindow()
    window.show()
    return window