with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''    def run_https():
        context = sslmod.SSLContext(sslmod.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        print(f"[+] HTTPS with SocketIO on 0.0.0.0:{HTTPS_PORT}")
        socketio.run(app, host="0.0.0.0", port=HTTPS_PORT,
                     ssl_context=context,
                     allow_unsafe_werkzeug=True)'''

new_block = '''    def run_https():
        context = sslmod.SSLContext(sslmod.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(cert_file, key_file)
        print(f"[+] HTTPS on 0.0.0.0:{HTTPS_PORT}")
        from werkzeug.serving import make_server
        srv = make_server("0.0.0.0", HTTPS_PORT, app,
                          ssl_context=context, threaded=True)
        srv.serve_forever()'''

if old_block in content:
    content = content.replace(old_block, new_block)
    print('HTTPS block replaced successfully')
else:
    print('ERROR: Could not find old HTTPS block')
    # Debug: show what's actually there
    idx = content.find('def run_https():')
    if idx >= 0:
        print(f'Found at {idx}:')
        print(content[idx:idx+300])

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
