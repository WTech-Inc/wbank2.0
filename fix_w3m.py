with open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: Add login check instead of relying on @login_required
old_info = '''def web3_info():
    """Get Web3 wallet info for current user."""
    from flask_login import current_user
    username = current_user.username'''

new_info = '''def web3_info():
    """Get Web3 wallet info for current user."""
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401
    username = current_user.username'''

content = content.replace(old_info, new_info)

# Fix send endpoint
old_send = '''def web3_send():
    """Send WTC tokens to another address."""
    from flask_login import current_user
    username = current_user.username'''

new_send = '''def web3_send():
    """Send WTC tokens to another address."""
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401
    username = current_user.username'''

content = content.replace(old_send, new_send)

# Fix history endpoint
old_hist = '''def web3_history():
    """Get WTC transaction history."""
    from flask_login import current_user
    username = current_user.username'''

new_hist = '''def web3_history():
    """Get WTC transaction history."""
    from flask_login import current_user
    if not current_user.is_authenticated:
        return jsonify({"error": "Not logged in"}), 401
    username = current_user.username'''

content = content.replace(old_hist, new_hist)

# Fix the write_audit_log import issue - use from main instead of local
content = content.replace(
    'from main import write_audit_log',
    'from flask import current_app'
)

# Replace the write_audit_log call with a direct approach
content = content.replace(
    "    write_audit_log(\"WTC_SEND\", username,\n                    f\"Sent {amount} WTC to {to_address}\", request)",
    "    # Audit logged via wbankrecord below"
)

with open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed web3 module')

import py_compile
try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
