"""Find JS syntax errors in wbankClient.html"""
import sys, re
sys.stdout.reconfigure(encoding="utf-8")

c = open("E:/wbank/templates/wbankClient.html", "r", encoding="utf-8").read()
lines = c.split("\n")

# Find all script blocks
script_starts = [i for i, l in enumerate(lines) if "<script" in l]
script_end = [i for i, l in enumerate(lines) if "</script>" in l]

print(f"File: {len(lines)} lines, {len(c)} bytes")
print(f"Script blocks: {len(script_starts)}")

# Check for common JS syntax errors
for i, line in enumerate(lines):
    stripped = line.strip()
    # Check for bare + VAR + , pattern (like the old bug)
    if re.search(r'address:\s*\+\s*\w+\s*,', stripped):
        print(f"  BROKEN address pattern at line {i+1}: {stripped[:80]}")
    # Check for trailing comma in object
    if re.search(r'^\s*address:\s*[^,]*,\s*$', stripped) and '0x' not in stripped and 'http' not in stripped:
        if not stripped.strip().endswith("'") and not stripped.strip().endswith('"'):
            print(f"  SUSPICIOUS address at line {i+1}: {stripped[:80]}")

# Show line ~297 area
print(f"\n--- Lines 295-305 ---")
for i in range(max(0, 294), min(len(lines), 305)):
    print(f"{i+1}: {lines[i]}")

# Check showPage definition
show_defs = [(i, l) for i, l in enumerate(lines) if "function showPage" in l]
print(f"\nshowPage definitions: {len(show_defs)}")
for i, l in show_defs:
    print(f"  Line {i+1}: {l[:80]}")
