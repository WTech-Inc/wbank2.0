import urllib.request, sys

for path in ['/admin', '/admin/', '/admin/dashboard', '/admin/login']:
    try:
        r = urllib.request.urlopen('http://localhost:8080' + path, timeout=5)
        sys.stdout.write(f'{path}: {r.status} ({len(r.read())} bytes)\n')
    except urllib.request.HTTPError as e:
        sys.stdout.write(f'{path}: HTTP {e.code}\n')
    except Exception as e:
        sys.stdout.write(f'{path}: Error {e}\n')
sys.stdout.flush()
