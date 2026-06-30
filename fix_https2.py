with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the HTTPS function to use app.run directly
old_https = '''    def run_https():
        context = sslmod.SSLContext(sslmod.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        print(f"[+] HTTPS on 0.0.0.0:{HTTPS_PORT}")
        # Use werkzeug directly for HTTPS to avoid eventlet issues
        from flask import Flask
        from werkzeug.serving import run_simple
        run_simple("0.0.0.0", HTTPS_PORT, app,
                   ssl_context=context,
                   use_debugger=False, use_reloader=False)'''

new_https = '''    def run_https():
        context = sslmod.SSLContext(sslmod.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        print(f"[+] HTTPS on 0.0.0.0:{HTTPS_PORT}")
        # Use app.run with SSL context directly
        app.run(host="0.0.0.0", port=HTTPS_PORT, ssl_context=context,
                debug=False, use_reloader=False)'''

content = content.replace(old_https, new_https)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
