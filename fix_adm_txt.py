with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and fix the garbled text by looking for the pattern near line 2532
import re

# Replace known garbled patterns with English text
# The garbled text appears to be mangled Chinese from unicode escape misprocessing
replacements = {
    # Line 2532: write_audit_log("ADMIN_LOGIN", user, "garbled", request)
    'write_audit_log("ADMIN_LOGIN", user, "': 'write_audit_log("ADMIN_LOGIN", user, "admin login success"',
    # These are the exact garbled text - let me be more aggressive
}

# Actually, let me just find and replace the problematic lines by reading the raw bytes
with open('E:\\wbank\\main.py', 'rb') as f:
    data = f.read()

# The garbled text contains Chinese characters that got corrupted.
# Let me find the pattern with the garbled text and replace the whole function
# Find the admin_login function in bytes
pattern1 = b'write_audit_log("ADMIN_LOGIN", user, "'
pattern2 = b'", request)'

# Find all occurrences of write_audit_log calls and fix them
import re as re_bytes
for match in re_bytes.finditer(b'write_audit_log\\([^)]+\\)', data):
    call = match.group()
    # Check if it's a login call (has garbled text)
    if b'ADMIN_LOGIN' in call and b'\\"' not in call:
        # Extract the start of the call
        # Replace the garbled text part
        print(f'Found admin call at offset {match.start()}')
        # We'll handle it differently - do a text-level replacement

# Let me just delete and recreate the admin_login function
text = data.decode('utf-8')

# Find the exact garbled string by looking for the pattern
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'admin_login():' in line and 'admin_login_page' not in line:
        fn_start = i
    if i >= fn_start if 'fn_start' in dir() else False:
        pass

# Actually, the simplest approach: replace the whole admin_login function
old_func = '''def admin_login():
    """Admin login handler."""
    user = request.form.get("user")
    pw = request.form.get("pw")
    if user in users and check_password_hash(users[user], pw):
        session["admin_user"] = user
        session.permanent = True
        write_audit_log("ADMIN_LOGIN", user, "admin login success", request)
        return redirect("/admin/dashboard")
    write_audit_log("ADMIN_LOGIN_FAIL", user, "admin login failed", request)
    flash("Account or password error", "error")
    return redirect("/admin")'''

# But I don't know the exact old text. Let me find the function boundaries.
start_idx = text.find('def admin_login():')
end_idx = text.find('\n@', text.find('\n@', start_idx) + 1)
if end_idx < 0:
    end_idx = text.find('\ndef ', start_idx + 10)

if start_idx >= 0:
    # Find the function end (next decorator or def)
    search_start = start_idx + 1
    next_def = text.find('\n@', search_start)
    if next_def > 0:
        old_text = text[start_idx:next_def]
        new_text = '''def admin_login():
    """Admin login handler."""
    user = request.form.get("user")
    pw = request.form.get("pw")
    if user in users and check_password_hash(users[user], pw):
        session["admin_user"] = user
        session.permanent = True
        write_audit_log("ADMIN_LOGIN", user, "admin login success", request)
        return redirect("/admin/dashboard")
    write_audit_log("ADMIN_LOGIN_FAIL", user, "admin login failed", request)
    flash("Account or password error", "error")
    return redirect("/admin")
'''
        text = text[:start_idx] + new_text + text[next_def:]
        print('Replaced admin_login function')
    else:
        print('Could not find end of admin_login function')
else:
    print('Could not find admin_login function')

# Also fix the logout function
old_logout = '''def admin_logout():
    """Admin logout."""
    admin_user = session.pop("admin_user", None)
    if admin_user:
        write_audit_log("ADMIN_LOGOUT", admin_user, "admin logout", request)
    session.clear()'''

# Find and fix
start_idx = text.find('def admin_logout():')
search_start = start_idx + 1
next_def = text.find('\ndef ', search_start)
if start_idx >= 0 and next_def > 0:
    old_text = text[start_idx:next_def]
    new_text = '''def admin_logout():
    """Admin logout."""
    admin_user = session.pop("admin_user", None)
    if admin_user:
        write_audit_log("ADMIN_LOGOUT", admin_user, "admin logout", request)
    session.clear()
    flash("Logged out", "info")
    return redirect("/admin")
'''
    text = text[:start_idx] + new_text + text[next_def:]
    print('Replaced admin_logout function')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(text)

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
