"""Check Flask path resolution"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir("E:/wbank")
os.environ["dataurl"] = "postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
from flask import Flask
app = Flask("WTech")
print("root_path:", app.root_path)
print("template_folder:", app.template_folder)
tpl_path = os.path.join(app.root_path, "templates", "wbank", "login.html")
print("login.html exists:", os.path.exists(tpl_path))
print("CWD:", os.getcwd())
print("Dir exists:", os.path.isdir(os.path.join(app.root_path, "templates", "wbank")))
# Try to find where templates actually are
for root, dirs, files in os.walk("."):
    for f in files:
        if f == "login.html":
            print(f"Found at: {os.path.join(root, f)}")
