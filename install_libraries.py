import subprocess
import sys

# Method for installing the required libraries for the program
def install_libs():
    # Required packages to be installed
    packages = ["joblib", "numpy", "pandas", "PySide6", "selenium", "scikit-learn", "urllib3", "transformers", "torch"]

    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)