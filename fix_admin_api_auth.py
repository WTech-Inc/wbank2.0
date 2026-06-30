"""Fix admin API auth - accept both session and query param token"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/main.py"
c = open(path, "r", encoding="utf-8").read()

# Add a simple token check to all admin API routes
# Replace: if "admin_user" not in session: return jsonify(...), 401
# With: check both session AND url param

old_check = '    if "admin_user" not in session:\n        return jsonify({"error": "Not logged in"}), 401'

# Count how many times this pattern appears
count = c.count(old_check)
print(f"Found {count} admin auth checks")

new_check = '''    if "admin_user" not in session:
        # Also allow if 'token' query param matches
        if request.args.get("token") != hashlib.sha256("WTechAdmin2026".encode()).hexdigest():
            return jsonify({"error": "Not logged in"}), 401'''

c = c.replace(old_check, new_check)

# Also update dashboard to pass token to template
old_dash = 'return render_template("admin/index.html", admin_user=session["admin_user"])'
new_dash = 'return render_template("admin/index.html", admin_user=session["admin_user"], admin_token=hashlib.sha256("WTechAdmin2026".encode()).hexdigest())'
if old_dash in c:
    c = c.replace(old_dash, new_dash)
    print("Dashboard token added")

open(path, "w", encoding="utf-8").write(c)
print("Done")
