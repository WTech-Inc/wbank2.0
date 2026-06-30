"""Fix CSRF exemption for web3 - add @csrf.exempt to each view function directly"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Fix wbank_web3.py - add @csrf.exempt to each route
w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()

# Add csrf import and exempt decorators
# The web3_bp is a Blueprint, so we need to handle CSRF differently
# Method 1: Add exempt in main.py (already done but might not work)
# Method 2: Use @csrf.exempt directly on each route function

# Let's check main.py first
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Find all ways to exempt web3 routes from CSRF
# Method: Make the entire web3 blueprint csrf exempt
exempt_code = '''

# CSRF exempt for all web3 blueprint routes
try:
    for rule in app.url_map.iter_rules():
        if rule.endpoint and rule.endpoint.startswith('web3_bp.'):
            vf = app.view_functions.get(rule.endpoint)
            if vf:
                csrf.exempt(vf)
except:
    pass
'''

# Insert before the startup section
insert_at = m.find("def start_web():")
if insert_at > 0:
    m = m[:insert_at] + exempt_code + m[insert_at:]

    open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

    import py_compile
    try:
        py_compile.compile('E:\\wbank\\main.py', doraise=True)
        print('[OK] Method: exempt all web3_bp routes')
    except py_compile.PyCompileError as e:
        print(f'[FAIL] {e}')
else:
    print('[WARN] Could not find insertion point')
