"""Add swap link to admin sidebar"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/templates/admin/index.html", "r", encoding="utf-8").read()

# Find KYC link end and add swap after it
idx = c.find("showSection('kyc', this)")
if idx < 0:
    print("KYC link not found!")
    sys.exit(1)

# Find the end of the KYC link
link_end = c.find("</a>", idx)
if link_end < 0:
    print("KYC link end not found!")
    sys.exit(1)

swap_link = '\n        <a href="#" onclick="showSection(\'swap\', this)">💱 WTC/HKD Swap</a>'

c = c[:link_end+4] + swap_link + c[link_end+4:]

open("E:/wbank/templates/admin/index.html", "w", encoding="utf-8").write(c)
print(f"OK - swap link added after position {link_end}")
