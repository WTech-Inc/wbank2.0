"""Move admin_swap_page route BEFORE catch-all route"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/main.py", "r", encoding="utf-8").read()

# Find the catch-all route
catch_all = '@app.route("/<path:template_name>")'

# Find the swap route definition
swap_start = c.find('@app.route("/admin/swap")')
swap_end = c.find('@app.route("/wbank/auth/v1/logout")')

if swap_start < 0 or swap_end < 0:
    print("Could not find swap route!")
    sys.exit(1)

# Extract the swap function
swap_func = c[swap_start:swap_end]

# Remove it from current position
c = c[:swap_start] + c[swap_end:]

# Insert it BEFORE the catch-all route
catch_all_pos = c.find(catch_all)
if catch_all_pos < 0:
    print("Could not find catch-all route!")
    sys.exit(1)

c = c[:catch_all_pos] + swap_func + "\n" + c[catch_all_pos:]

# Also restore render_template call
c = c.replace('return "SWAP PAGE TEST"', 'return render_template("admin/swap.html")')

open("E:/wbank/main.py", "w", encoding="utf-8").write(c)
print(f"OK - swap route moved before catch-all")
