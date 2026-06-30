Set WshShell = CreateObject("WScript.Shell")  
WshShell.CurrentDirectory = "E:\wbank"  
WshShell.Run "python main.py", 0, False  
