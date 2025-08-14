# Common Errors and Issues

During testing, most errors and issues originated from the setup process. Commonly, Python or Pip was not configured correctly, or Windows Defender may be trying to block the application from running. Below are some common issues and suggested fixes:  

| Issue / Error             | Suggested Fix                                                                                                                                                                                         |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Windows protected your PC | Windows displays this warning because this is an "unrecognized application." Select "More info," then "Run anyway."                                                                                    |
| Python not recognized.    | Ensure Python (version 3.13 or greater) is correctly installed. Check 'system environment variables,' and add Python's executable path to the "Path" variable.                                        |
| Pip not recognized.       | Pip is what Python uses to install libraries / packages. Check 'system environment variables,' and add Pip's executable path (located in the /scripts folder in Python's dir) to the "Path" variable. |
| Training mode freezes     | If edits were made to train_stock_list.csv, ensure the file is in its original format. Verify your device is connected to the internet.                                                                |   

If you encounter any errors or issues while running the .exe file, please attempt to run the program by opening a terminal and navigating to the project directory. Run the program via the "python ./bootstap" command, and reference the table above!  

After trying the above fixes, if the problem persists, please feel free to add it to the "Issues" tab on GitHub. I will investigate the issue and implement a patch if necessary!  
