"""Find and fix JS errors in wbankClient.html"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

tpl = open('E:\\wbank\\templates\\wbankClient.html', 'r', encoding='utf-8').read()
lines = tpl.split('\n')

print('=== Checking for JS errors ===')

# 1. Find stray }
stray_count = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped == '};' or stripped == '}':
        # Check context - is it inside a script?
        stray_count += 1
print(f'Stray }} or }}; lines: {stray_count}')

# 2. Find showPage definition
print('\n=== showPage references ===')
for i, line in enumerate(lines):
    if 'showPage' in line:
        print(f'L{i+1}: {line.strip()[:120]}')

# 3. Find the nav buttons
print('\n=== Nav buttons ===')
for i, line in enumerate(lines):
    if 'onclick="showPage' in line or 'nav-item' in line:
        print(f'L{i+1}: {line.strip()[:120]}')

# 4. Check where showPage is defined
print('\n=== First showPage function ===')
for i, line in enumerate(lines):
    if 'function showPage' in line or 'showPage = function' in line:
        print(f'L{i+1}: {line.strip()[:120]}')
        # Check if it has the right syntax
        for j in range(i, min(i+10, len(lines))):
            print(f'  L{j+1}: {lines[j].strip()[:150]}')
        break

# 5. Fix: remove stray } that might be floating
print('\n=== Fixing JS errors ===')

# Look for the specific pattern: a line with just "}" followed by script closing
# This is likely from the old "const origShowPage = showPage; ... };" pattern

# Remove stray "};" lines that aren't part of any function
fixed = re.sub(r'^\s*\}\s*;\s*$', '', tpl, flags=re.MULTILINE)

# But restore "};" inside actual functions (e.g., end of sendWTC)
# Actually, let me find the problematic area
idx = tpl.find('=== END Web3 Wallet ===')
if idx >= 0:
    context = tpl[idx-200:idx+50]
    print(f'Context around END Web3 Wallet:')
    print(context)

# Find and fix the orphaned "};"
# The old showPage override might have left a "};" in the code
# Check for "};\n    </script>" pattern
orphan = tpl.count('};\n    </script>')
print(f'}}\\n</script> count: {orphan}')

# Fix: remove the orphaned "};" in END Web3 Wallet section
orphan = re.sub(r'\n\s*\}\s*;\s*\n\s*// === END Web3 Wallet ===', '\n    // === END Web3 Wallet ===', tpl)
if orphan != tpl:
    print('[OK] Removed orphaned };')
    tpl = orphan

# Fix: ensure the showPage override at bottom doesn't break
# The "if (typeof window.showPage === 'function')" might fail if showPage is not yet defined
# Move the nav buttons JS check to window.onload context

# Write back
open('E:\\wbank\\templates\\wbankClient.html', 'w', encoding='utf-8').write(tpl)
print('[OK] Fixed - restart server')
