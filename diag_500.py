"""Diagnose 500 error on login page - standalone Flask test"""
import sys, os, hashlib
sys.stdout.reconfigure(encoding='utf-8')

os.chdir("E:/wbank")
os.environ["dataurl"] = "postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

# Manually set up Flask app similar to main.py
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from extensions import db

app = Flask("WTech")
app.config['SECRET_KEY'] = hashlib.sha256("WTech2225556".encode()).hexdigest()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["dataurl"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)
db.init_app(app)

# Import models
from models import *

with app.app_context():
    db.create_all()
    print("DB tables OK")
    users = wbankwallet.query.all()
    print(f"Users: {len(users)}")

# Try rendering the template
from flask import render_template_string
template_content = open("templates/wbank/login.html", encoding="utf-8").read()

try:
    rendered = render_template_string(template_content, url="/wbank")
    print("LOGIN TEMPLATE OK - rendered successfully")
except Exception as e:
    print(f"LOGIN TEMPLATE FAIL: {e}")
    import traceback
    traceback.print_exc()

# Try the home template
try:
    home_content = open("templates/wbank/home.html", encoding="utf-8").read()
    rendered = render_template_string(home_content, count=5)
    print("HOME TEMPLATE OK - rendered successfully")
except Exception as e:
    print(f"HOME TEMPLATE FAIL: {e}")
    import traceback
    traceback.print_exc()
