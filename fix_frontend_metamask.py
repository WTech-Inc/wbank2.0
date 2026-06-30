"""
fix_frontend_metamask.py — 加 MetaMask 支援 + 優化 send 體驗
Run on production server: python fix_frontend_metamask.py
"""
import sys, json
sys.stdout.reconfigure(encoding='utf-8')

WTC_CONTRACT = "0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB"
BASESCAN = "https://basescan.org"
GAS_FEE = 50

# ═══ 1. Update wbankClient.html ═══
tpl_path = 'E:\\wbank\\templates\\wbankClient.html'
tpl = open(tpl_path, 'r', encoding='utf-8').read()

# Check if already done
if 'addToMetaMask' in tpl:
    print('MetaMask button already exists')
else:
    # Add MetaMask card before QR code card
    metamask_card = '''
            <!-- Add WTC to MetaMask -->
            <div class="card" style="text-align:center;padding:16px;">
                <h3>MetaMask</h3>
                <p style="font-size:12px;color:#64748b;margin-bottom:8px;">
                    WTC Token MetaMask
                </p>
                <button onclick="addToMetaMask()"
                        style="background:#f6851b;color:white;border:none;border-radius:8px;padding:10px 24px;font-weight:600;font-size:14px;cursor:pointer;">
                    MetaMask
                </button>
                <div style="margin-top:12px;font-size:11px;color:#94a3b8;line-height:1.6;">
                    Network: Base Mainnet (Chain 8453)<br>
                    Contract: <span style="font-family:monospace;font-size:10px;">''' + WTC_CONTRACT + '''</span><br>
                    <a href="''' + BASESCAN + '''/address/''' + WTC_CONTRACT + '''" target="_blank" style="color:#4fc3f7;text-decoration:none;">
                        Basescan
                    </a>
                </div>
            </div>'''

    tpl = tpl.replace(
        '<div class="card">\n                <h3>QR</h3>',
        metamask_card + '\n            <div class="card">\n                <h3>QR</h3>'
    )
    # Also try literal version
    tpl = tpl.replace(
        '<div class="card">\n                <h3>QR</h3>',
        metamask_card + '\n            <div class="card">\n                <h3>QR</h3>'
    )
    print('MetaMask card added')

    # Add JS functions before closing </script>
    js_code = '''
        async function addToMetaMask() {
            if (!window.ethereum) {
                alert('');
                return;
            }
            try {
                await window.ethereum.request({
                    method: 'wallet_addEthereumChain',
                    params: [{
                        chainId: '0x2105',
                        chainName: 'Base Mainnet',
                        nativeCurrency: { name: 'ETH', symbol: 'ETH', decimals: 18 },
                        rpcUrls: ['https://mainnet.base.org'],
                        blockExplorerUrls: ['https://basescan.org']
                    }]
                });
                const wasAdded = await window.ethereum.request({
                    method: 'wallet_watchAsset',
                    params: {
                        type: 'ERC20',
                        options: {
                            address: '''' + WTC_CONTRACT + '''',
                            symbol: 'WTC',
                            decimals: 18
                        }
                    }
                });
                if (wasAdded) alert('WTC MetaMask!');
            } catch(e) {
                alert(e.message || '');
            }
        }
        function copyAddr() {
            const el = document.getElementById('web3-address');
            if (!el) return;
            const addr = '0x' + el.textContent;
            navigator.clipboard.writeText(addr).then(function() {
                alert('');
            }).catch(function() {
                var ta = document.createElement('textarea');
                ta.value = addr;
                document.body.appendChild(ta);
                ta.select();
                document.execCommand('copy');
                document.body.removeChild(ta);
                alert('');
            });
        }
'''

    # Insert before closing script tag, after existing code
    tpl = tpl.replace('</script>', js_code + '\n    </script>')

    # Make address clickable
    tpl = tpl.replace(
        '<span id="web3-address">{{ hash_card_number[:40] }}</span>',
        '<span id="web3-address" style="cursor:pointer;" onclick="copyAddr()" title="">{{ hash_card_number[:40] }}</span>'
    )

    # Improve send result
    old_send_result = 'result.innerHTML = \'<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;">\' + \' Sent \' + d.amount + \' WTC<br>TX: \' + (d.tx_hash ? d.tx_hash.slice(0,20)+\'...\' : \'\') + \'</div>\';'

    new_send_result = '''result.innerHTML = '<div style="background:#dcfce7;color:#16a34a;padding:12px;border-radius:8px;"> Sent ' + d.amount + ' WTC (Fee: ''' + str(GAS_FEE) + ''' WTC)<br>TX: ' + (d.tx_hash ? d.tx_hash.slice(0,20)+'...' : '') + '<br><a href="https://basescan.org/tx/' + (d.tx_hash || '') + '" target="_blank" style="color:#16a34a;">Basescan</a></div>';'''

    if old_send_result in tpl:
        tpl = tpl.replace(old_send_result, new_send_result)
        print('Send result updated')
    else:
        print('Send result pattern not found - continuing')

    # Add fee info below send button
    fee_info = '<div style="font-size:11px;color:#94a3b8;margin-top:4px;">  ' + str(GAS_FEE) + ' WTC (gas fee)</div>'
    tpl = tpl.replace('id="send-btn"> WTC</button>', 'id="send-btn"> WTC</button>' + fee_info)

    open(tpl_path, 'w', encoding='utf-8').write(tpl)
    print('wbankClient.html updated')

# === 2. Check deployer wallet ===
print('\n=== Checking deployer wallet ===')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org'))
print('Connected to Base:', w3.is_connected())

with open('E:\\wbank\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break

dep = Account.from_key(pk)
print('Deployer:', dep.address)

eth_bal = w3.eth.get_balance(dep.address)
print('ETH balance:', w3.from_wei(eth_bal, 'ether'), 'ETH')

gp = w3.eth.gas_price
cost_per_tx = gp * 100000
print('Gas price:', w3.from_wei(gp, 'gwei'), 'gwei')
print('Cost per tx:', w3.from_wei(cost_per_tx, 'ether'), 'ETH')
print('TX remaining:', int(eth_bal / cost_per_tx) if cost_per_tx > 0 else 'N/A')

if eth_bal < cost_per_tx:
    print('\nWARNING: Deployer wallet not enough ETH for gas!')
    print('Send at least', w3.from_wei(cost_per_tx * 10, 'ether'), 'ETH to', dep.address)
else:
    print('\nDeployer wallet has enough ETH')

# === 3. Test contract ===
print('\n=== Testing WTC contract ===')
try:
    wtc_addr = Web3.to_checksum_address(WTC_CONTRACT)
    min_abi = json.loads('[{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"type":"function"},{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"type":"function"}]')
    c = w3.eth.contract(address=wtc_addr, abi=min_abi)
    name = c.functions.name().call()
    symbol = c.functions.symbol().call()
    print('Contract:', name, '(', symbol, ')')
    print('Address:', WTC_CONTRACT)
    print('BaseScan:', 'https://basescan.org/address/' + WTC_CONTRACT)
    dep_wtc = c.functions.balanceOf(dep.address).call() / 10**18
    print('Deployer WTC balance:', dep_wtc, 'WTC')
except Exception as e:
    print('Contract check failed:', e)

print('\n=== DONE! ===')
print('Restart server: python restart_server.py')
