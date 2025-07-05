from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QRadioButton, QPushButton, QMessageBox, 
    QButtonGroup, QHBoxLayout, QSizePolicy
)
from PySide6.QtCore import Qt
import sys

option_selected = -1

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Munger's Stock Advisor")
        self.setGeometry(100, 100, 400, 300)

        # Define layouts
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)         
        main_layout.setContentsMargins(10, 10, 10, 10)  
        title_layout = QVBoxLayout()
        title_layout.setSpacing(0)   
        title_layout.setContentsMargins(0, 0, 0, 0)

        # Create the title element using HTML
        title_label = QLabel()
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setText(
            "<div style='font-size:24px; font-weight:bold; line-height:1.0;'>"
            "Welcome to Munger's Stock Advisor!"
            "</div>"
            "<div style='font-size:16px; font-style:italic; color:gray; line-height:1.0;'>"
            "Written by Brian Munger, 2025"
            "</div>"
        )
        title_layout.addWidget(title_label)
        main_layout.addLayout(title_layout)

        # Create radio buttons for options
        self.radio_buy_sell = QRadioButton("1. AI Buy / Sell / Hold")
        self.radio_train = QRadioButton("2. Train AI Model")
        self.radio_exit = QRadioButton("3. Exit")

        # Center the radio buttons, add title and submit button
        options_layout = QVBoxLayout()
        options_layout.setAlignment(Qt.AlignCenter)
        label_select = QLabel("Select an Option:")
        label_select.setStyleSheet("font-size: 20px; font-weight: bold;")
        options_layout.addWidget(label_select)
        options_layout.addWidget(self.radio_buy_sell)
        options_layout.addWidget(self.radio_train)
        options_layout.addWidget(self.radio_exit)
        main_layout.addLayout(options_layout)

        submit_btn = QPushButton("Select")
        submit_btn.setFixedWidth(100)
        submit_btn.clicked.connect(self.handle_submit)
        submit_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        # Center it within the options block
        submit_container = QHBoxLayout()
        submit_container.setAlignment(Qt.AlignCenter)
        submit_container.addWidget(submit_btn)
        options_layout.addLayout(submit_container)

        # Group radio buttons so only one can be selected
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radio_buy_sell)
        self.button_group.addButton(self.radio_train)
        self.button_group.addButton(self.radio_exit)
        main_layout.addWidget(self.radio_buy_sell)
        main_layout.addWidget(self.radio_train)
        main_layout.addWidget(self.radio_exit)

        # Disclaimer and about button
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

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def handle_submit(self):
        global option_selected

        if self.radio_buy_sell.isChecked():
            option_selected = 1
        elif self.radio_train.isChecked():
            option_selected = 2
        elif self.radio_exit.isChecked():
            self.close()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an option before submitting.")

    def show_disclaimer(self):
        QMessageBox.information(self, "Disclaimer", "")

    def show_about(self):
        QMessageBox.information(self, "About", "")

def run_main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_main_window()
