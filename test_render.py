"""Test template rendering with exact same Flask config as main.py"""
import sys, os
sys.stdout.reconfigure(encoding="utf-8")
os.chdir("E:/wbank")
os.environ["dataurl"] = "postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

from flask import Flask, render_template, render_template_string
from flask_wtf.csrf import CSRFProtect
import hashlib

app = Flask("WTech")
app.config["SECRET_KEY"] = hashlib.sha256("WTech2225556".encode()).hexdigest()
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["dataurl"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)

from extensions import db
db.init_app(app)

from models import *

print(f"root_path: {app.root_path}")
print(f"template_folder: {app.template_folder}")

with app.app_context():
    db.create_all()

    # Test simple string rendering
    try:
        r = render_template_string("test {{ url }}", url="/wbank")
        print(f"String render: OK ({r})")
    except Exception as e:
        print(f"String render FAIL: {e}")

    # Test login template
    try:
        r = render_template("wbank/login.html", url="/wbank")
        print(f"Login render: OK ({len(r)} bytes)")
    except Exception as e:
        print(f"Login render FAIL: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    # Check if static file exists
    static_dir = os.path.join(app.root_path, "static")
    print(f"static dir exists: {os.path.isdir(static_dir)}")
    if os.path.isdir(static_dir):
        print(f"static files: {os.listdir(static_dir)[:10]}")
