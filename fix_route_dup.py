"""Remove duplicate register_page route"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

main = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()

# Check for the problematic "Route disabled" handler
if 'Route disabled' in main and 'register_page' in main:
    print('[INFO] Found Route disabled + register_page - removing duplicate')

    # Find the old disabled route for /auth/reg
    # Pattern: @app.route("/auth/reg"... with return jsonify({"error":"Route disabled"...})
    disabled_pattern = r"""@app\.route\(["']/auth/reg["'].*?\).*?def [a-z_]+\(.*?\):.*?return jsonify\(\{.*?error["']\s*:\s*["']Route disabled.*?\}.*?\).*?(?=\n\s*@app\.route|\ndef )"""

    old_count = main.count('def register_page')
    print(f'  register_page count: {old_count}')

    if old_count > 1:
        # Find the FIRST occurrence and remove it (it's the old disabled one)
        first_pos = main.find('def register_page(')
        if first_pos > 0:
            # Find the @app.route before it
            route_pos = main.rfind('@app.route', 0, first_pos)
            if route_pos >= 0:
                # Find the next route/function after this one
                next_route = main.find('@app.route', first_pos + 20)
                if next_route < 0:
                    next_route = main.find('def ', first_pos + 20)
                if next_route > 0:
                    # Remove everything from route_pos to before next_route
                    main = main[:route_pos] + main[next_route:]
                    print(f'  [OK] Removed duplicate register_page route')

    open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(main)
elif 'register_page' in main:
    print('[OK] Route exists without conflict')
else:
    print('[INFO] No register_page found')

# Also add a unique endpoint name to ensure no conflict
if 'register_page' not in main:
    print('[ERROR] register_page missing entirely!')
