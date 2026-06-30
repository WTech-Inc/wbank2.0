"""Add full admin routes + fix CSRF"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Check if /admin routes exist
has_admin_route = "'/admin'" in m or '"/admin"' in m
print(f'Has /admin route: {has_admin_route}')

if not has_admin_route or True:  # Always check
    # Find a good insertion point - before the catch-all route
    catch_all_idx = m.find('@app.route("/<path:template_name>")')
    if catch_all_idx > 0:
        # Insert admin routes before catch-all
        admin_routes = '''

# === Admin Panel Routes ===

@app.route("/admin")
@app.route("/admin/")
def admin_login_page():
    """Admin login page."""
    return render_template("admin/index.html")

@app.route("/admin/login", methods=["POST"])
@csrf.exempt
def admin_login():
    """Admin login handler."""
    try:
        user = request.form.get("user")
        pw = request.form.get("pw")
        admin_user = wbankwallet.query.filter_by(username=user).first()
        if admin_user and admin_user.role == "admin" and admin_user.password == pw:
            session["admin_user"] = user
            session.permanent = True
            try: write_audit_log("ADMIN_LOGIN", user, "Admin login success", request)
            except: pass
            return redirect("/admin/dashboard")
        try: write_audit_log("ADMIN_LOGIN_FAIL", user, "Admin login failed", request)
        except: pass
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/logout")
def admin_logout():
    admin_user = session.pop("admin_user", None)
    if admin_user:
        try: write_audit_log("ADMIN_LOGOUT", admin_user, "Admin logout", request)
        except: pass
    session.clear()
    return redirect("/admin")

@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin_user" not in session:
        return redirect("/admin")
    write_audit_log("ADMIN_VIEW_DASHBOARD", session["admin_user"], "Viewed admin dashboard", request)
    return render_template("admin/index.html", admin_user=session["admin_user"])

@app.route("/admin/api/stats")
@csrf.exempt
def admin_api_stats():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        total_users = wbankwallet.query.count()
        try: pending_kyc = wbankkyc.query.count()
        except: pending_kyc = 0
        try: total_records = wbankrecord.query.count()
        except: total_records = 0
        try: audit_count = audit_log.query.count()
        except: audit_count = 0
        return jsonify({
            "total_users": total_users,
            "pending_kyc": pending_kyc,
            "total_records": total_records,
            "audit_count": audit_count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/users")
@csrf.exempt
def admin_api_users():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        users_list = wbankwallet.query.order_by(wbankwallet.username).all()
        return jsonify([{
            "username": u.username, "balance": u.balance,
            "verify": u.verify, "role": u.role,
            "accnumber": u.accnumber, "email": u.email, "sub": u.sub
        } for u in users_list])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/verify_user", methods=["POST"])
@csrf.exempt
def admin_api_verify_user():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        uname = request.json.get("username")
        user = wbankwallet.query.filter_by(username=uname).first()
        if user:
            user.verify = "yes"
            user.role = "user"
            db.session.commit()
            write_audit_log("ADMIN_VERIFY_USER", session["admin_user"], f"Verified: {uname}", request)
            return jsonify({"success": True})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/freeze_user", methods=["POST"])
@csrf.exempt
def admin_api_freeze_user():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        uname = request.json.get("username")
        user = wbankwallet.query.filter_by(username=uname).first()
        if user:
            if user.sub and "Freeze" in str(user.sub):
                user.sub = None
                action = "Unfrozen"
            else:
                user.sub = "Freeze: by admin"
                action = "Frozen"
            db.session.commit()
            write_audit_log(f"ADMIN_{action.upper()}", session["admin_user"], f"{action}: {uname}", request)
            return jsonify({"success": True, "action": action})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/update_balance", methods=["POST"])
@csrf.exempt
def admin_api_update_balance():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        uname = request.json.get("username")
        amount = request.json.get("amount", 0, type=int)
        user = wbankwallet.query.filter_by(username=uname).first()
        if user:
            old = user.balance
            user.balance = str(int(user.balance) + amount)
            db.session.commit()
            write_audit_log("ADMIN_UPDATE_BALANCE", session["admin_user"],
                          f"User: {uname}, Old: {old}, New: {user.balance}, Change: {amount}", request)
            return jsonify({"success": True, "new_balance": user.balance})
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/audit_log")
@csrf.exempt
def admin_api_audit_log():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        entries = audit_log.query.order_by(audit_log.timestamp.desc()).limit(100).all()
        return jsonify([{
            "id": e.id, "username": e.username, "action": e.action,
            "detail": e.detail, "ip_address": e.ip_address,
            "timestamp": e.timestamp.strftime("%Y/%m/%d %H:%M:%S") if e.timestamp else ""
        } for e in entries])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

'''
        m = m[:catch_all_idx] + admin_routes + m[catch_all_idx:]
        print('[OK] Admin routes added before catch-all')
    else:
        print('[WARN] Could not find catch-all route')
        # Try inserting before start_web
        idx = m.find('def start_web():')
        if idx > 0:
            m = m[:idx] + admin_routes + m[idx:]
            print('[OK] Admin routes added before start_web')

open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('[OK] Syntax OK')
except py_compile.PyCompileError as e:
    print(f'[FAIL] {e}')

print('\nRestart server')
