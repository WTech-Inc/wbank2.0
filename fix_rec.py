import py_compile

with open('E:\\wbank\\wbank_web3.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix: use ON CONFLICT to handle duplicate username
content = content.replace(
    '        sql_text("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t)")',
    '        sql_text("INSERT INTO wbankrecord (username, action, time) VALUES (:u, :a, :t) ON CONFLICT (username) DO UPDATE SET action = :a, time = :t")'
)

with open('E:\\wbank\\wbank_web3.py', 'w', encoding='utf-8') as f:
    f.write(content)

try:
    py_compile.compile('E:\\wbank\\wbank_web3.py', doraise=True)
    print('Syntax OK!')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
