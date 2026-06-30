"""Check end of file for JS issues"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
lines = open("E:/wbank/templates/wbankClient.html", "r", encoding="utf-8").readlines()
for i in range(max(0, len(lines)-30), len(lines)):
    print(f"{i+1}: {lines[i].rstrip()[:120]}")
