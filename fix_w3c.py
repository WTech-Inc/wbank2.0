with open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add csrf import after flask imports
content = content.replace(
    'from flask import Blueprint, request, jsonify, session',
    'from flask import Blueprint, request, jsonify, session\nfrom flask_wtf.csrf import CSRFProtect, csrf_exempt'
)

# Add @csrf_exempt to send endpoint (POST)
content = content.replace(
    "@web3_bp.route('/wbank/web3/send', methods=['POST'])\ndef web3_send():",
    "@web3_bp.route('/wbank/web3/send', methods=['POST'])\n@csrf_exempt\ndef web3_send():"
)

with open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')

# Verify
c = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
print('csrf_exempt in file:', 'csrf_exempt' in c)
