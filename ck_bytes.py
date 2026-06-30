import hashlib, requests, sys

ak = hashlib.sha256('wtech->wtech888->true'.encode()).hexdigest()
r = requests.get(f'http://localhost:8080/wbank/home?accessKey={ak}', timeout=5)

# Check raw bytes around position 193
raw = r.content
sys.stdout.write(f'Bytes around 193: {raw[185:200].hex(" ")}\n')
# Print as string
sys.stdout.write(f'As string: {raw[185:200]}\n')
# Check the title tag
title_start = raw.find(b'<title>')
title_end = raw.find(b'</title>', title_start)
if title_start >= 0:
    sys.stdout.write(f'Title: {raw[title_start:title_end+8]}\n')

# Also check the /wbank route (which renders wbank.html)
r2 = requests.get('http://localhost:8080/wbank', timeout=5)
sys.stdout.write(f'/wbank status: {r2.status_code}\n')
if r2.status_code == 200:
    raw2 = r2.content
    title_start2 = raw2.find(b'<title>')
    title_end2 = raw2.find(b'</title>', title_start2)
    if title_start2 >= 0:
        sys.stdout.write(f'/wbank Title: {raw2[title_start2:title_end2+8]}\n')

sys.stdout.flush()
