"""Test Neon DB connection"""
import psycopg2
try:
    conn = psycopg2.connect(
        "postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
    )
    cur = conn.cursor()
    cur.execute("SELECT 1")
    print("DB OK - connected")
    cur.close()
    conn.close()
except Exception as e:
    print(f"DB FAIL: {e}")
