import sys
sys.stdout.reconfigure(encoding='utf-8')

# Check .env file
with open('E:\\wbank\\.env', 'r') as f:
    content = f.read()
print(f'Raw content: {repr(content)}')

# Extract key
for line in content.split('\n'):
    if 'DEPLOYER_PRIVATE_KEY' in line:
        key = line.split('=')[1].strip()
        print(f'Extracted key: {repr(key)}')
        print(f'Length: {len(key)}')
        print(f'Starts with 0x: {key.startswith("0x")}')
        print(f'Hex chars only: {all(c in "0123456789abcdefABCDEF" for c in key.replace("0x",""))}')
