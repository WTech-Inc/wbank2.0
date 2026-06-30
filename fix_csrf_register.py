import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Add @csrf.exempt to register_submit
old = '''@app.route("/auth/reg", methods=["POST"])
def register_submit():'''
new = '''@app.route("/auth/reg", methods=["POST"])
@csrf.exempt
def register_submit():'''

if old in m:
    m = m.replace(old, new)
    open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)
    print('[OK] @csrf.exempt added to register_submit')

    import py_compile
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('[OK] Syntax OK')
else:
    print('[WARN] Pattern not found')
    # Debug
    idx = m.find('def register_submit')
    if idx >= 0:
        print('Context:', m[idx-50:idx+50])
