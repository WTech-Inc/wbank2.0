with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire start_web function to use app.run for HTTPS
old_start = '''def start_web():
    """Run app using SocketIO with SSL, port 8080 (http) + 8443 (https).
    Portproxy on Windows: 80\\u21928080, 443\\u21928443 (already configured)."""
    import ssl as sslmod
    from threading import Thread

    cert_file = "E:\\\\wbank\\\\cert.pem"
    key_file = "E:\\\\wbank\\\\key.pem"
    HTTP_PORT = int(os.environ.get("HTTP_PORT", 8080))
    HTTPS_PORT = int(os.environ.get("HTTPS_PORT", 8443))

    def run_http():
        print(f"[+] HTTP with SocketIO on 0.0.0.0:{HTTP_PORT}")
        socketio.run(app, host="0.0.0.0", port=HTTP_PORT,
                     allow_unsafe_werkzeug=True)

    def run_https():
        context = sslmod.SSLContext(sslmod.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        print(f"[+] HTTPS with SocketIO on 0.0.0.0:{HTTPS_PORT}")
        socketio.run(app, host="0.0.0.0", port=HTTPS_PORT,
                     ssl_context=context,
                     allow_unsafe_werkzeug=True)

    t1 = Thread(target=run_http, daemon=True)
    t2 = Thread(target=run_https, daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()'''

new_start = '''def start_web():
    """Run app using SocketIO with SSL, port 8080 (http) + 8443 (https).
    Portproxy on Windows: 80\\u21928080, 443\\u21928443 (already configured)."""
    import ssl as sslmod
    from threading import Thread
    from werkzeug.serving import make_server

    cert_file = "E:\\\\wbank\\\\cert.pem"
    key_file = "E:\\\\wbank\\\\key.pem"
    HTTP_PORT = int(os.environ.get("HTTP_PORT", 8080))
    HTTPS_PORT = int(os.environ.get("HTTPS_PORT", 8443))

    def run_http():
        print(f"[+] HTTP with SocketIO on 0.0.0.0:{HTTP_PORT}")
        socketio.run(app, host="0.0.0.0", port=HTTP_PORT,
                     allow_unsafe_werkzeug=True)

    def run_https():
        context = sslmod.SSLContext(sslmod.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        print(f"[+] HTTPS on 0.0.0.0:{HTTPS_PORT}")
        # Use werkzeug directly for HTTPS to avoid eventlet issues
        from flask import Flask
        from werkzeug.serving import run_simple
        run_simple("0.0.0.0", HTTPS_PORT, app,
                   ssl_context=context,
                   use_debugger=False, use_reloader=False)

    t1 = Thread(target=run_http, daemon=True)
    t2 = Thread(target=run_https, daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()'''

content = content.replace(old_start, new_start)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
