"""Add swap sidebar link after KYC"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/templates/admin/index.html", "r", encoding="utf-8").read()

old = "showSection('kyc', this)"
new = "showSection('kyc', this)         showSection('swap', this)"

# Replace JUST the KYC link sidebar entry
old_line = '<a href="#" onclick="showSection(\'kyc\', this)">KYC</a>'
new_line = '<a href="#" onclick="showSection(\'kyc\', this)">KYC</a>\n        <a href="#" onclick="showSection(\'swap\', this)">Swap</a>'

if old_line in c:
    c = c.replace(old_line, new_line)
    open("E:/wbank/templates/admin/index.html", "w", encoding="utf-8").write(c)
    print("OK - swap link added after KYC")
else:
    print("KYC link pattern not found")
    # Search for kyc
    idx = c.lower().find("kyc")
    if idx >= 0:
        print(f"KYC found at {idx}: {c[idx-30:idx+80]}")
