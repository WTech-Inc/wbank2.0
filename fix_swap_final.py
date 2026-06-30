"""Add swap sidebar link with correct emoji text"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/templates/admin/index.html", "r", encoding="utf-8").read()

# The KYC link line
old_line = '<a href="#" onclick="showSection(\'kyc\', this)">\U0001f4dd KYC 審核</a>'
new_line = '<a href="#" onclick="showSection(\'kyc\', this)">\U0001f4dd KYC 審核</a>\n        <a href="#" onclick="showSection(\'swap\', this)">\U0001f4b1 WTC/HKD Swap</a>'

if old_line in c:
    c = c.replace(old_line, new_line)
    open("E:/wbank/templates/admin/index.html", "w", encoding="utf-8").write(c)
    print("OK - swap link added")
else:
    print("NOT FOUND - showing what's around KYC:")
    idx = c.find("KYC")
    if idx >= 0:
        print(repr(c[idx-20:idx+80]))
