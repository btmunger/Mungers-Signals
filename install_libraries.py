import subprocess
import sys

# Method for running the install GUI
def run_install_gui():
    from PySide6.QtWidgets import QApplication
    app = QApplication(sys.argv)

    from gui.install_gui import run_install_window
    window = run_install_window()
    window.show()
    app.exec()

    from main import run_gui
    run_gui(app)

# Method for installing the required libraries for the program
def install_libs():
    # Required packages to be installed
    packages = ["joblib", "numpy", "pandas", "selenium", "scikit-learn", "urllib3", "transformers", "torch"]
    CREATE_NO_WINDOW = 0x08000000

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install"] + packages,
        creationflags=CREATE_NO_WINDOW
    )

if __name__ == "__main__":
    run_install_gui()