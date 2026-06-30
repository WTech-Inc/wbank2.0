"""Fix Flask app to use explicit root_path"""
import os

path = "E:/wbank/main.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

old_line = 'app = Flask(__name__)'
new_line = '_ROOT = os.path.dirname(os.path.abspath(__file__))\napp = Flask(__name__, root_path=_ROOT)'

if old_line in content:
    content = content.replace(old_line, new_line)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK")
else:
    print("NOT FOUND")
    print([l for l in content.split("\n") if "Flask" in l])
