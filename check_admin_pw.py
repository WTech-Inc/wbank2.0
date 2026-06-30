"""Check exact admin password"""
import sys, psycopg2
sys.stdout.reconfigure(encoding="utf-8")
conn = psycopg2.connect("postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
cur = conn.cursor()
cur.execute("SELECT password FROM wbankwallet WHERE username='wbank'")
pw = cur.fetchone()
print(repr(pw[0]))
cur.close()
conn.close()
