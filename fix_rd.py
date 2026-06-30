with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix admin redirects - staff also goes to dashboard
content = content.replace('redirect("/admin/wbankkyc")', 'redirect("/admin/dashboard")')
content = content.replace("redirect('/admin/wbankkyc')", "redirect('/admin/dashboard')")
content = content.replace('redirect("/admin/wbankwallet")', 'redirect("/admin/dashboard")')
content = content.replace("redirect('/admin/wbankwallet')", "redirect('/admin/dashboard')")

# Remove Flask-Admin config
content = content.replace("app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'\n", "")

# Remove commented Flask-Admin code
start = content.find('# 創建 Flask-Admin 管理界面')
end = content.find('\n\n# 添加 SQLAlchemy 模型管理視圖')
if start > 0 and end > start:
    content = content[:start] + content[end:]

content = content.replace('\n\n\n# 添加 SQLAlchemy 模型管理視圖\n\n', '\n')

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Fixed')
print('FLASK_ADMIN_SWATCH:', 'FLASK_ADMIN_SWATCH' in content)
print('/admin/wbankkyc:', '/admin/wbankkyc' in content)
print('/admin/wbankwallet:', '/admin/wbankwallet' in content)
