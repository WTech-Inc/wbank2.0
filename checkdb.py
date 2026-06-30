import psycopg2  
conn=psycopg2.connect(database='neondb',user='neondb_owner',password='npg_KP2Zat1YscBz',host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech',port=5432,sslmode='require')  
cur=conn.cursor()  
cur.execute('SELECT column_name FROM information_schema.columns WHERE table_name=''wbankwallet''')  
for r in cur: print(r[0])  
cur.close() 
conn.close() 
