# Installation Guide

### Prerequisites 

Two prerequisites are required to run this program:
1. Python version 3.13 or greater (https://www.python.org/downloads/)
2. Google Chrome (https://www.google.com/chrome/dr/download/)

### How to Install

Similar to other GitHub projects, there are a couple of different ways to download and use this project. In general, you can download the project via the zip file or by cloning the repository:
1. Zip File: Navigate to the "releases" tab on the right side of this GitHub repository. Select the latest release and download the attached zip file. Extract the folder, and run the program.
2. Clone Repo: Navigate to your desired directory that you would like to clone the repository in (using the 'cd' shell command). Then, clone it using this command (can be found under the "<> Code" button as well): "git clone git@github.com:btmunger/Mungers-Signals.git".

On the first run, any missing Python libraries that are required for the program to run will be installed. This may take a couple of minutes, but the program will redirect you to the main screen once completed. If you're curious about what files are installed, reference "install_libraries.py". Note that PySide6 is installed in the "bootstrap.py" file upon first run. 

### How to Run

Running the program via the executable file (MungerSignals.exe) is the easiest way to run the project. Please note that I elected not to buy a certificate from a Certificate Authority, which leads Windows to "protect your PC" from the project (a warning will appear letting you know that an unknown publisher made the application). Please select "More info," then "Run anyway." If this scares you, no problem at all! You can also run it via Python commands.  

Running the program via Python commands is a great way to bypass this Windows Defender error and to check for any errors with the program. In the project directory (/Mungers-Signals), run this Python command: "python bootstrap.py." This file checks that the required packages are installed and redirects you to the main logic file. For more on how the files are organized, reference the FILE_STRUCTURE.md file in /docs.
