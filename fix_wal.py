with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the end of the old log_audit function and add write_audit_log after it
old_log_audit_end = '''    db.session.commit()
  except Exception:
    pass  # audit log failure should not crash the app

'''

# Check if write_audit_log already exists
if 'def write_audit_log' in content:
    print('write_audit_log already exists')
else:
    # Find the end of log_audit function
    idx = content.find("pass  # audit log failure should not crash the app")
    if idx < 0:
        idx = content.find("pass  # audit log failure should not crash")

    if idx > 0:
        # Find the end of that line
        end_line = content.find('\n', idx)
        after_func = content.find('\n\n', end_line)
        if after_func < 0:
            after_func = end_line + 1

        write_audit_func = '''

def write_audit_log(action, username, detail=None, request_obj=None):
  """Write audit log to audit_log table with IP tracking."""
  try:
    ip = None
    if request_obj:
      ip = request_obj.remote_addr
      x_forwarded = request_obj.headers.get('X-Forwarded-For')
      if x_forwarded:
        ip = x_forwarded.split(',')[0].strip()
    tz = pytz.timezone('Asia/Taipei')
    utc_time = datetime.datetime.now(pytz.timezone('UTC'))
    local_time = utc_time.astimezone(tz)
    db.session.add(audit_log(
        username=str(username) if username else 'system',
        action=str(action),
        detail=str(detail) if detail else None,
        ip_address=str(ip) if ip else None,
        timestamp=local_time
    ))
    db.session.commit()
  except Exception as e:
    db.session.rollback()
    print(f'Audit log write error: {e}')

'''
        content = content[:end_line+1] + write_audit_func + content[end_line+1:]
        print('Added write_audit_log function')
    else:
        print('Could not find insertion point')

# Fix garbled Chinese text in admin routes
# The garbled text appears as: "�޲z���n�J���\"
# These are from my original unicode escapes that got decoded wrong
# Let me fix them by replacing known garbled patterns
content = content.replace(
    'write_audit_log("ADMIN_LOGIN", user, "�޲z���n�J���", request)',
    'write_audit_log("ADMIN_LOGIN", user, "Admin login success", request)'
)
content = content.replace(
    'write_audit_log("ADMIN_LOGIN_FAIL", user, "�޲z���n�J����", request)',
    'write_audit_log("ADMIN_LOGIN_FAIL", user, "Admin login failed", request)'
)
content = content.replace(
    'write_audit_log("ADMIN_LOGOUT", admin_user, "�޲z���n�X", request)',
    'write_audit_log("ADMIN_LOGOUT", admin_user, "Admin logout", request)'
)

# Fix flash messages
content = content.replace('flash("�b���αK�X���~", "error")', 'flash("Account or password error", "error")')
content = content.replace('flash("�w�n�X", "info")', 'flash("Logged out", "info")')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
