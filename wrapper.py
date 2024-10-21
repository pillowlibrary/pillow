import os
import subprocess

working_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(working_directory)
subprocess.run([r"C:\Users\bob\AppData\Local\Programs\Python\Python310\pythonw.exe", "main.py"])
