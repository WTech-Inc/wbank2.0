"""Find admin user and test login"""
import sys, ssl, urllib.request, urllib.parse, json
sys.stdout.reconfigure(encoding="utf-8")

# Find admin users
import psycopg2
conn = psycopg2.connect("postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
cur = conn.cursor()
cur.execute("SELECT username, password, role FROM wbankwallet")
for r in cur.fetchall():
    print(f"User: {r[0]}, Role: {r[2]}, PW: {r[1][:30]}...")
cur.close()
conn.close()
