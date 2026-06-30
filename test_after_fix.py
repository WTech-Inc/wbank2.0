"""Test all routes after Flask(__name__) fix"""
import ssl, urllib.request
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

tests = ["/", "/wbank/auth/v1", "/wbank/web3/info", "/wbank/home"]
for path in tests:
    try:
        r = urllib.request.urlopen(f"https://127.0.0.1:9001{path}", context=ctx, timeout=5)
        body = r.read()
        print(f"{path:30s} {r.status} ({len(body)} bytes)")
        if r.status == 200 and len(body) > 100:
            print(f"  FIRST 100: {body[:100]}")
    except urllib.error.HTTPError as e:
        body = e.read()
        print(f"{path:30s} {e.code} ({len(body)} bytes)")
        if e.code == 500:
            print(f"  ERROR: {body.decode('utf-8','replace')[:200]}")
    except Exception as e:
        print(f"{path:30s} ERROR: {e}")
