import os
import subprocess
import sys

working_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(working_directory)

subprocess.Popen([r"C:\Users\bob\AppData\Local\Programs\Python\Python310\pythonw.exe", "main.py"],
                 creationflags=subprocess.CREATE_NEW_PROCESS_GROUP,
                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

sys.exit()
