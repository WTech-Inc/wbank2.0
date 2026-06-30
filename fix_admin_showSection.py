"""Fix admin template - remove duplicate showSection and add swap support to original"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# Remove my duplicate showSection (the one that takes 1 param)
old_dup = '''function showSection(name) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById('section-' + name).classList.add('active');
    document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
    const link = document.querySelector(`.sidebar a[onclick*="'${name}'"]`);
    if (link) link.classList.add('active');
    if (name === 'swap') loadSwapData();
}'''

if old_dup in c:
    c = c.replace(old_dup, "")
    print("Removed duplicate showSection")
else:
    print("Duplicate showSection not found - checking...")

# Add swap support to ORIGINAL showSection
old_orig = '''    if (id === 'audit') { auditPage = 1; loadAuditLog(); }
}'''

new_orig = '''    if (id === 'audit') { auditPage = 1; loadAuditLog(); }
    if (id === 'swap') loadSwapData();
}'''

if old_orig in c:
    c = c.replace(old_orig, new_orig)
    print("Added swap support to original showSection")
else:
    print("Original showSection end not found")

open(path, "w", encoding="utf-8").write(c)
print(f"Saved ({len(c)} bytes)")
