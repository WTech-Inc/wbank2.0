"""Fix the quote issue in swap function"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

with open("E:/wbank/main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Find the problematic line and replace it
old = "onsubmit=\"return confirm('Confirm this withdrawal? HK$"
new = "onsubmit=\"return confirm('HK$"

content = content.replace(old, new)

# Remove the ' cash' part
old2 = " + ' cash')"
content = content.replace(old2, ")")

with open("E:/wbank/main.py", "w", encoding="utf-8") as f:
    f.write(content)

import py_compile
try:
    py_compile.compile("E:/wbank/main.py", doraise=True)
    print("OK - syntax verified")
except Exception as e:
    print(f"ERROR: {e}")
