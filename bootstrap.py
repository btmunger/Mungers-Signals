import subprocess
import shutil
import sys
import os

def boot_main():
    # Try to import PySide6 library
    try:
        from PySide6.QtWidgets import QApplication
        app = QApplication(sys.argv)

        # Call main function to run 
        from main import run_gui
        run_gui(app)
    except ImportError:
        python_exe = shutil.which("pythonw")

        subprocess.check_call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([python_exe, "-m", "pip", "install", "PySide6"])

        os.execv(python_exe, [python_exe, "install_libraries.py"] + sys.argv[1:])

if __name__ == "__main__":
    boot_main()