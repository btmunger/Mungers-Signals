from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QSystemTrayIcon
from PySide6.QtGui import QIcon
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Munger's Stock Advisor")
        self.setGeometry(100, 100, 400, 200)
        self.setWindowIcon(QIcon("gui/logo.png"))

        # Does not work
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("gui/logo.png"))  
        self.tray_icon.setToolTip("Munger's Stock Advisor")
        self.tray_icon.show() 

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Welcome to Munger's Stock Advisor"))
        layout.addWidget(QLabel("Click buttons to run analysis or train model (TODO)"))

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
