import sys
with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()
# Check for key functions
for kw in ['def log_audit', '@socketio.on("trade")', '@socketio.on("friedBot")',
           '@socketio.on("tradeBot")', '/wcoins/data', 'handle_transfer', 'handle_nfc']:
    sys.stdout.write(f'{kw}: {kw in content}\n')
sys.stdout.write(f'Size: {len(content)} bytes\n')
sys.stdout.flush()
