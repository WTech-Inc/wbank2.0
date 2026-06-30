"""Update main.py to use ports 8085 and 8445"""
with open("E:/wbank/main.py", "r", encoding="utf-8") as f:
    content = f.read()

changes = [
    ("HTTP_PORT = int(os.environ.get(\"HTTP_PORT\", 8080))", "HTTP_PORT = int(os.environ.get(\"HTTP_PORT\", 8085))"),
    ("HTTPS_PORT = int(os.environ.get(\"HTTPS_PORT\", 8443))", "HTTPS_PORT = int(os.environ.get(\"HTTPS_PORT\", 8445))"),
]

for old, new in changes:
    if old in content:
        content = content.replace(old, new)
        print(f"OK: {old.split('=')[0].strip()} -> {new.split('=')[1].strip()}")
    else:
        print(f"NOT FOUND: {old}")

with open("E:/wbank/main.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done - ports updated")
