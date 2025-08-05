from PySide6.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, QRadioButton, QPushButton, QMessageBox,
    QButtonGroup, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
import ctypes

# Class for GUI main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the window / taskbar icon 
        myappid = u'arbitrary string in unicode' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        self.setWindowIcon(QIcon("gui/icon/logo.ico"))

        # Window title and inital position / size of GUI
        self.setWindowTitle("Munger's Signals")
        self.setGeometry(100, 100, 400, 300) # x, y, width, height

        # Initialize option selected variable
        self.option_selected = -1

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

        # Create radio buttons for options
        self.radio_buy_sell = QRadioButton("1. AI Buy / Sell / Hold")
        self.radio_train = QRadioButton("2. Train AI Model")
        self.radio_exit = QRadioButton("3. Exit")

        # Center the radio buttons, add title button
        options_layout = QVBoxLayout()
        options_layout.setAlignment(Qt.AlignCenter)
        label_select = QLabel("Select an Option:")
        label_select.setStyleSheet("font-size: 20px; font-weight: bold;")
        options_layout.addWidget(label_select)
        options_layout.addWidget(self.radio_buy_sell)
        options_layout.addWidget(self.radio_train)
        main_layout.addLayout(options_layout)
        # Select button 
        select_btn = QPushButton("Select")
        select_btn.setFixedWidth(100)
        select_btn.clicked.connect(self.handle_select)
        select_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Center the button within the options block
        submit_container = QHBoxLayout()
        submit_container.setAlignment(Qt.AlignCenter)
        submit_container.addWidget(select_btn)
        options_layout.addLayout(submit_container)

        # Group radio buttons so only one can be selected
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_buy_sell)
        self.button_group.addButton(self.radio_train)
        self.button_group.addButton(self.radio_exit)

        # Disclaimer and about buttons
        bottom_buttons_layout = QHBoxLayout()
        bottom_buttons_layout.setSpacing(20)
        disclaimer_btn = QPushButton("Disclaimer")
        disclaimer_btn.setFixedWidth(100)
        disclaimer_btn.clicked.connect(self.show_disclaimer)
        about_btn = QPushButton("About")
        about_btn.setFixedWidth(100)
        about_btn.clicked.connect(self.show_about)
        bottom_buttons_layout.addStretch()
        bottom_buttons_layout.addWidget(disclaimer_btn)
        bottom_buttons_layout.addWidget(about_btn)
        bottom_buttons_layout.addStretch()
        main_layout.addLayout(bottom_buttons_layout)

        # Set window
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    # Class method for handling when an option is selected
    def handle_select(self):
        # Mark the appropriate selection
        if self.radio_buy_sell.isChecked():
            self.option_selected = 1
        elif self.radio_train.isChecked():
            self.option_selected = 2
        else:
            QMessageBox.warning(self, "No Selection", "Please select an option before submitting.")
            return

        # Close the current window
        self.close() 

    def show_disclaimer(self):
        QMessageBox.information(self, "Disclaimer", "")

    def show_about(self):
        QMessageBox.information(self, "About", "")

# Main method for running the title / into GUI window
def run_main_window():
    window = MainWindow()
    window.show()
    return window