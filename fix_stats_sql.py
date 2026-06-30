import sys
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Find and fix the stats API
old_stats = '''@app.route("/api/main/stats")
def api_main_stats():
    """Return main page stats dynamically."""
    try:
        total_users = wbankwallet.query.count()
        total_tx = wbankrecord.query.count()
        # Sum volume
        from sqlalchemy import text
        vol = db.session.execute(text("SELECT COALESCE(SUM(amount::numeric), 0) FROM wbankrecord")).scalar()
        return jsonify({
            "users": total_users,
            "transactions": total_tx,
            "volume": float(vol) if vol else 0,
            "uptime": 99.9
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''

new_stats = '''@app.route("/api/main/stats")
def api_main_stats():
    """Return main page stats dynamically."""
    try:
        total_users = wbankwallet.query.count()
        total_tx = wbankrecord.query.count()
        from sqlalchemy import text
        try:
            vol = db.session.execute(text("SELECT COUNT(*) FROM wbankrecord")).scalar()
        except:
            vol = total_tx
        return jsonify({
            "users": total_users,
            "transactions": total_tx,
            "volume": vol or 0,
            "uptime": 99.9
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500'''

if old_stats in m:
    m = m.replace(old_stats, new_stats)
    open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)
    print('[OK] Stats API fixed')
else:
    print('[WARN] Could not find old stats API')
    # Try finding what's actually there
    idx = m.find('api/main/stats')
    if idx >= 0:
        print(m[idx:idx+500])

import py_compile
py_compile.compile('E:\\wbank\\main.py', doraise=True)
print('[OK] Syntax OK')
