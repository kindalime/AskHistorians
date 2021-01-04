# Run this on a Windows device to package all the files into a windows executable.

import sys
from cx_Freeze import setup, Executable

# includes      = []
# include_files = [r"C:\Users\(USERNAME)\AppData\Local\Programs\Python\Python35-32\DLLs\tcl86t.dll", \
#                  r"C:\Users\(USERNAME)\AppData\Local\Programs\Python\Python35-32\DLLs\tk86t.dll"]

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("main.py", base=base)]

setup(executables=executables)