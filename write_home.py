import sys

path = 'E:\\wbank\\templates\\wbank\\home.html'
content = '<!DOCTYPE html>\n<html lang="zh-Hant">\n<head>\n    <meta charset="UTF-8">\n'
content += '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
content += '    <title>泓財銀行 WBank - 首頁</title>\n'
content += '    <style>\n'
content += '        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f4f8; color: #333; display: flex; justify-content: center; align-items: center; min-height: 100vh; }\n'
content += '        .container { background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); max-width: 600px; width: 100%; }\n'
content += '        h1 { color: #003366; margin-bottom: 10px; }\n'
content += '        p { line-height: 1.8; color: #555; }\n'
content += '        .stats { background: #e8f4fd; padding: 15px; border-radius: 8px; margin: 20px 0; text-align: center; }\n'
content += '        .stats span { font-size: 24px; font-weight: bold; color: #003366; }\n'
content += '        footer { text-align: center; margin-top: 30px; color: #999; font-size: 14px; }\n'
content += '    </style>\n</head>\n<body>\n    <div class="container">\n'
content += '        <h1>泓財銀行 WBank</h1>\n'
content += '        <p>致力於提供完善的金融科技服務。</p>\n'
content += '        <div class="stats">\n'
content += '            <p>目前用戶總數：<span>{{ count }}</span> 人</p>\n'
content += '        </div>\n'
content += '        <p><a href="/wbank">前往登入</a></p>\n'
content += '        <footer>&copy; 2026 WBank. All rights reserved.</footer>\n'
content += '    </div>\n</body>\n</html>'

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

sys.stdout.write('Written clean wbank/home.html\n')
sys.stdout.flush()
