import subprocess
import sys

# Method for installing the required libraries
def install_libraries(app):
    from gui.install_gui import run_install_window
    window = run_install_window()
    window.show()
    app.exec()

# Variable that tracks if missing libraries need to be installed
libraries_installed = True

# Try to import PySide6 library
try:
    from PySide6.QtWidgets import QApplication
    print("")
except ImportError:
    print("\nFirst time running, installing required libraries...\n")
    libraries_installed = False

    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "PySide6"])

    from PySide6.QtWidgets import QApplication  # Try again

# Start GUI
app = QApplication(sys.argv)

# Install rest of libraries w/ GUI screen if required
if not libraries_installed:
    from main import install_libraries
    install_libraries(app)

# Call main function to run / install libraries if required
from main import run_gui
run_gui(app)