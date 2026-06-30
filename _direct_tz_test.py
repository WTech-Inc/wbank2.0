"""Direct test of wcoins_blockchain timezone conversion"""
import sys
sys.path.insert(0, '.')
sys.modules.pop('wcoins_blockchain', None)

from extensions import db
from main import app
from wcoins_blockchain import Blockchain
import pytz
from sqlalchemy import text

with app.app_context():
    # Direct DB check
    rows = db.execute(
        text('SELECT block_index, created_at FROM wcoins_block ORDER BY block_index DESC LIMIT 2')
    ).fetchall()

    for r in rows:
        raw_ts = r[1]
        conv_ts = pytz.UTC.localize(raw_ts).astimezone(pytz.timezone('Asia/Taipei'))
        print(f'Block #{r[0]}: raw={raw_ts} ({type(raw_ts).__name__}) -> converted={conv_ts.strftime("%Y-%m-%d %H:%M:%S")}')

    # Via Blockchain.get_chain()
    bc = Blockchain(db.session)
    chain = bc.get_chain(limit=2)
    for c in chain:
        print(f'  get_chain: #{c["block_index"]} time={c["created_at"]}')
