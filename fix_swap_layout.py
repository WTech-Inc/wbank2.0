"""Fix swap section alignment and add burger menu to admin template"""
import sys
sys.stdout.reconfigure(encoding="utf-8")

path = "E:/wbank/templates/admin/index.html"
c = open(path, "r", encoding="utf-8").read()

# 1. Fix swap section: make sure section-swap div has same structure as others
# The other sections use the class "section" and are inside the content div
# The swap section might be using incorrect indentation or structure

# Check if swap section div uses different indentation
old_swap_div = '<div id="section-swap" class="section">'
new_swap_div = '            <div id="section-swap" class="section">'
c = c.replace(old_swap_div, new_swap_div)

# 2. Add burger menu button to topbar
burger = '<button class="btn btn-dark d-md-none" onclick="toggleSidebar()">☰</button>'
if burger not in c:
    c = c.replace('class="topbar">', 'class="topbar">' + burger)

# 3. Add toggleSidebar JS and responsive CSS
toggle_js = '''
        function toggleSidebar() {
            var sb = document.querySelector('.sidebar');
            if (sb) sb.style.display = sb.style.display === 'none' ? 'block' : 'none';
        }
'''
c = c.replace("</script>", toggle_js + "\n</script>")

# Add mobile CSS
mobile_css = '''
        @media (max-width: 768px) {
            .sidebar { display: none; }
            .content { margin-left: 0 !important; }
            .topbar { left: 0 !important; }
        }
'''
c = c.replace("</style>", mobile_css + "\n</style>")

open(path, "w", encoding="utf-8").write(c)
print(f"Done - {len(c)} bytes")
