# Phase 2: Add write_audit_log function and admin routes
import py_compile

with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add write_audit_log function after the log_audit function
marker = "    except Exception:\n        pass  # audit log failure should not crash the app"
insert_pos = content.find(marker)
if insert_pos > 0:
    end_of_line = content.find('\n', insert_pos)
    after_func = content.find('\n\n', end_of_line)
    if after_func < 0:
        after_func = end_of_line + 1

    write_audit_func = '''

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
    content = content[:end_of_line+1] + write_audit_func + content[end_of_line+1:]
    print('Added write_audit_log function')
else:
    print('ERROR: Could not find insertion point')
    exit(1)

# 2. Add admin routes before startup section
startup_marker = '# Startup\n# ════════════════════════════════'
idx = content.find(startup_marker)
if idx < 0:
    startup_marker = 'def start_web():'
    idx = content.find(startup_marker)

if idx > 0:
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
@csrf.exempt
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
@csrf.exempt
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
@csrf.exempt
def admin_api_users():
    """Get users list as JSON."""
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
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
@csrf.exempt
def admin_api_verify_user():
    """Verify a user account."""
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        username = request.json.get("username")
        user = wbankwallet.query.filter_by(username=username).first()
        if user:
            user.verify = "yes"
            user.role = "user"
            db.session.commit()
            write_audit_log("ADMIN_VERIFY_USER", session["admin_user"],
                          f"Verified user: {username}", request)
            return jsonify({"success": True})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/freeze_user", methods=["POST"])
@csrf.exempt
def admin_api_freeze_user():
    """Freeze/unfreeze a user account."""
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
            write_audit_log(f"ADMIN_{action_text.upper()}", session["admin_user"],
                          f"{action_text} user: {username}", request)
            return jsonify({"success": True, "action": action_text})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/update_balance", methods=["POST"])
@csrf.exempt
def admin_api_update_balance():
    """Update user balance."""
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
                          f"User: {username}, Old: {old_balance}, New: {user.balance}, Change: {amount}", request)
            return jsonify({"success": True, "new_balance": user.balance})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

'''

    content = content[:idx] + admin_routes + '\n' + content[idx:]
    print('Added admin routes')
else:
    print('ERROR: Could not find startup section')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
