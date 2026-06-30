with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find @app.route("/wbank") (line 1660)
for i, line in enumerate(lines):
    if 'app.route("/wbank")' in line or line.strip() == '@app.route("/wbank")':
        for j in range(i, min(i+20, len(lines))):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
