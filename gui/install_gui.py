import sys
import ctypes
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QProgressBar
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QThread, Signal
from install_libraries import install_libs

# Class for running the install
class InstallLogic(QThread):
    finished_install = Signal()

    # Initalize the thread
    def __init__(self):
        super().__init__()

    # Method for calling the necessary functions for installing the py packages 
    def run(self):
        install_libs()
        self.finished_install.emit()

# Class for the GUI install window
class InstallWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the taskbar icon for Windows
        myappid = u'arbitrary string in unicode'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowIcon(QIcon("gui/icon/logo.ico"))

        # Window settings
        self.setWindowTitle("Munger's Signals")
        self.setGeometry(100, 100, 400, 300)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Title section
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
        main_layout.addWidget(title_label)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedWidth(300)
        self.progress_bar.setTextVisible(False)
        main_layout.addWidget(self.progress_bar, alignment=Qt.AlignCenter)

        # Installing text
        self.time_remaining = QLabel("Installing required Python packages...")
        self.time_remaining.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.time_remaining)

        # Set window
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Create and start thread 
        self.thread = InstallLogic()
        self.thread.finished_install.connect(self.finished)
        self.thread.start()

    # Method for closing the window once installing is finished
    def finished(self):
        self.close()
        self.thread.quit()
        self.thread.wait()
        return

# Method for handling the installation window
def run_install_window():
    # Start GUI
    window = InstallWindow()
    window.show()
    return window