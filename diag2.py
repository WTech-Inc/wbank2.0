"""Diagnose 500 - test routes directly with app"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

os.environ["dataurl"] = "postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from extensions import db
from flask_login import LoginManager
import hashlib

app = Flask("WTech")
app.config['SECRET_KEY'] = hashlib.sha256("WTech2225556".encode()).hexdigest()
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["dataurl"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing

csrf = CSRFProtect(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

from models import *

with app.app_context():
    db.create_all()

# Register just the routes we want to test
@app.route("/")
def index():
    return "root ok"

@app.route("/wbank/auth/v1")
def login():
    from flask import render_template
    return render_template("wbank/login.html", url="/wbank")

@app.route("/wbank/home")
def home():
    from flask import render_template
    users = wbankwallet.query.all()
    count = len([u for u in users if u.username != 'wbank'])
    return render_template("wbank/home.html", count=count)

# Test
with app.test_client() as c:
    r1 = c.get("/")
    print(f"GET /: {r1.status_code}")
    if r1.status_code != 200:
        print(f"  Error: {r1.data[:200]}")

    r2 = c.get("/wbank/auth/v1")
    print(f"GET /wbank/auth/v1: {r2.status_code}")
    if r2.status_code != 200:
        print(f"  Error: {r2.data[:500]}")
    else:
        print(f"  Body: {r2.data[:200]}")

    r3 = c.get("/wbank/home")
    print(f"GET /wbank/home: {r3.status_code}")
    if r3.status_code != 200:
        print(f"  Error: {r3.data[:500]}")
    else:
        print(f"  Body: {r3.data[:200]}")
