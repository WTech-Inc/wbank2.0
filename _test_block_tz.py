"""Test Block to_dict timezone conversion"""
import sys
sys.modules.pop('wcoins_blockchain', None)
from wcoins_blockchain import Block
import pytz
from datetime import datetime

b = Block(1, 'sender', 'receiver', '100')
print('Block created_at (UTC):', b.created_at)
d = b.to_dict()
print('to_dict created_at:', d['created_at'])

# Verify conversion
local = pytz.UTC.localize(b.created_at).astimezone(pytz.timezone('Asia/Taipei'))
expected = local.strftime('%Y-%m-%d %H:%M:%S')
print('Expected (UTC+8):', expected)
print('Got:', d['created_at'])
print('MATCH:', d['created_at'] == expected)
