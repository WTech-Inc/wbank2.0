import sys

with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find insertion point: after handle_nfc_detected function and before next section
insert_idx = None
for i, line in enumerate(lines):
    if 'def handle_nfc_detected' in line:
        # Find the end - look for the next function definition
        for j in range(i+1, min(i+60, len(lines))):
            if lines[j].strip().startswith('@') or (lines[j].strip().startswith('def ') and j > i+1):
                insert_idx = j
                break
        break

if insert_idx is None:
    # Fallback: find after the last socketio handler
    for i in range(len(lines)-1, 0, -1):
        if '@socketio.on' in lines[i]:
            insert_idx = i + 1
            break

if insert_idx is None:
    sys.stdout.write('ERROR: Could not find insertion point\n')
    sys.exit(1)

# Functions to insert
new_funcs = '''def log_audit(action, user, amount, reviewer, detail=None):
  """Write audit log entry to wbankrecord (legacy)."""
  try:
    tz = pytz.timezone('Asia/Taipei')
    utc_time = datetime.datetime.now(pytz.timezone('UTC'))
    local_time = utc_time.astimezone(tz)
    db.session.add(wbankrecord(
        username=str(user),
        action=f"[{action}] {detail or ''} \\u8f49\\u5e33\\u65b9:{user} \\u6536\\u6b3e\\u65b9:{reviewer} \\u91d1\\u984d:{amount}",
        time=local_time
    ))
    db.session.commit()
  except Exception:
    pass

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

'''

# Insert functions
lines.insert(insert_idx, new_funcs)
sys.stdout.write(f'Inserted audit log functions at line {insert_idx}\n')

# Now find startup section and insert admin routes
# Find 'def start_web():' or '# Startup'
startup_idx = None
for i, line in enumerate(lines):
    if line.strip() == '# Startup' or 'def start_web():' in line:
        startup_idx = i
        break

if startup_idx is None:
    sys.stdout.write('ERROR: Could not find startup section\n')
    sys.exit(1)

admin_routes = '''
# ============================================================
# Audit Log & Admin Panel Routes
# ============================================================

@app.route("/admin")
@app.route("/admin/")
def admin_login_page():
    """Admin login page."""
    return render_template("admin/index.html")

@app.route("/admin/login", methods=["POST"])
@csrf.exempt
def admin_login():
    """Admin login handler."""
    user = request.form.get("user")
    pw = request.form.get("pw")
    if user in users and check_password_hash(users[user], pw):
        session["admin_user"] = user
        session.permanent = True
        write_audit_log("ADMIN_LOGIN", user, "Admin login success", request)
        return redirect("/admin/dashboard")
    write_audit_log("ADMIN_LOGIN_FAIL", user, "Admin login failed", request)
    flash("Account or password error", "error")
    return redirect("/admin")

@app.route("/admin/logout")
def admin_logout():
    """Admin logout."""
    admin_user = session.pop("admin_user", None)
    if admin_user:
        write_audit_log("ADMIN_LOGOUT", admin_user, "Admin logout", request)
    session.clear()
    flash("Logged out", "info")
    return redirect("/admin")

@app.route("/admin/dashboard")
def admin_dashboard():
    """Admin dashboard page."""
    if "admin_user" not in session:
        return redirect("/admin")
    return render_template("admin/index.html", admin_user=session["admin_user"])

@app.route("/admin/api/stats")
def admin_api_stats():
    """Get dashboard statistics."""
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        total_users = wbankwallet.query.count()
        pending_kyc = wbankkyc.query.count()
        total_records = wbankrecord.query.count()
        try:
            audit_count = audit_log.query.count()
        except Exception:
            audit_count = 0
        return jsonify({
            "total_users": total_users,
            "pending_kyc": pending_kyc,
            "total_records": total_records,
            "audit_count": audit_count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/audit_log")
def admin_api_audit_log():
    """Get audit log entries as JSON."""
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 50, type=int)
        action_filter = request.args.get("action", "")
        username_filter = request.args.get("username", "")
        query = audit_log.query.order_by(audit_log.timestamp.desc())
        if action_filter:
            query = query.filter(audit_log.action.ilike(f"%{action_filter}%"))
        if username_filter:
            query = query.filter(audit_log.username.ilike(f"%{username_filter}%"))
        total = query.count()
        entries = query.offset((page - 1) * per_page).limit(per_page).all()
        return jsonify({
            "total": total, "page": page, "per_page": per_page,
            "entries": [{
                "id": e.id, "username": e.username, "action": e.action,
                "detail": e.detail, "ip_address": e.ip_address,
                "timestamp": e.timestamp.strftime("%Y/%m/%d %H:%M:%S") if e.timestamp else ""
            } for e in entries]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/users")
def admin_api_users():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        users_list = wbankwallet.query.order_by(wbankwallet.username).all()
        return jsonify([{
            "username": u.username, "balance": u.balance, "verify": u.verify,
            "role": u.role, "accnumber": u.accnumber, "email": u.email, "sub": u.sub
        } for u in users_list])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/verify_user", methods=["POST"])
def admin_api_verify_user():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        username = request.json.get("username")
        user = wbankwallet.query.filter_by(username=username).first()
        if user:
            user.verify = "yes"
            user.role = "user"
            db.session.commit()
            write_audit_log("ADMIN_VERIFY_USER", session["admin_user"], f"Verified: {username}", request)
            return jsonify({"success": True})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/freeze_user", methods=["POST"])
def admin_api_freeze_user():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        username = request.json.get("username")
        user = wbankwallet.query.filter_by(username=username).first()
        if user:
            if user.sub and "Freeze" in str(user.sub):
                user.sub = None
                action_text = "Unfrozen"
            else:
                user.sub = "Freeze: by admin"
                action_text = "Frozen"
            db.session.commit()
            write_audit_log(f"ADMIN_{action_text.upper()}", session["admin_user"], f"{action_text}: {username}", request)
            return jsonify({"success": True, "action": action_text})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/update_balance", methods=["POST"])
def admin_api_update_balance():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        username = request.json.get("username")
        amount = request.json.get("amount", 0, type=int)
        user = wbankwallet.query.filter_by(username=username).first()
        if user:
            old_balance = user.balance
            user.balance = str(int(user.balance) + amount)
            db.session.commit()
            write_audit_log("ADMIN_UPDATE_BALANCE", session["admin_user"],
                          f"User: {username}, Old: {old_balance}, New: {user.balance}", request)
            return jsonify({"success": True, "new_balance": user.balance})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

'''

lines.insert(startup_idx, admin_routes)
sys.stdout.write(f'Inserted admin routes at line {startup_idx}\n')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    sys.stdout.write('Syntax OK!\n')
except py_compile.PyCompileError as e:
    sys.stdout.write(f'Syntax Error: {e}\n')
    sys.exit(1)

sys.stdout.flush()
