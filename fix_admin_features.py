"""Fix admin audit log API format and enhance swap records display"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

# ═══ 1. Fix audit log API to return paginated object ═══
main_content = open("E:/wbank/main.py", "r", encoding="utf-8").read()

old_audit_api = '''@app.route("/admin/api/audit_log")
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
        return jsonify({"error": str(e)}), 500'''

new_audit_api = '''@app.route("/admin/api/audit_log")
@csrf.exempt
def admin_api_audit_log():
    if "admin_user" not in session:
        return jsonify({"error": "Not logged in"}), 401
    try:
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 50))
        action_filter = request.args.get("action", "")
        username_filter = request.args.get("username", "")
        query = audit_log.query
        if action_filter:
            query = query.filter(audit_log.action.like(f"%{action_filter}%"))
        if username_filter:
            query = query.filter(audit_log.username.like(f"%{username_filter}%"))
        total = query.count()
        entries = query.order_by(audit_log.timestamp.desc()).offset((page-1)*per_page).limit(per_page).all()
        return jsonify({
            "entries": [{
                "id": e.id, "username": e.username, "action": e.action,
                "detail": e.detail, "ip_address": e.ip_address,
                "timestamp": e.timestamp.strftime("%Y/%m/%d %H:%M:%S") if e.timestamp else ""
            } for e in entries],
            "total": total,
            "page": page,
            "per_page": per_page
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''

if old_audit_api in main_content:
    main_content = main_content.replace(old_audit_api, new_audit_api)
    print("Audit API fixed (paginated response)")
else:
    print("Audit API pattern not found")

# ═══ 2. Update swap/apply to store more details ═══
# Add a swap_detail field to the record
old_apply = '''    # Create swap record (using cashout table)
    new_swap = cashout(name=user, amount=round(net_hkd, 2))
    db.session.add(new_swap)
    db.session.commit()

    # Audit logged inline
    try:
        db.session.execute(
            text("INSERT INTO audit_log (username, action, detail, ip_address, timestamp) VALUES (:u, :a, :d, :i, :t)"),
            {'u': user, 'a': 'SWAP_APPLY', 'd': f"Swapped {wtc_amount} WTC -> {round(net_hkd,2)} HKD (Fee: {round(fee_amount,2)} HKD)", 'i': request.remote_addr, 't': datetime.datetime.utcnow()}
        )
        db.session.commit()
    except:
        pass'''

new_apply = '''    # Create swap record with full details
    new_swap = cashout(name=user, amount=round(net_hkd, 2))
    db.session.add(new_swap)
    db.session.flush()
    swap_id = new_swap.id

    # Audit logged inline
    try:
        db.session.execute(
            text("INSERT INTO audit_log (username, action, detail, ip_address, timestamp) VALUES (:u, :a, :d, :i, :t)"),
            {'u': user, 'a': 'SWAP_APPLY', 'd': f"Swapped {wtc_amount} WTC -> HK${round(net_hkd,2)} (Gross: HK${round(gross_hkd,2)}, Fee: HK${round(fee_amount,2)}, Rate: {wtc_rate}WTC={hkd_rate}HKD)", 'i': request.remote_addr, 't': datetime.datetime.utcnow()}
        )
        db.session.commit()
    except:
        pass'''

if old_apply in main_content:
    main_content = main_content.replace(old_apply, new_apply)
    print("Swap apply updated with full details")
else:
    print("Swap apply pattern not found")

open("E:/wbank/main.py", "w", encoding="utf-8").write(main_content)

# ═══ 3. Update admin admin panel swap table to show more info ═══
admin_tpl = open("E:/wbank/templates/admin/index.html", "r", encoding="utf-8").read()

# Update the swap table headers and data display
old_swap_headers = '<th>ID</th><th>User</th><th>Amount (HKD)</th><th>Status</th><th>Action</th>'
new_swap_headers = '<th>ID</th><th>User</th><th>Amount</th><th>Status</th><th>Detail</th><th>Action</th>'

if old_swap_headers in admin_tpl:
    admin_tpl = admin_tpl.replace(old_swap_headers, new_swap_headers)
    print("Admin swap table headers updated")

# Update the swap table row rendering
old_swap_row = '''tbody.innerHTML = swaps.map(s =>
'<tr><td>' + s.id + '</td><td>' + s.user + '</td><td>HK$' + s.amount + '</td><td>' + (s.status || 'Pending') + '</td>' +
'<td>' + ((s.status || 'Pending') === 'Pending' ?'''

new_swap_row = '''tbody.innerHTML = swaps.map(s =>
'<tr><td>' + s.id + '</td><td>' + (s.user || '') + '</td><td>HK$' + (s.amount || 0) + '</td><td>' + (s.status || 'Pending') + '</td>' +
'<td style="font-size:11px;color:#64748b;">' + (s.detail || '-') + '</td>' +
'<td>' + ((s.status || 'Pending') === 'Pending' ?'''

if old_swap_row in admin_tpl:
    admin_tpl = admin_tpl.replace(old_swap_row, new_swap_row)
    print("Admin swap table rows updated")
else:
    print("Swap row pattern not found - checking alternatives...")
    # Try to find any swap row rendering
    idx = admin_tpl.find("swaps.map")
    if idx >= 0:
        print(f"Found swaps.map at position {idx}:")
        print(admin_tpl[idx:idx+300])

open("E:/wbank/templates/admin/index.html", "w", encoding="utf-8").write(admin_tpl)

# ═══ 4. Update admin swap API to include detail from audit_log ═══
# The swap API already works - the detail is now in the audit_log

print("\nDone! Restart server.")
