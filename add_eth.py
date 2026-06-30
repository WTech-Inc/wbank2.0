import psycopg2
conn = psycopg2.connect(
    database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()
cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name='wbankwallet'")
cols = [r[0] for r in cur.fetchall()]
print('Current columns:', cols)
if 'eth_address' not in cols:
    cur.execute('ALTER TABLE wbankwallet ADD COLUMN eth_address VARCHAR(64)')
    print('Added eth_address')
if 'eth_key_encrypted' not in cols:
    cur.execute('ALTER TABLE wbankwallet ADD COLUMN eth_key_encrypted TEXT')
    print('Added eth_key_encrypted')
conn.commit()
conn.close()
print('Done')
