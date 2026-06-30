import sys
sys.stdout.reconfigure(encoding='utf-8')
print(open('E:\\wbank\\run.log', 'rb').read()[-3000:].decode('utf-8', 'replace'))
