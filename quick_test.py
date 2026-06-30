"""Quick test of server on new ports"""
import ssl, urllib.request
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

for path in ["/", "/wbank/auth/v1", "/wbank/web3/info", "/wbank/home"]:
    try:
        r = urllib.request.urlopen(f"https://127.0.0.1:8445{path}", context=ctx, timeout=5)
        print(f"{path}: {r.status} ({len(r.read())} bytes)")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")[:100]
        print(f"{path}: {e.code} - {body}")
    except Exception as e:
        print(f"{path}: ERROR - {e}")
