"""Check JS syntax in second script block"""
import sys, re
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/templates/wbankClient.html", "r", encoding="utf-8").read()

# Extract second script block (between line 300's <script> and 523's </script>)
lines = c.split("\n")
script_lines = []
in_block = False
for i, line in enumerate(lines):
    if i >= 299 and i < 523:  # lines 300-522
        if i == 300:
            continue  # skip <script> tag
        if i == 522:
            continue  # skip </script> tag
        script_lines.append(line)

script = "\n".join(script_lines)

# Check for common JS syntax issues
# 1. Unmatched braces
opens = script.count("{")
closes = script.count("}")
if opens != closes:
    print(f"UNMATCHED BRACES: {opens} open, {closes} close")

# 2. Unmatched parentheses
parens_open = script.count("(")
parens_close = script.count(")")
if parens_open != parens_close:
    print(f"UNMATCHED PARENS: {parens_open} open, {parens_close} close")

# 3. Check for missing semicolons before '}'
# (not a syntax error in JS, but can indicate issues)

# 4. Print the problematic line 511
print(f"\nLine 511: {lines[510].rstrip()[:150]}")

# 5. Try to write to a temp file and check with Node.js if available
import os
temp_file = "E:/wbank/_temp_check.js"
with open(temp_file, "w", encoding="utf-8") as f:
    f.write("'use strict';\n" + script)
try:
    result = os.system(f'node --check {temp_file} 2>&1')
    if result == 0:
        print("JS SYNTAX: OK")
    else:
        print(f"JS SYNTAX: FAILED (exit {result})")
except:
    print("JS CHECK: Node not available")
finally:
    if os.path.exists(temp_file):
        os.remove(temp_file)

# Show condensed version of the script (function names only)
funcs = re.findall(r'(async\s+)?function\s+(\w+)', script)
print(f"\nFunctions defined: {[f[1] for f in funcs]}")
