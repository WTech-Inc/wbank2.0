"""Add write_audit_log function back to main.py"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Check if write_audit_log already exists
if 'def write_audit_log' in m:
    print('[OK] write_audit_log already exists')
else:
    # Add the function before admin routes
    admin_idx = m.find("=== Admin Panel Routes ===")
    if admin_idx < 0:
        admin_idx = m.find("def admin_login_page")

    audit_func = '''

def write_audit_log(action, username, detail=None, request_obj=None):
    """Write audit log to audit_log table."""
    try:
        ip = None
        if request_obj:
            ip = request_obj.remote_addr
            xf = request_obj.headers.get('X-Forwarded-For')
            if xf:
                ip = xf.split(',')[0].strip()
        try:
            tz = pytz.timezone('Asia/Taipei')
            utc_time = datetime.datetime.now(pytz.timezone('UTC'))
            local_time = utc_time.astimezone(tz)
        except:
            local_time = datetime.datetime.now()
        db.session.add(audit_log(
            username=str(username) if username else 'system',
            action=str(action),
            detail=str(detail) if detail else None,
            ip_address=str(ip) if ip else None,
            timestamp=local_time
        ))
        db.session.commit()
    except Exception:
        db.session.rollback()

'''

    if admin_idx > 0:
        m = m[:admin_idx] + audit_func + m[admin_idx:]
        print('[OK] write_audit_log function added')
    else:
        # Add near the end before start_web
        idx = m.find("def start_web():")
        if idx > 0:
            m = m[:idx] + audit_func + m[idx:]
            print('[OK] write_audit_log added before start_web')

    open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

    import py_compile
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('[OK] Syntax OK')

print('\nRestart server')
