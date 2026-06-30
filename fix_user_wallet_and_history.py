"""Fix: user wallet + transaction history in frontend"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import psycopg2
from web3 import Web3

# 1. Update user's wallet address in DB
user_wallet = '0xdffa9cfe9ffa749fd93883c587193381263aa59c'
checksummed = Web3.to_checksum_address(user_wallet)
print(f'User wallet: {checksummed}')

conn = psycopg2.connect(
    database='neondb', user='neondb_owner', password='npg_KP2Zat1YscBz',
    host='ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech', sslmode='require')
cur = conn.cursor()

# Update wangtry's wallet
cur.execute("UPDATE wbankwallet SET eth_address=%s WHERE username='wangtry'", (checksummed,))
cur.execute("UPDATE wbankwallet SET eth_key_encrypted=NULL WHERE username='wangtry'")
conn.commit()
print('[OK] User wallet updated in database')

# Check Sepolia balance
w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))
eth_bal = w3.eth.get_balance(checksummed)
print(f'Sepolia ETH: {w3.from_wei(eth_bal, "ether")}')

# 2. Check and fix tx-history in frontend
tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()

if 'id="tx-history"' not in tpl:
    print('\n[FIX] tx-history div missing - adding send form + history section...')

    # Find the end of the web3 tab
    web3_end = tpl.find('</div>\n            </div>\n        </div>', tpl.find('id="web3"'))
    if web3_end > 0:
        # Add send form + history section before the closing of web3 tab
        add_section = '''
                <div style="background:white;border:1px solid #e8ecf1;border-radius:12px;padding:20px;margin-bottom:16px;">
                    <h4 style="margin:0 0 16px;font-size:16px;color:#1a1a2e;">📤 發送 WTC</h4>
                    <div style="margin-bottom:12px;">
                        <label style="font-size:13px;color:#64748b;display:block;margin-bottom:4px;">接收地址 (Ethereum 0x...)</label>
                        <input type="text" id="send-to" placeholder="0x..."
                               style="width:100%;padding:10px;border:1px solid #e2e8f0;border-radius:8px;font-size:14px;font-family:monospace;">
                    </div>
                    <div style="margin-bottom:16px;">
                        <label style="font-size:13px;color:#64748b;display:block;margin-bottom:4px;">數量 (WTC)</label>
                        <input type="number" id="send-amount" placeholder="0"
                               style="width:100%;padding:10px;border:1px solid #e2e8f0;border-radius:8px;font-size:14px;">
                    </div>
                    <button onclick="sendWTC()" id="send-btn"
                            style="width:100%;padding:12px;background:linear-gradient(135deg,#4fc3f7,#00bcd4);color:#0c0c1d;border:none;border-radius:8px;font-weight:600;font-size:15px;cursor:pointer;">
                        🔗 發送 WTC
                    </button>
                    <div id="send-result" style="margin-top:12px;display:none;"></div>
                </div>

                <div style="background:white;border:1px solid #e8ecf1;border-radius:12px;padding:20px;">
                    <h4 style="margin:0 0 12px;font-size:16px;color:#1a1a2e;">📜 交易記錄</h4>
                    <div id="tx-history" style="font-size:13px;color:#64748b;">載入中...</div>
                </div>
'''
        tpl = tpl[:web3_end] + add_section + tpl[web3_end:]
        open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8').write(tpl)
        print('[OK] Send form + tx-history added to web3 tab')
else:
    print('\n[OK] tx-history div already exists')

# 3. Also ensure loadWeb3Info references 'send-btn' correctly
if 'document.getElementById("send-btn")' not in tpl and 'send-btn' in tpl:
    print('[INFO] send-btn already referenced')

print('\n=== Done ===')
print('Restart server needed')
