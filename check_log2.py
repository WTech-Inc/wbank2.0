import sys
sys.stdout.reconfigure(encoding='utf-8')
log = open('E:\\wbank\\run.log', 'rb').read()
print(f'Log size: {len(log)} bytes')
print('---')
print(log.decode('utf-8', 'replace')[-1500:])
