import sys, re
sys.stdout.reconfigure(encoding='utf-8')

m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
lines = m.split('\n')

# 1. Find all blocks starting with @app.route containing /auth/reg or /wbank/kyc/status
# 2. For each, check if it's part of the new do_everything.py block (look for "do_everything" marker)
# 3. Remove old duplicates, keep new ones

# Strategy: Find ALL regions between @app.route lines and track which ones are new/old
routes_to_check = ['/auth/reg', '/wbank/kyc/status']

for route_path in routes_to_check:
    # Find all @app.route blocks for this path
    positions = []
    for i, line in enumerate(lines):
        if f'@app.route("{route_path}"' in line or f"@app.route('{route_path}'" in line:
            # Find the end of this block (next @app.route or def at module level)
            func_name = ''
            end = i + 1
            while end < len(lines):
                if lines[end].strip().startswith('@app.route') and end > i:
                    break
                if lines[end].strip().startswith('def ') and end > i:
                    func_name = lines[end].strip()
                if end > i and lines[end].strip().startswith('') and end > i + 30:
                    # Check if we've reached a blank line after the function
                    pass
                end += 1
            positions.append((i, end, func_name, route_path))

    print(f'\nRoute {route_path}: {len(positions)} occurrences')
    for start, end, func, path in positions:
        # Check if this block has "do_everything" marker (new) or not (old)
        block_text = '\n'.join(lines[start:end])
        is_new = 'do_everything' in block_text or 'Registration + KYC' in block_text or '=== Registration' in block_text
        marker = '✅ NEW' if is_new else '❌ OLD'
        print(f'  {marker}: lines {start+1}-{end} | {func}')

        # If old, mark for removal
        if not is_new:
            for j in range(start, end):
                lines[j] = None  # Mark for deletion

# Remove marked lines
new_lines = [l for l in lines if l is not None]
m = '\n'.join(new_lines)

# Check for remaining duplicates
print(f'\nFinal checks:')
print(f'  register_page count: {m.count("def register_page(")}')
print(f'  kyc_status count: {m.count("def kyc_status(")}')

# Write back
open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)

# Verify syntax
import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('  ✅ Syntax OK')
except py_compile.PyCompileError as e:
    print(f'  ❌ {e}')

print('\n=== Done ===')
