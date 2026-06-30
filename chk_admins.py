import psycopg2
conn = psycopg2.connect(
    database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()
cur.execute('SELECT username, role FROM wbankwallet ORDER BY username')
for r in cur.fetchall():
    print(f'{r[0]}: role={r[1]}')
conn.close()
