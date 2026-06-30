"""Fix the backup main.py - remove Flask-Admin code and add our routes"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
orig_size = len(m)

# Remove Flask-Admin lines (lines 258-275 roughly)
# Pattern: admin = Admin(...) and admin.add_view(...)
import re

# Remove Flask-Admin initialization
m = re.sub(
    r"admin = Admin\(.*?\).*?\n.*?admin\.add_view\(.*?\).*?\n",
    '',
    m,
    flags=re.DOTALL
)

# Remove any remaining walletView references
m = m.replace('walletView', '')  # Remove references

# Also remove the import if it exists
m = re.sub(r"from flask_admin.*?\n", '', m)
m = re.sub(r"import flask_admin.*?\n", '', m)
m = re.sub(r"app\.config\['FLASK_ADMIN.*?\n", '', m)

print(f'Size: {orig_size} -> {len(m)}')

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax: OK')
except py_compile.PyCompileError as e:
    print(f'Syntax: {e}')
    # Try to find what's wrong
    lines = m.split('\n')
    for i, line in enumerate(lines):
        if 'walletView' in line or 'Admin(' in line:
            print(f'  Line {i+1}: {line.strip()[:100]}')

# Check if our routes are still there
print(f'/auth/reg: {"YES" if "/auth/reg" in m else "NO"}')
print(f'register_page: {"YES" if "def register_page" in m else "NO"}')

# Add routes if missing
if 'def register_page' not in m:
    print('Routes missing - re-adding...')
    new_routes = '''

@app.route("/auth/reg", methods=["GET"])
def register_page():
    return render_template("wbank/register.html", current_year=2222)

@app.route("/auth/reg", methods=["POST"])
def register_submit():
    try:
        u = request.form.get("username","").strip().lower()
        pw = request.form.get("password","").strip()
        fn = request.form.get("fname","").strip()
        idn = request.form.get("id_number","").strip()
        ph = request.form.get("phone","").strip()
        em = request.form.get("email","").strip()
        addr = request.form.get("address","").strip()
        car = request.form.get("career","").strip()
        if not u or not pw: return jsonify({"error":"填写用户名密码"}),400
        if len(pw) < 6: return jsonify({"error":"密码至少6位"}),400
        if wbankwallet.query.filter_by(username=u).first(): return jsonify({"error":"用户名已被注册"}),400
        import time as _t
        nu = wbankwallet(username=u,password=pw,email=em,
            accnumber="WB"+str(int(_t.time()))[-8:],balance="0",role="user",sub="active",verify="pending")
        db.session.add(nu); db.session.flush()
        from sqlalchemy import text
        db.session.execute(text("INSERT INTO wbankkyc (username,fname,id_number,address,career,phone,email,status,submitted_at) VALUES(:u,:fn,:idn,:addr,:car,:ph,:em,:st,:ts)"),{"u":u,"fn":fn,"idn":idn,"addr":addr,"car":car,"ph":ph,"em":em,"st":"pending","ts":datetime.datetime.now()})
        db.session.commit()
        session["username"]=u; session["role"]="user"
        try: write_audit_log("USER_REGISTER",u,"New KYC reg",request)
        except: pass
        return jsonify({"success":True,"message":"注册成功!KYC审核中","redirect":"/wbank/client"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":"系统错误:"+str(e)}),500
'''

    insert_at = m.find("def start_web():")
    if insert_at < 0: insert_at = len(m)
    m = m[:insert_at] + new_routes + m[insert_at:]
    print('Routes re-added')

open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

# Final syntax check
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Final syntax: OK')
except py_compile.PyCompileError as e:
    print(f'Final syntax: {e}')
