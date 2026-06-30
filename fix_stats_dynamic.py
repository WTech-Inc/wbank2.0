"""Fix main page stats to be dynamic (from API) instead of hardcoded"""
import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Add stats API endpoint to main.py
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

stats_api = '''

@app.route("/api/main/stats")
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
        return jsonify({"error": str(e)}), 500
'''

# Inject before start_web
insert_at = m.find("def start_web():")
if insert_at < 0:
    insert_at = len(m)
m = m[:insert_at] + stats_api + "\n" + m[insert_at:]

open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('[OK] main.py syntax OK + stats API added')
except py_compile.PyCompileError as e:
    print(f'[FAIL] {e}')

# 2. Update wbank.html template to use API data
tpl = open('E:\\wbank\\templates\\wbank.html', 'r', encoding='utf-8').read()

# Replace the hardcoded counter section with dynamic fetch
old_stats_section = '''        <!-- Stats -->
        <div class="stats-row">'''
new_stats_section = '''        <!-- Stats (dynamic from API) -->
        <div class="stats-row" id="stats-row">'''

tpl = tpl.replace(old_stats_section, new_stats_section)

# Replace each counter to use API data
replacements = [
    ('data-target="1580"', 'data-target="0" id="stat-users"'),
    ('data-target="12500"', 'data-target="0" id="stat-tx"'),
    ('data-target="8900000"', 'data-target="0" id="stat-volume"'),
    ('data-target="99"', 'data-target="99" id="stat-uptime"'),
]
for old_val, new_val in replacements:
    tpl = tpl.replace(old_val, new_val)

# Add fetch script before closing </body>
fetch_script = '''
    <script>
        // Fetch real-time stats
        fetch('/api/main/stats')
            .then(r => r.json())
            .then(d => {
                if (d.users !== undefined) {
                    const u = document.getElementById('stat-users');
                    if (u) u.textContent = d.users.toLocaleString();
                }
                if (d.transactions !== undefined) {
                    const t = document.getElementById('stat-tx');
                    if (t) t.textContent = d.transactions.toLocaleString();
                }
                if (d.volume !== undefined) {
                    const v = document.getElementById('stat-volume');
                    if (v) v.textContent = Math.round(d.volume).toLocaleString();
                }
                if (d.uptime !== undefined) {
                    const up = document.getElementById('stat-uptime');
                    if (up) up.textContent = d.uptime;
                }
            })
            .catch(() => {});
    </script>
'''

if '</body>' in tpl:
    tpl = tpl.replace('</body>', fetch_script + '\n</body>')
    print('[OK] Dynamic stats script added to wbank.html')

open('E:\\wbank\\templates\\wbank.html', 'w', encoding='utf-8').write(tpl)
print('[OK] wbank.html updated with dynamic stats')

print('\n=== Done ===')
