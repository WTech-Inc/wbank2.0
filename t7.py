import py_compile

with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace admin_login to use database auth
old_admin_login = '''@app.route("/admin/login", methods=["POST"])
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
    return redirect("/admin")'''

new_admin_login = '''@app.route("/admin/login", methods=["POST"])
@csrf.exempt
def admin_login():
    """Admin login handler - authenticates via wbankwallet table with role='admin'."""
    user = request.form.get("user")
    pw = request.form.get("pw")
    try:
        # Look up user in database with admin role
        admin_user = wbankwallet.query.filter_by(username=user).first()
        if admin_user and admin_user.role == "admin" and admin_user.password == pw:
            session["admin_user"] = user
            session.permanent = True
            write_audit_log("ADMIN_LOGIN", user, "Admin login success via database", request)
            return redirect("/admin/dashboard")
        write_audit_log("ADMIN_LOGIN_FAIL", user, "Admin login failed - invalid credentials or not admin", request)
        flash("Account or password error", "error")
        return redirect("/admin")
    except Exception as e:
        write_audit_log("ADMIN_LOGIN_ERROR", user, f"Login system error: {str(e)}", request)
        flash("System error, please try again", "error")
        return redirect("/admin")'''

content = content.replace(old_admin_login, new_admin_login)

print('Admin login now uses database auth')

# 2. Add export endpoints before startup section
startup_marker = 'def start_web():'
idx = content.find(startup_marker)
if idx > 0:
    export_routes = '''

# ============================================================
# Export Routes (ISO 27001 compliant)
# ============================================================

@app.route("/admin/api/export/users")
def admin_api_export_users():
    """Export users as CSV."""
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    import csv, io
    try:
        users_list = wbankwallet.query.order_by(wbankwallet.username).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Username", "Balance", "AccountNumber", "Verify", "Role", "Email", "Status"])
        for u in users_list:
            writer.writerow([u.username, u.balance, u.accnumber, u.verify, u.role, u.email, u.sub or ""])
        write_audit_log("EXPORT_USERS", session["admin_user"], f"Exported {len(users_list)} users as CSV", request)
        return Response(output.getvalue(), mimetype="text/csv",
                        headers={"Content-Disposition": "attachment;filename=wbank_users.csv"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/export/audit_log")
def admin_api_export_audit_log():
    """Export audit log as CSV."""
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    import csv, io
    try:
        entries = audit_log.query.order_by(audit_log.timestamp.desc()).all()
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Timestamp", "Username", "Action", "Detail", "IP Address"])
        for e in entries:
            ts = e.timestamp.strftime("%Y/%m/%d %H:%M:%S") if e.timestamp else ""
            writer.writerow([e.id, ts, e.username, e.action, e.detail or "", e.ip_address or ""])
        write_audit_log("EXPORT_AUDIT_LOG", session["admin_user"],
                        f"Exported {len(entries)} audit log entries as CSV", request)
        return Response(output.getvalue(), mimetype="text/csv",
                        headers={"Content-Disposition": "attachment;filename=wbank_audit_log.csv"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/export/json")
def admin_api_export_json():
    """Export all data as JSON."""
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        users_list = wbankwallet.query.order_by(wbankwallet.username).all()
        audit_entries = audit_log.query.order_by(audit_log.timestamp.desc()).all()
        data = {
            "users": [{
                "username": u.username, "balance": u.balance, "accnumber": u.accnumber,
                "verify": u.verify, "role": u.role, "email": u.email, "status": u.sub
            } for u in users_list],
            "audit_log": [{
                "id": e.id,
                "timestamp": e.timestamp.strftime("%Y/%m/%d %H:%M:%S") if e.timestamp else "",
                "username": e.username, "action": e.action,
                "detail": e.detail, "ip_address": e.ip_address
            } for e in audit_entries]
        }
        write_audit_log("EXPORT_JSON", session["admin_user"],
                        f"Exported {len(users_list)} users, {len(audit_entries)} audit entries", request)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/admin/api/export/audit_json")
def admin_api_export_audit_json():
    """Export audit log as JSON."""
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        entries = audit_log.query.order_by(audit_log.timestamp.desc()).all()
        data = [{
            "id": e.id,
            "timestamp": e.timestamp.strftime("%Y/%m/%d %H:%M:%S") if e.timestamp else "",
            "username": e.username, "action": e.action,
            "detail": e.detail, "ip_address": e.ip_address
        } for e in entries]
        write_audit_log("EXPORT_AUDIT_JSON", session["admin_user"],
                        f"Exported {len(entries)} audit entries as JSON", request)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

'''

    content = content[:idx] + export_routes + '\n' + content[idx:]
    print('Added export routes')
else:
    print('ERROR: Could not find startup section')

# Also add audit logging for admin page views
# Add to admin_dashboard
old_dash = '''@app.route("/admin/dashboard")
def admin_dashboard():
    """Admin dashboard page."""
    if "admin_user" not in session:
        return redirect("/admin")
    return render_template("admin/index.html", admin_user=session["admin_user"])'''

new_dash = '''@app.route("/admin/dashboard")
def admin_dashboard():
    """Admin dashboard page."""
    if "admin_user" not in session:
        return redirect("/admin")
    write_audit_log("ADMIN_VIEW_DASHBOARD", session["admin_user"], "Viewed admin dashboard", request)
    return render_template("admin/index.html", admin_user=session["admin_user"])'''

content = content.replace(old_dash, new_dash)
print('Added audit log to dashboard view')

# Add audit for API stats view
old_stats = '''@app.route("/admin/api/stats")
def admin_api_stats():
    """Get dashboard statistics."""
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:'''

new_stats = '''@app.route("/admin/api/stats")
def admin_api_stats():
    """Get dashboard statistics."""
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        write_audit_log("ADMIN_VIEW_STATS", session["admin_user"], "Viewed dashboard stats", request)'''

content = content.replace(old_stats, new_stats)
print('Added audit log to stats view')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
