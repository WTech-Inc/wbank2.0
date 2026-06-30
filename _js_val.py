"""Validate JS syntax by extracting script and running node --check"""
import re, subprocess

f = open('templates/wbankClient.html', 'r', encoding='utf-8')
content = f.read()
f.close()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', content, re.DOTALL)
main_script = scripts[-1]

# Extract just the function definitions and check structure
lines = main_script.split('\n')
print(f'Script lines: {len(lines)}')

# Write to file
with open('_js_check.js', 'w', encoding='utf-8') as f:
    f.write(main_script)

# Try node --check
try:
    r = subprocess.run(['node', '--check', '_js_check.js'], capture_output=True, timeout=10)
    if r.returncode == 0:
        print('NODE SYNC CHECK: PASSED')
    else:
        print(f'NODE ERROR (exit {r.returncode}):')
        print(r.stderr.decode('utf-8', errors='replace')[:2000])
except FileNotFoundError:
    print('Node.js not available on server')
except Exception as e:
    print(f'Error running node: {e}')

# If node not available, at least check basic syntax by looking for common issues
print('\nManual checks:')
# Check all function definitions
for i, l in enumerate(lines):
    s = l.strip()
    if 'function ' in s:
        # Check for function()() pattern
        if ')(' in s and 'function' in s and '.then' not in s and '.catch' not in s:
            print(f'  L{i+1}: Suspicious function pattern: {s[:80]}')
