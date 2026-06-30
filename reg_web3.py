with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Register web3 blueprint
old = "from wcloud import wcloud_bp # 導入 Blueprint"
new = old + "\nfrom wbank_web3 import web3_bp"
content = content.replace(old, new)

old2 = "app.register_blueprint(wcloud_bp, url_prefix='/wcloud')"
new2 = old2 + "\napp.register_blueprint(web3_bp)"
content = content.replace(old2, new2)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('Blueprint registered')

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
