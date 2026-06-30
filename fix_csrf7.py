with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the old broken csrf exempt block
old = """# CSRF exemption for web3 blueprint (by endpoint string)
csrf.exempt('web3_bp.web3_info')
csrf.exempt('web3_bp.web3_send')
csrf.exempt('web3_bp.web3_history')"""

new = """# CSRF exemption for web3 routes - override via restirct_routes
pass"""

content = content.replace(old, new)

# Add a bypass in restrict_routes to skip csrf for web3
# Find the restrict_routes function
old_rr = """def restrict_routes():
    \"\"\"Restrict all routes except /, /wbank, /wbank/*, /admin/*, /static/*\"\"\"
    path = request.path"""

new_rr = """def restrict_routes():
    \"\"\"Restrict all routes except /, /wbank, /wbank/*, /admin/*, /static/*\"\"\"
    # Bypass CSRF for web3 endpoints
    if request.path.startswith('/wbank/web3/'):
        from flask_wtf.csrf import generate_csrf
        # Set a flag to skip CSRF checking
        request._csrf_disable = True
    path = request.path"""

content = content.replace(old_rr, new_rr)

# Now add another before_request that runs AFTER csrf_protect but before views
# By adding a custom before_request that runs first and sets _csrf_exempt on the view
old_csrf_init = """csrf = CSRFProtect(app)

pass"""

new_csrf_init = """csrf = CSRFProtect(app)

# Disable CSRF for web3 routes dynamically
_orig_csrf_protect = None
for func in app.before_request_funcs.get(None, []):
    if func.__name__ == 'csrf_protect':
        _orig_csrf_protect = func
        break

if _orig_csrf_protect:
    @app.before_request
    def _web3_csrf_bypass():
        if request.path.startswith('/wbank/web3/'):
            # Mark the view function as exempt
            if request.endpoint and request.endpoint in app.view_functions:
                app.view_functions[request.endpoint]._csrf_exempt = True
"""

content = content.replace(old_csrf_init, new_csrf_init)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
