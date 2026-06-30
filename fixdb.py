#!/usr/bin/env python3
"""Fix wbankwallet table - add missing columns"""
import psycopg2
import os

url = os.environ.get(
    "dataurl",
    "postgresql://neondb_owner:***@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
)

conn = psycopg2.connect(url)
cur = conn.cursor()

# Add missing columns
cur.execute("ALTER TABLE wbankwallet ADD COLUMN IF NOT EXISTS mfa_key VARCHAR(120)")
cur.execute("ALTER TABLE wbankwallet ADD COLUMN IF NOT EXISTS openpay BOOLEAN DEFAULT FALSE")

conn.commit()
cur.close()
conn.close()
print("DB FIX OK")
