"""Add WTC/ETH liquidity on Aerodrome (Base DEX)"""
import sys, json, time
sys.stdout.reconfigure(encoding='utf-8')
from web3 import Web3
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

# Contract addresses on Base
WTC = '0x498f0bDA3d53D4B45fCb8DbaAd0932e7A0C848FB'
WETH = '0x4200000000000000000000000000000000000006'  # Base WETH
ROUTER = '0xcF77a3Ba9A5CA399B7c97c74d54e5b1Beb874E43'  # Aerodrome Router

w3 = Web3(Web3.HTTPProvider('https://mainnet.base.org', request_kwargs={'timeout': 60}))

# Load deployer key
pk = ''
with open('E:\\wbank\\.env') as f:
    for line in f:
        line = line.strip()
        if line.startswith('DEPLOYER_PRIVATE_KEY='):
            pk = line.split('=', 1)[1].strip()
            break
if pk.startswith('0x'): pk = pk[2:]
deployer = Account.from_key(pk)
print(f'Deployer: {deployer.address}')
print(f'ETH: {w3.from_wei(w3.eth.get_balance(deployer.address), "ether")}')

# ERC20 ABI for approve + balanceOf
erc20_abi = json.loads('[{"constant":false,"inputs":[{"name":"spender","type":"address"},{"name":"amount","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"type":"function"},{"constant":true,"inputs":[{"name":"account","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"type":"function"}]')

wtc = w3.eth.contract(address=Web3.to_checksum_address(WTC), abi=erc20_abi)
wtc_bal = wtc.functions.balanceOf(Web3.to_checksum_address(deployer.address)).call()
print(f'Deployer WTC: {wtc_bal / 10**18}')

# 1. Approve WTC for Aerodrome Router
print('\n1. Approving WTC for Router...')
nonce = w3.eth.get_transaction_count(deployer.address)
gp = w3.eth.gas_price
tx = wtc.functions.approve(Web3.to_checksum_address(ROUTER), 500000 * 10**18).build_transaction({
    'from': deployer.address, 'nonce': nonce,
    'gas': 50000, 'gasPrice': gp, 'chainId': 8453
})
signed = deployer.sign_transaction(tx)
h = w3.eth.send_raw_transaction(signed.raw_transaction)
r = w3.eth.wait_for_transaction_receipt(h, timeout=60)
print(f'  Status: {"OK" if r.status == 1 else "FAIL"}')

# 2. Add liquidity via Aerodrome Router
print('\n2. Adding liquidity (1000 WTC + remaining ETH)...')
# Get expected ETH amount for 1000 WTC
eth_balance = w3.eth.get_balance(deployer.address)
eth_to_use = w3.to_wei(0.0003, 'ether')  # use what we can afford

if eth_balance > eth_to_use + w3.to_wei(0.0001, 'ether'):
    # Aerodrome addLiquidity expects:
    # addLiquidity(address tokenA, address tokenB, bool stable, uint amountADesired, uint amountBDesired, uint amountAMin, uint amountBMin, address to, uint deadline)
    # For WTC/ETH, tokenA=WTC, tokenB=WETH
    amount_wtc = 600 * 10**18

    # Router ABI for addLiquidityETH
    router_abi = json.loads('[{"inputs":[{"name":"token","type":"address"},{"name":"stable","type":"bool"},{"name":"amountTokenDesired","type":"uint256"},{"name":"amountTokenMin","type":"uint256"},{"name":"amountETHMin","type":"uint256"},{"name":"to","type":"address"},{"name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"name":"amountToken","type":"uint256"},{"name":"amountETH","type":"uint256"},{"name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"}]')
    router = w3.eth.contract(address=Web3.to_checksum_address(ROUTER), abi=router_abi)

    deadline = int(time.time()) + 600
    nonce2 = w3.eth.get_transaction_count(deployer.address)

    tx2 = router.functions.addLiquidityETH(
        Web3.to_checksum_address(WTC),  # token
        False,  # stable
        amount_wtc,  # amountTokenDesired
        int(amount_wtc * 0.95),  # amountTokenMin (5% slippage)
        int(eth_to_use * 0.95),  # amountETHMin
        Web3.to_checksum_address(deployer.address),  # to
        deadline
    ).build_transaction({
        'from': deployer.address, 'nonce': nonce2,
        'gas': 500000, 'gasPrice': w3.eth.gas_price,
        'chainId': 8453, 'value': eth_to_use
    })

    signed2 = deployer.sign_transaction(tx2)
    h2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
    print(f'  TX: {h2.hex()}')
    r2 = w3.eth.wait_for_transaction_receipt(h2, timeout=120)
    if r2.status == 1:
        print(f'  ✅ Liquidity added! Pool created')
        print(f'  https://aerodrome.finance/pools')
    else:
        print(f'  ❌ Failed')
        # Check why
        print(f'  Gas used: {r2.gasUsed}')
else:
    print(f'  ❌ Not enough ETH (need {w3.from_wei(eth_to_use, "ether")}, have {w3.from_wei(eth_balance, "ether")})')

# Show remaining
print(f'\nRemaining ETH: {w3.from_wei(w3.eth.get_balance(deployer.address), "ether")}')
print(f'On Aerodrome: https://aerodrome.finance/swap?inputCurrency={WTC}&outputCurrency={WETH}')
