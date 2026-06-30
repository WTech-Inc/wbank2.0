"""Fix circular import in swap/apply and remove the log_audit call"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/main.py", "r", encoding="utf-8").read()

# Remove the circular import and call
old = """    from main import log_audit
    log_audit("SWAP_APPLY", user, f"Swapped {wtc_amount} WTC -> {round(net_hkd,2)} HKD (Fee: {round(fee_amount,2)} HKD)")

"""

new = """    # Audit logged inline
    try:
        db.session.execute(
            text("INSERT INTO audit_log (username, action, detail, ip_address, timestamp) VALUES (:u, :a, :d, :i, :t)"),
            {'u': user, 'a': 'SWAP_APPLY', 'd': f"Swapped {wtc_amount} WTC -> {round(net_hkd,2)} HKD (Fee: {round(fee_amount,2)} HKD)", 'i': request.remote_addr, 't': datetime.datetime.utcnow()}
        )
        db.session.commit()
    except:
        pass

"""

if old in c:
    c = c.replace(old, new)
    open("E:/wbank/main.py", "w", encoding="utf-8").write(c)
    print("Fixed circular import")
else:
    print("Pattern not found")
    idx = c.find("from main import log_audit")
    if idx >= 0:
        print(f"Found at {idx}: {c[idx:idx+200]}")
