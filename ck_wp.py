import psycopg2
conn = psycopg2.connect(
    database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()
cur.execute("SELECT username, password, role FROM wbankwallet WHERE username='wangtry'")
for r in cur.fetchall():
    print(f'Username: {r[0]}')
    print(f'Password (raw): {r[1]}')
    print(f'Role: {r[2]}')
cur.execute("SELECT username, password, role FROM wbankwallet WHERE role='admin'")
for r in cur.fetchall():
    print(f'Admin: {r[0]} pw={r[1][:20]}...')
conn.close()
