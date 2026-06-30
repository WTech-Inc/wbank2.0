"""Fix CSRF exemption for web3 blueprint"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Check if CSRF exemption already exists
if 'csrf.exempt(web3_bp' in m or 'web3_info._csrf_exempt' in m:
    print('[OK] CSRF exemption already exists')
else:
    # Find csrf = CSRFProtect(app) or similar
    if 'CSRFProtect(app)' in m:
        # Add exemption after CSRF initialization
        old = 'csrf = CSRFProtect(app)'
        new = old + '\n# CSRF exempt for web3 blueprint\nfor _fn in ["web3_info","web3_send","web3_history"]:\n    try:\n        vf = web3_bp.view_functions.get(_fn)\n        if vf:\n            csrf.exempt(vf)\n    except:\n        pass\n'
        if old in m:
            m = m.replace(old, new)
            print('[OK] CSRF exemption added')
        else:
            print('[WARN] Could not find CSRFProtect(app)')
            # Try alternative
            for line in m.split('\n'):
                if 'CSRFProtect' in line and 'app' in line:
                    print(f'  Found: {line.strip()[:100]}')
    else:
        print('[WARN] No CSRFProtect found')

    open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('[OK] Syntax OK')
except py_compile.PyCompileError as e:
    print(f'[FAIL] {e}')

print('\n=== Restart needed ===')
