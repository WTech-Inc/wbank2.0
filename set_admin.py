import psycopg2
conn = psycopg2.connect(
    database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()

# Set wangtry as admin
cur.execute("UPDATE wbankwallet SET role='admin' WHERE username='wangtry'")
conn.commit()
print(f'Updated {cur.rowcount} rows')

# Verify
cur.execute('SELECT username, role FROM wbankwallet WHERE role=%s', ('admin',))
for r in cur.fetchall():
    print(f'Admin: {r[0]}: role={r[1]}')

conn.close()
