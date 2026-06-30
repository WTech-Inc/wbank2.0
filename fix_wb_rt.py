with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add local IP check to /wbank route before ip-api call
old = '''  else:
    user_ip = request.remote_addr

  try:
    res = requests.get(f"http://ip-api.com/json/{user_ip}").json()
  except requests.RequestException:
    return abort(502)'''

new = '''  else:
    user_ip = request.remote_addr

  # Handle local/private IPs
  if user_ip in ('127.0.0.1', '::1', 'localhost') or user_ip.startswith(('192.168.', '10.', '172.16.')):
    return render_template("wbank.html", site_key=CF_SITES_KEY)

  try:
    res = requests.get(f"http://ip-api.com/json/{user_ip}").json()
  except requests.RequestException:
    return render_template("wbank.html", site_key=CF_SITES_KEY)'''

content = content.replace(old, new)

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
