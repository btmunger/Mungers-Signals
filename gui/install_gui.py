import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QPushButton,  
    QProgressBar
)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
import ctypes

class InstallWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window / taskbar icon 
        myappid = u'arbitrary string in unicode' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowIcon(QIcon("gui/icon/logo.ico"))

        # Window title and inital position / size of GUI
        self.setWindowTitle("Munger's Signals")
        self.setGeometry(100, 100, 400, 300) # x, y, width, height

        # Define layouts
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 10, 10, 10)
        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Create the title element using HTML
        title_label = QLabel()
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setText(
            "<div style='font-size:24px; font-weight:bold; line-height:1.0;'>"
            "Welcome to Munger's Signals!"
            "</div>"
            "<div style='font-size:16px; font-style:italic; color:gray; line-height:1.0;'>"
            "Your AI Day Trading Buddy!"
            "</div>"
        )
        title_layout.addWidget(title_label)
        main_layout.addLayout(title_layout)

        # Progresss bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(300)
        self.progress_bar.setTextVisible(False)
        self.layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Installing libraries text
        self.time_remaining = QLabel()
        self.time_remaining.setText("Installing required py packages...")
        self.time_remaining.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.time_remaining)
        self.layout.addSpacing(100)

# Method for handling the installation window
def run_install_window():
    # Start GUI
    app = QApplication(sys.argv)
    window = InstallWindow()
    app.exec()