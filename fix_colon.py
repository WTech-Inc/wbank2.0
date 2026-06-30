"""Fix colon position in restrict_routes"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/main.py", "r", encoding="utf-8").read()

old = """if path == '/admin' or path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/socket.io/'): or path == "/admin_swap\""""
new = """if path == '/admin' or path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/socket.io/') or path == '/admin_swap':"""

if old in c:
    c = c.replace(old, new)
    open("E:/wbank/main.py", "w", encoding="utf-8").write(c)
    print("OK")
else:
    print("Not found!")
    # Show the actual line
    for i, line in enumerate(c.split("\n")):
        if "admin_swap" in line:
            print(f"Line {i+1}: {line}")
