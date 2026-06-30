"""Fix audit log timezone to UTC+8"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/main.py"
c = open(path, "r", encoding="utf-8").read()

old = '''"timestamp": e.timestamp.strftime("%Y/%m/%d %H:%M:%S") if e.timestamp else ""'''
new = '''"timestamp": pytz.timezone("Asia/Taipei").fromutc(e.timestamp).strftime("%Y/%m/%d %H:%M:%S") if e.timestamp else ""'''

if old in c:
    c = c.replace(old, new)
    open(path, "w", encoding="utf-8").write(c)
    print("OK - timezone fix applied")
else:
    print("Pattern not found")
    idx = c.find("strftime")
    if idx >= 0:
        print(f"Found at {idx}: {c[idx:idx+100]}")
