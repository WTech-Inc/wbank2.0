"""Test SSL cert loading on the server"""
import ssl, sys
try:
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain("E:/wbank/cert.pem", "E:/wbank/key.pem")
    print("OK - cert and key load successfully")
    # Verify cert
    cert = ctx.get_ca_certs()
    print(f"CA certs: {len(cert)}")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
