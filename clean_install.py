"""Clean install - use backup as base and apply only what's needed"""
import subprocess, os, time, sys
sys.stdout.reconfigure(encoding='utf-8')

# Step 1: Restore from backup
print('[1/6] Restore main.py from backup...')
import shutil
shutil.copy2('E:\\wbank\\main_backup_discord.py', 'E:\\wbank\\main.py')
print('  OK - restored main.py from backup')

# Step 2: Verify wbank_web3.py ABI fix
print('[2/6] Verify wbank_web3.py...')
w3 = open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8').read()
if 'false' in w3 or 'true' in w3:
    import re
    w3 = re.sub(r'(?<!["\'])false(?!["\'])', 'False', w3)
    w3 = re.sub(r'(?<!["\'])true(?!["\'])', 'True', w3)
    open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8').write(w3)
    print('  OK - ABI fixed')
else:
    print('  OK - no fix needed')

# Step 3: Add register/KYC routes and login link to main.py (simple text injection)
print('[3/6] Add register/KYC routes...')
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# The routes to inject
new_routes = """

# === Registration + KYC Routes ===

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
        if not u or not pw:
            return jsonify({"error":"请填写用户名和密码"}),400
        if len(pw) < 6:
            return jsonify({"error":"密码至少6位"}),400
        if wbankwallet.query.filter_by(username=u).first():
            return jsonify({"error":"用户名已被注册"}),400
        import time as _time
        nu = wbankwallet(username=u, password=pw, email=em,
            accnumber="WB"+str(int(_time.time()))[-8:],
            balance="0", role="user", sub="active", verify="pending")
        db.session.add(nu)
        db.session.flush()
        from sqlalchemy import text
        db.session.execute(
            text("INSERT INTO wbankkyc (username,fname,id_number,address,career,phone,email,status,submitted_at) VALUES (:u,:fn,:idn,:addr,:car,:ph,:em,:st,:ts)"),
            {"u":u,"fn":fn,"idn":idn,"addr":addr,"car":car,"ph":ph,"em":em,"st":"pending","ts":datetime.datetime.now()}
        )
        db.session.commit()
        session["username"] = u
        session["role"] = "user"
        try:
            write_audit_log("USER_REGISTER",u,f"New user registration with KYC",request)
        except:
            pass
        return jsonify({"success":True,"message":"注册成功！KYC审核中","redirect":"/wbank/client"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error":"系统错误: "+str(e)}),500

@app.route("/wbank/kyc/status",methods=["GET"])
def kyc_status():
    u = session.get("username")
    if not u:
        return jsonify({"error":"Not logged in"}),401
    from sqlalchemy import text
    r = db.session.execute(
        text("SELECT fname,status,submitted_at FROM wbankkyc WHERE username=:u"),
        {"u":u}
    ).fetchone()
    if not r:
        return jsonify({"status":"none","message":"尚未提交KYC"})
    sm = {"pending":"KYC审核中","approved":"KYC已通过","rejected":"KYC被拒绝"}
    ts = r[2].strftime("%Y/%m/%d %H:%M") if r[2] else ""
    return jsonify({"status":r[1] or "pending","fname":r[0],"submitted_at":ts,"message":sm.get(r[1],"未知")})
"""

# Inject before the startup section
insert_at = m.find("def start_web():")
if insert_at < 0:
    insert_at = m.find("if __name__")
if insert_at < 0:
    insert_at = len(m)

m = m[:insert_at] + new_routes + "\n" + m[insert_at:]

open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)
print('  OK - routes added')

# Step 4: Add register link to login template
print('[4/6] Add register link to login page...')
tpl = open('E:\\wbank\\templates\\wbank\\login.html', 'r', encoding='utf-8').read()
link = '<div style="text-align:center;margin-top:18px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.06);font-size:13px;color:#94a3b8;"><a href=/auth/reg style="color:#4fc3f7;text-decoration:none;font-weight:600;">立即開户 →</a></div>'
if '</form>' in tpl and '立即開户' not in tpl:
    tpl = tpl.replace('</form>', '</form>\n' + link)
    open('E:\\wbank\\templates\\wbank\\login.html', 'w', encoding='utf-8').write(tpl)
    print('  OK - login link added')
else:
    print('  OK - already has link or no </form>')


# Step 5: Verify syntax
print('[5/6] Verify syntax...')
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('  OK')
except py_compile.PyCompileError as e:
    print(f'  FAIL: {e}')
    sys.exit(1)

# Step 6: Kill and restart
print('[6/6] Restart server...')
subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True, timeout=10)
time.sleep(3)

env = os.environ.copy()
env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
env['HTTP_PORT'] = '8080'
env['HTTPS_PORT'] = '8443'

proc = subprocess.Popen(
    ['python', 'main.py'],
    cwd='E:\\wbank',
    env=env,
    stdout=open('E:\\wbank\\run.log', 'w'),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)
print(f'  Started PID: {proc.pid}')
time.sleep(5)

# Verify
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/NH'], capture_output=True, text=True, timeout=10)
print(f'  Running: {"YES" if "python" in r.stdout else "NO"}')

import urllib.request
for path in ['/', '/auth/reg', '/wbank/auth/v1']:
    try:
        r = urllib.request.urlopen(f'http://localhost:8080{path}', timeout=5)
        print(f'  {path}: HTTP {r.status} OK')
    except urllib.error.HTTPError as e:
        print(f'  {path}: HTTP {e.code}')
    except Exception as e:
        print(f'  {path}: {e}')

# Check log for errors
log = open('E:\\wbank\\run.log', 'r', encoding='utf-8').read()
if 'Traceback' in log:
    lines = log.split('\n')
    errs = [l for l in lines if 'Traceback' in l or 'Error' in l or 'Error' in l]
    print(f'  Log errors: {len(errs)}')
    for e in errs[-3:]:
        print(f'    {e[:150]}')
else:
    print('  Log: OK (no errors)')

print('\n=== Done ===')
