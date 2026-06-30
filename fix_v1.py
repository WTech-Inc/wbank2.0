with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = '''@app.route("/wbank/auth/v1/session",methods=["GET","POST"])
def wbank_v1_auth_session():'''

new = '''@app.route("/wbank/auth/v1/session",methods=["GET","POST"])
@csrf.exempt
def wbank_v1_auth_session():'''

if old in content:
    content = content.replace(old, new)
    with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('CSRF exempt added to V1 login')
else:
    print('Could not find exact text')
    # Show exact line for debugging
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'v1/session' in line:
            print(f'Line {i+1}: {repr(line)}')
