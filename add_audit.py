# Add audit log routes and admin improvements to main.py

with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================
# 1. Add new audit log function right after the existing log_audit
# ============================================================

# Find the end of existing log_audit function
old_func = '''def log_audit(action, user, amount, reviewer, detail=None):
  """Write audit log entry to database."""
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
    pass  # audit log failure should not crash the app'''

new_func = '''def log_audit(action, user, amount, reviewer, detail=None):
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
  except Exception:
    db.session.rollback()'''

content = content.replace(old_func, new_func)

# ============================================================
# 2. Admin routes - find startup section and insert before it
# ============================================================

admin_routes = """

# ============================================================
# Audit Log & Admin Panel Routes
# ============================================================

@app.route("/admin")
def admin_login_page():
    \"\"\"Admin login page.\"\"\"
    return render_template("admin/index.html")

@app.route("/admin/login", methods=["POST"])
def admin_login():
    \"\"\"Admin login handler.\"\"\"
    user = request.form.get("user")
    pw = request.form.get("pw")
    if user in users and check_password_hash(users[user], pw):
        session["admin_user"] = user
        session.permanent = True
        write_audit_log("ADMIN_LOGIN", user, "管理員登入成功", request)
        return redirect("/admin/dashboard")
    write_audit_log("ADMIN_LOGIN_FAIL", user, "管理員登入失敗", request)
    flash("帳號或密碼錯誤", "error")
    return redirect("/admin")

@app.route("/admin/logout")
def admin_logout():
    \"\"\"Admin logout.\"\"\"
    admin_user = session.pop("admin_user", None)
    if admin_user:
        write_audit_log("ADMIN_LOGOUT", admin_user, "管理員登出", request)
    session.clear()
    flash("已登出", "info")
    return redirect("/admin")

@app.route("/admin/dashboard")
def admin_dashboard():
    \"\"\"Admin dashboard page.\"\"\"
    if "admin_user" not in session:
        return redirect("/admin")
    return render_template("admin/index.html", admin_user=session["admin_user"])

@app.route("/admin/api/stats")
def admin_api_stats():
    \"\"\"Get dashboard statistics.\"\"\"
    if "admin_user" not in session:
        return jsonify({"error": "未登錄"}), 401
    try:
        total_users = wbankwallet.query.count()
        pending_kyc = wbankkyc.query.count()
        total_records = wbankrecord.query.count()
        try:
            audit_count = audit_log.query.count()
        except:
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
    \"\"\"Get audit log entries as JSON.\"\"\"
    if "admin_user" not in session:
        return jsonify({"error": "未登錄"}), 401
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
            "total": total,
            "page": page,
            "per_page": per_page,
            "entries": [{
                "id": e.id,
                "username": e.username,
                "action": e.action,
                "detail": e.detail,
                "ip_address": e.ip_address,
                "timestamp": e.timestamp.strftime("%Y/%m/%d %H:%M:%S") if e.timestamp else ""
            } for e in entries]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/users")
def admin_api_users():
    \"\"\"Get users list as JSON.\"\"\"
    if "admin_user" not in session:
        return jsonify({"error": "未登錄"}), 401
    try:
        users_list = wbankwallet.query.order_by(wbankwallet.username).all()
        return jsonify([{
            "username": u.username,
            "balance": u.balance,
            "verify": u.verify,
            "role": u.role,
            "accnumber": u.accnumber,
            "email": u.email,
            "sub": u.sub
        } for u in users_list])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/verify_user", methods=["POST"])
def admin_api_verify_user():
    \"\"\"Verify a user account.\"\"\"
    if "admin_user" not in session:
        return jsonify({"error": "未登錄"}), 401
    try:
        username = request.json.get("username")
        user = wbankwallet.query.filter_by(username=username).first()
        if user:
            user.verify = "yes"
            user.role = "user"
            db.session.commit()
            write_audit_log("ADMIN_VERIFY_USER", session["admin_user"],
                          f"已驗證用戶: {username}", request)
            return jsonify({"success": True})
        return jsonify({"error": "用戶不存在"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/freeze_user", methods=["POST"])
def admin_api_freeze_user():
    \"\"\"Freeze/unfreeze a user account.\"\"\"
    if "admin_user" not in session:
        return jsonify({"error": "未登錄"}), 401
    try:
        username = request.json.get("username")
        user = wbankwallet.query.filter_by(username=username).first()
        if user:
            if user.sub and "凍結" in str(user.sub):
                user.sub = None
                action_text = "解凍"
            else:
                user.sub = "凍結：由管理員操作"
                action_text = "凍結"
            db.session.commit()
            write_audit_log(f"ADMIN_{action_text}_USER", session["admin_user"],
                          f"{action_text}用戶: {username}", request)
            return jsonify({"success": True})
        return jsonify({"error": "用戶不存在"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/update_balance", methods=["POST"])
def admin_api_update_balance():
    \"\"\"Update user balance.\"\"\"
    if "admin_user" not in session:
        return jsonify({"error": "未登錄"}), 401
    try:
        username = request.json.get("username")
        amount = request.json.get("amount", 0, type=int)
        user = wbankwallet.query.filter_by(username=username).first()
        if user:
            old_balance = user.balance
            user.balance = str(int(user.balance) + amount)
            db.session.commit()
            write_audit_log("ADMIN_UPDATE_BALANCE", session["admin_user"],
                          f"用戶: {username}, 舊餘額: {old_balance}, 新餘額: {user.balance}, 變動: {amount}", request)
            return jsonify({"success": True, "new_balance": user.balance})
        return jsonify({"error": "用戶不存在"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

"""

# Insert before startup section
startup_marker = '# ═══════════════════════════════════════════════\n# Startup\n# ═══════════════════════════════════════════════'
startup_idx = content.find(startup_marker)
if startup_idx < 0:
    # Try alternate
    startup_marker = '# Startup\n# ════════════════════════════════'
    startup_idx = content.find(startup_marker)

if startup_idx > 0:
    content = content[:startup_idx] + admin_routes + '\n' + content[startup_idx:]
else:
    print('ERROR: Could not find startup section')
    exit(1)

# ============================================================
# Write it back
# ============================================================
with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done')
print(f'Size: {len(content)} bytes')
