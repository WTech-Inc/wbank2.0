import re, py_compile

with open('E:\\wbank\\main.py', 'rb') as f:
    data = f.read()

text = data.decode('utf-8')

# 1. Remove trade_wcoins socket handler
text = re.sub(
    r"@socketio\.on\(\"trade\"\)\s*\n\s*def trade_wcoins\(data\):.*?(?=\n\s*@socketio\.on)",
    "",
    text,
    flags=re.DOTALL
)

# 2. Remove fried_wcoins_bot
text = re.sub(
    r"@socketio\.on\(\"friedBot\"\)\s*\n\s*def fried_wcoins_bot\(data\):.*?(?=\n\s*@socketio\.on)",
    "",
    text,
    flags=re.DOTALL
)

# 3. Remove trade_wcoins_bot
text = re.sub(
    r"@socketio\.on\(\"tradeBot\"\)\s*\n\s*def trade_wcoins_bot\(data\):.*?(?=\n\s*@socketio\.on|\n\s*@app\.route)",
    "",
    text,
    flags=re.DOTALL
)

# 4. Remove /wcoins/data route
text = re.sub(
    r"@app\.route\('/wcoins/data'\)\s*\n\s*def data\(\):.*?(?=\n\s*@app\.route|\n\s*def )",
    "",
    text,
    flags=re.DOTALL
)

# 5. Fix admin redirect
text = text.replace('redirect("/admin/wbankkyc")', 'redirect("/admin/dashboard")')
text = text.replace('redirect("/admin/wbankwallet")', 'redirect("/admin/dashboard")')

# 6. Flush out FLASK_ADMIN config
text = text.replace("app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'\n", "")

# 7. Remove Flask-Admin comment block
text = text.replace('\n# 創建 Flask-Admin 管理界面\n\n\n# 添加 SQLAlchemy 模型管理視圖\n\n', '\n')

# 8. Add restrict_routes for /admin
text = text.replace(
    "if path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/socket.io/'):",
    "if path == '/admin' or path.startswith('/admin/') or path.startswith('/static/') or path.startswith('/socket.io/'):"
)

# 9. Remove wangtry from users dict
text = text.replace('    "wangtry": generate_password_hash("Chan1234#"),\n', '')

# Write intermediate result
with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(text)

# Verify syntax
py_compile.compile('E:\\wbank\\main.py', doraise=True)
print('Phase 1 complete - investment removal and config cleanup')
