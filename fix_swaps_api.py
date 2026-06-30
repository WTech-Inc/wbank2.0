"""Update swap admin API to include audit detail"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/main.py"
c = open(path, "r", encoding="utf-8").read()

old = """def admin_api_swaps():
    \"\"\"Admin: Get all swap requests\"\"\"
    swaps = cashout.query.order_by(cashout.id.desc()).all()
    return jsonify([{
        "id": s.id,
        "user": s.name,
        "amount": s.amount,
        "status": s.status,
    } for s in swaps])"""

new = """def admin_api_swaps():
    \"\"\"Admin: Get all swap requests with details\"\"\"
    swaps = cashout.query.order_by(cashout.id.desc()).all()
    result = []
    for s in swaps:
        audit = audit_log.query.filter_by(username=s.name, action='SWAP_APPLY').order_by(audit_log.timestamp.desc()).first()
        result.append({
            "id": s.id,
            "user": s.name,
            "amount": s.amount,
            "status": s.status,
            "detail": audit.detail if audit else ''
        })
    return jsonify(result)"""

if old in c:
    c = c.replace(old, new)
    open(path, "w", encoding="utf-8").write(c)
    print("OK - swaps API updated with detail")
else:
    print("NOT FOUND")
