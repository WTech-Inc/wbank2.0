"""Test wbank/home route by calling it directly"""
import sys, os, hashlib, json
sys.stdout.reconfigure(encoding='utf-8')

os.chdir("E:/wbank")
os.environ["dataurl"] = "postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"

from main import app

with app.test_client() as c:
    # Test root redirect
    resp = c.get("/")
    print(f"GET /: {resp.status_code}")
    if resp.status_code == 302:
        print(f"  Redirect to: {resp.location}")
        # Follow redirect
        resp2 = c.get(resp.location)
        print(f"  Follow redirect: {resp2.status_code}")

    # Test home with accessKey
    key = hashlib.sha256("wtech->wtech888->true".encode("utf-8")).hexdigest()
    resp3 = c.get(f"/wbank/home?accessKey={key}")
    print(f"GET /wbank/home: {resp3.status_code}")
    if resp3.status_code != 200:
        print(f"  Response: {resp3.data[:500]}")

    # Test auth login
    resp4 = c.get("/wbank/auth/v1")
    print(f"GET /wbank/auth/v1: {resp4.status_code}")
    if resp4.status_code != 200:
        print(f"  Response: {resp4.data[:500]}")
