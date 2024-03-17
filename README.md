# TextBud
Text files comparator

Using Python's tkinter interface and difflib module I created a Python script to compare two text files entered by the user, to avoid uploading important files to the internet on some free pages, I wanted to compare my files locally. 
The repository contains two versions of the code, the first comparing text directly using difflib.Differ(), which is a class for comparing sequences of text lines, and also having the option to change text directly in text frames, and compare it again by pressing the "Compare" button. 
![alt text](https://github.com/sabixcel/TextBud/blob/main/capture1.PNG)
The second version uses difflib.HtmlDiff(), which generates an html file with the comparison between the two files. Both implementations are very simple to use and very useful, for example, when comparing two pieces of code.
![alt text](https://github.com/sabixcel/TextBud/blob/main/capture2.PNG)
![alt text](https://github.com/sabixcel/TextBud/blob/main/capture3.PNG)

The libraries needed to be installed to run the script are: 
• pip install tk
• pip install PyQt5

The script can also be converted to an executable (.exe) file, by following this steps:
• Install PyInstaller: pip install pyinstaller
• Navigate to Your Script's Directory: open a terminal or command prompt and navigate to the directory containing your Python script
• Run PyInstaller: pyinstaller textbud_v1.py
• Locate the Executable: once PyInstaller has finished running, you can find the generated executable file in the dist directory within your script's directory
• Test the Executable: you can now test the executable to ensure it works as expected. Run the executable from the command line or by double-clicking on it.
