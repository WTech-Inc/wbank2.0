"""Check table structure"""
import psycopg2
conn = psycopg2.connect("postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require")
cur = conn.cursor()
cur.execute("SELECT count(*) FROM wbankwallet")
print("Count:", cur.fetchone()[0])
cur.execute("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name='wbankwallet' ORDER BY ordinal_position")
for r in cur.fetchall():
    print(f"  {r[0]:20} {r[1]:15} nullable={r[2]}")
cur.close()
conn.close()
print("OK")
