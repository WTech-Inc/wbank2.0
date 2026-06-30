"""Fix status check - use 'in' instead of == to handle Chinese prefix"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/main.py", "r", encoding="utf-8").read()

old = "if st == 'Pending':"
new = "if 'Pending' in str(st):"

if old in c:
    c = c.replace(old, new)
    open("E:/wbank/main.py", "w", encoding="utf-8").write(c)
    print("OK - status check fixed")
else:
    print("Pattern not found!")
    # Search for it
    idx = c.find("Pending")
    if idx >= 0:
        print(f"Found at {idx}: {c[idx-20:idx+30]}")
