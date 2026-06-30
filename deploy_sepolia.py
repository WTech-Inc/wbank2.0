"""Deploy WTC to Sepolia Testnet"""
import sys, os, json, time
sys.stdout.reconfigure(encoding='utf-8')

# 1. Use existing wallet from env or generate new
print('[1/4] Setting up deployer wallet...')
from eth_account import Account
Account.enable_unaudited_hdwallet_features()

pk = os.environ.get('DEPLOYER_PRIVATE_KEY', '')
if not pk:
    # Try reading from .env file
    try:
        with open(os.path.join(os.path.dirname(__file__) or 'E:\\wbank', '.env')) as f:
            for line in f:
                if line.startswith('DEPLOYER_PRIVATE_KEY='):
                    pk = line.strip().split('=', 1)[1]
                    break
    except:
        pass

if pk:
    if pk.startswith('0x'):
        pk = pk[2:]
    acct = Account.from_key(pk)
else:
    acct = Account.create()
    pk = acct.key.hex()
    # Save to .env
    with open(os.path.join(os.path.dirname(__file__) or 'E:\\wbank', '.env'), 'w') as f:
        f.write(f'DEPLOYER_PRIVATE_KEY=0x{pk}\n')

addr = acct.address

print(f'  Address: {addr}')

# 2. Skip OpenZeppelin - write standalone ERC20 without imports
print('\n[2/4] Writing standalone WTC contract (no imports needed)...')
oz_dir = 'E:\\wbank\\contracts\\node_modules\\@openzeppelin\\contracts'

# Write standalone WTC contract with ERC20 implemented inline
standalone_wtc = '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract WTC {
    string public name = "WCoins Token";
    string public symbol = "WTC";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    address public bridgeAddress;
    uint256 public constant MAX_SUPPLY = 100_000_000 * 10 ** 18;

    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    address public owner;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event BridgeUpdated(address indexed oldBridge, address indexed newBridge);
    event TokensMinted(address indexed to, uint256 amount, string fromChain);
    event TokensBurned(address indexed from, uint256 amount, string toChain);

    modifier onlyOwner() { require(msg.sender == owner, "only owner"); _; }
    modifier onlyBridge() { require(msg.sender == bridgeAddress, "only bridge"); _; }

    constructor() {
        owner = msg.sender;
        _mint(msg.sender, 10_000_000 * 10 ** 18);
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        require(to != address(0), "zero address");
        require(balanceOf[msg.sender] >= amount, "insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) external returns (bool) {
        require(allowance[from][msg.sender] >= amount, "insufficient allowance");
        require(balanceOf[from] >= amount, "insufficient balance");
        allowance[from][msg.sender] -= amount;
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
        return true;
    }

    function _mint(address to, uint256 amount) internal {
        totalSupply += amount;
        balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);
    }

    function _burn(address from, uint256 amount) internal {
        require(balanceOf[from] >= amount, "insufficient balance");
        totalSupply -= amount;
        balanceOf[from] -= amount;
        emit Transfer(from, address(0), amount);
    }

    function mintByBridge(address to, uint256 amount, string calldata fromChain) external onlyBridge {
        require(totalSupply + amount <= MAX_SUPPLY, "max supply");
        _mint(to, amount);
        emit TokensMinted(to, amount, fromChain);
    }

    function burnByBridge(uint256 amount, string calldata toChain) external {
        _burn(msg.sender, amount);
        emit TokensBurned(msg.sender, amount, toChain);
    }

    function setBridge(address _b) external onlyOwner {
        require(_b != address(0), "invalid");
        emit BridgeUpdated(bridgeAddress, _b);
        bridgeAddress = _b;
    }
}
'''
with open('E:\\wbank\\contracts\\WTC.sol', 'w') as f:
    f.write(standalone_wtc)
print('  [OK] WTC.sol rewritten without imports')

# Standalone bridge
standalone_bridge = '''// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

interface IWTC {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
    function mintByBridge(address to, uint256 amount, string calldata fromChain) external;
    function owner() external view returns (address);
}

contract WTCBridge {
    IWTC public wtcToken;
    uint256 public bridgeFee;
    bool public paused;
    address public owner;

    mapping(address => bool) public relayers;
    mapping(address => uint256) public nonces;

    event TokensLocked(address indexed user, uint256 amount, uint256 targetChainId, string chainName, uint256 nonce, uint256 timestamp);
    event TokensUnlocked(address indexed user, uint256 amount, uint256 sourceChainId, string chainName, uint256 nonce, address indexed relayer);

    modifier onlyRelayer() { require(relayers[msg.sender], "only relayer"); _; }
    modifier onlyOwner() { require(msg.sender == owner, "only owner"); _; }

    constructor(address _wtc) {
        require(_wtc != address(0), "invalid");
        wtcToken = IWTC(_wtc);
        owner = msg.sender;
        relayers[msg.sender] = true;
    }

    function bridgeOut(uint256 amount, uint256 targetChainId, string calldata chainName) external {
        require(!paused, "paused");
        require(amount > 0, "amount > 0");
        require(amount <= wtcToken.balanceOf(msg.sender), "insufficient balance");
        uint256 fee = (amount * bridgeFee) / 10000;
        uint256 bridgeAmount = amount - fee;
        wtcToken.transferFrom(msg.sender, address(this), amount);
        if (fee > 0) wtcToken.transfer(owner, fee);
        uint256 nonce = nonces[msg.sender]++;
        emit TokensLocked(msg.sender, bridgeAmount, targetChainId, chainName, nonce, block.timestamp);
    }

    function completeBridgeIn(address user, uint256 amount, uint256 sourceChainId, string calldata chainName, uint256 userNonce) external onlyRelayer {
        require(!paused, "paused");
        wtcToken.mintByBridge(user, amount, chainName);
        emit TokensUnlocked(user, amount, sourceChainId, chainName, userNonce, msg.sender);
    }

    function setPaused(bool p) external onlyOwner { paused = p; }
    function setFee(uint256 f) external onlyOwner { require(f <= 1000, "max 10%"); bridgeFee = f; }
    function addRelayer(address r) external onlyOwner { relayers[r] = true; }
    function removeRelayer(address r) external onlyOwner { relayers[r] = false; }
    function emergencyWithdraw() external onlyOwner {
        uint256 b = wtcToken.balanceOf(address(this));
        require(b > 0); wtcToken.transfer(owner, b);
    }
}
'''
with open('E:\\wbank\\contracts\\WTCBridge.sol', 'w') as f:
    f.write(standalone_bridge)
print('  [OK] WTCBridge.sol rewritten without imports')

# 3. Try to compile and deploy
print('\n[3/4] Deploying WTC Token...')
try:
    from solcx import compile_files, install_solc
    install_solc('0.8.20')

    cd = 'E:\\wbank\\contracts'
    compiled = compile_files(
        [os.path.join(cd, 'WTC.sol'), os.path.join(cd, 'WTCBridge.sol')],
        solc_version='0.8.20',
        output_values=['abi', 'bin']
    )

    from web3 import Web3
    w3 = Web3(Web3.HTTPProvider('https://ethereum-sepolia.publicnode.com'))

    if not w3.is_connected():
        print('  [FAIL] Cannot connect to Sepolia RPC')
        sys.exit(1)

    print(f'  Connected to Sepolia (block {w3.eth.block_number})')

    # Fund wallet check
    deployer = Account.from_key(pk)
    bal = w3.eth.get_balance(deployer.address)
    print(f'  Deployer balance: {w3.from_wei(bal, "ether")} ETH')

    if bal < 10000000000000000:  # 0.01 ETH
        print('\n  ⚠️ Need Sepolia ETH! Send to:')
        print(f'     {deployer.address}')
        print('\n  Get free ETH from:')
        print('  • https://www.alchemy.com/faucets/ethereum-sepolia')
        print('  • https://sepolia-faucet.pk910.de/ (PoW faucet - no login)')
        print('  • https://cloud.google.com/application/web3/faucet/ethereum/sepolia')
        print()

        # Try PoW faucet
        print('  Trying PoW faucet (sepolia-faucet.pk910.de)...')
        try:
            import requests
            # This PoW faucet doesn't need captcha
            r = requests.post('https://sepolia-faucet.pk910.de/api/claim', json={
                'address': deployer.address,
                'referralCode': ''
            }, timeout=30)
            print(f'  Faucet response: {r.text[:100]}')
            time.sleep(5)
            new_bal = w3.eth.get_balance(deployer.address)
            print(f'  Balance after claim: {w3.from_wei(new_bal, "ether")} ETH')
        except Exception as e:
            print(f'  Faucet error: {e}')

    # Deploy if enough balance
    bal = w3.eth.get_balance(deployer.address)
    if bal >= 10000000000000000:
        print(f'\n  Deploying WTC Token...')

        wtc_info = None
        for path, info in compiled.items():
            if 'WTC' in path and 'Bridge' not in path:
                wtc_info = info
                break

        if not wtc_info:
            print('  [FAIL] WTC contract not found in compiled output')
            sys.exit(1)

        WTC = w3.eth.contract(abi=wtc_info['abi'], bytecode=wtc_info['bin'])
        tx = WTC.constructor().build_transaction({
            'from': deployer.address,
            'nonce': w3.eth.get_transaction_count(deployer.address),
            'gas': 2000000,
            'gasPrice': w3.eth.gas_price,
            'chainId': 11155111
        })
        signed = deployer.sign_transaction(tx)
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        wtc_addr = receipt.contractAddress
        print(f'  ✅ WTC Token deployed: {wtc_addr}')

        # Deploy Bridge
        print('\n  Deploying WTCBridge...')
        bridge_info = None
        for path, info in compiled.items():
            if 'Bridge' in path:
                bridge_info = info
                break

        if bridge_info:
            BR = w3.eth.contract(abi=bridge_info['abi'], bytecode=bridge_info['bin'])
            tx2 = BR.constructor(wtc_addr).build_transaction({
                'from': deployer.address,
                'nonce': w3.eth.get_transaction_count(deployer.address),
                'gas': 2000000,
                'gasPrice': w3.eth.gas_price,
                'chainId': 11155111
            })
            signed2 = deployer.sign_transaction(tx2)
            tx_hash2 = w3.eth.send_raw_transaction(signed2.raw_transaction)
            receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2, timeout=120)
            bridge_addr = receipt2.contractAddress
            print(f'  ✅ Bridge deployed: {bridge_addr}')

            # Configure bridge
            wtc = w3.eth.contract(address=wtc_addr, abi=wtc_info['abi'])
            current = wtc.functions.bridgeAddress().call()
            if current != bridge_addr:
                tx3 = wtc.functions.setBridge(bridge_addr).build_transaction({
                    'from': deployer.address,
                    'nonce': w3.eth.get_transaction_count(deployer.address),
                    'gas': 50000,
                    'gasPrice': w3.eth.gas_price,
                    'chainId': 11155111
                })
                signed3 = deployer.sign_transaction(tx3)
                w3.eth.send_raw_transaction(signed3.raw_transaction)
                print('  ✅ Bridge configured in WTC')

        # Save deployment info
        artifacts = {
            'network': 'sepolia',
            'chain_id': 11155111,
            'wtc': {'address': wtc_addr},
            'bridge': {'address': bridge_addr if 'bridge_addr' in dir() else ''}
        }
        os.makedirs(os.path.join(cd, 'deployments'), exist_ok=True)
        with open(os.path.join(cd, 'deployments', 'sepolia.json'), 'w') as f:
            json.dump(artifacts, f, indent=2)

        # Update wbank_web3.py with real contract address
        w3_path = 'E:\\wbank\\wbank_web3.py'
        wbank_w3 = open(w3_path, 'r', encoding='utf-8').read()
        wbank_w3 = wbank_w3.replace(
            'WTC_CONTRACT_ADDRESS = "0x0000000000000000000000000000000000000000"',
            f'WTC_CONTRACT_ADDRESS = "{wtc_addr}"'
        )
        open(w3_path, 'w', encoding='utf-8').write(wbank_w3)
        print(f'\n  ✅ wbank_web3.py updated with WTC address: {wtc_addr}')

        print(f'\n  View on Etherscan: https://sepolia.etherscan.io/address/{wtc_addr}')
    else:
        print(f'\n  [SKIP] Not enough ETH to deploy (need ~0.01 ETH)')
        print(f'  Send ETH to: {deployer.address}')
        print(f'  Then run: python E:\\wbank\\contracts\\deploy_contracts.py --network sepolia')

except ImportError as e:
    print(f'  [ERROR] {e}')
    print('  Installing dependencies...')
    os.system(f'{sys.executable} -m pip install web3 eth-account py-solc-x')
    print('  Re-run this script after installation')

# 4. Update deploy_contracts.py default
print('\n[4/4] Updating deploy script default...')
dc = open('E:\\wbank\\contracts\\deploy_contracts.py', 'r', encoding='utf-8').read()
if 'eth-mainnet' in dc and 'DEFAULT_NETWORK' in dc:
    dc = dc.replace('DEFAULT_NETWORK = "eth-mainnet"', 'DEFAULT_NETWORK = "sepolia"')
    open('E:\\wbank\\contracts\\deploy_contracts.py', 'w', encoding='utf-8').write(dc)
    print('  [OK] Default network changed to sepolia')

print('\n=== Done ===')
