with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Try a simpler replacement - find the exact text around the try block
old_text = '''    user_ip = request.remote_addr

  try:
    res = requests.get(f"http://ip-api.com/json/{user_ip}").json()
  except requests.RequestException:
    return abort(502)

  if res["status"] != "fail":
    ip_address = res.get("query")
    org_info = res.get("org")
    if res.get("countryCode") == "CN":
      return redirect(f"/wtech/bockweb?place=cn&ip={ip_address}&org={org_info}")
    elif res.get("countryCode") == "TW":
      return redirect(f"/wtech/bockweb?place=tw&ip={ip_address}&org={org_info}")
    else:
      return render_template("wbank.html", site_key=CF_SITES_KEY)
  else:
    return abort(502)'''

new_text = '''    user_ip = request.remote_addr

    # Handle local/private IPs
    if user_ip in ('127.0.0.1', '::1', 'localhost') or user_ip.startswith(('192.168.', '10.', '172.16.')):
      return render_template("wbank.html", site_key=CF_SITES_KEY)

    try:
      res = requests.get(f"http://ip-api.com/json/{user_ip}").json()
    except requests.RequestException:
      return render_template("wbank.html", site_key=CF_SITES_KEY)

    if res["status"] != "fail":
      ip_address = res.get("query")
      org_info = res.get("org")
      if res.get("countryCode") == "CN":
        return redirect(f"/wtech/bockweb?place=cn&ip={ip_address}&org={org_info}")
      elif res.get("countryCode") == "TW":
        return redirect(f"/wtech/bockweb?place=tw&ip={ip_address}&org={org_info}")
      else:
        return render_template("wbank.html", site_key=CF_SITES_KEY)
    else:
      return render_template("wbank.html", site_key=CF_SITES_KEY)'''

if old_text in content:
    content = content.replace(old_text, new_text)
    print('Replaced successfully')
else:
    print('Could not find old text')
    idx = content.find('    user_ip = request.remote_addr')
    if idx >= 0:
        print(f'Found at {idx}:')
        print(content[idx:idx+400])

with open('E:\\wbank\\main.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('E:\\wbank\\main.py', doraise=True)
    print('Syntax OK')
except py_compile.PyCompileError as e:
    print(f'Syntax Error: {e}')
