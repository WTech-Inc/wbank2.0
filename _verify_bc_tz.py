"""Verify wcoins_blockchain pytz fix is active"""
import sys, inspect

# Clear cache
if 'wcoins_blockchain' in sys.modules:
    del sys.modules['wcoins_blockchain']

from wcoins_blockchain import Blockchain
src = inspect.getsource(Blockchain.get_chain)

if 'pytz' in src and 'Asia/Taipei' in src:
    print('OK: get_chain has pytz conversion')
else:
    print('WARN: get_chain MISSING pytz conversion!')
    print(src[:300])

src2 = inspect.getsource(Blockchain.get_user_tx)
if 'pytz' in src2 and 'Asia/Taipei' in src2:
    print('OK: get_user_tx has pytz conversion')
else:
    print('WARN: get_user_tx MISSING pytz conversion!')

# Test with real data
from sqlalchemy import create_engine, text
engine = create_engine('postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require')
bc = Blockchain(engine)
chain = bc.get_chain(limit=2)
if chain:
    ts = chain[0].get("created_at","N/A")
    print(f'Chain block time: {ts}')
    # Should be UTC+8 (e.g., 05:32 UTC = 13:32 UTC+8)
    if '13:' in chain[0].get('created_at', ''):
        print('TIMEZONE CORRECT: UTC+8 displayed')
    elif '05:' in chain[0].get('created_at', ''):
        print('TIMEZONE WRONG: Still UTC!')
else:
    print('No chain data available')
