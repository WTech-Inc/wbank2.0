import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Add register link to login.html
tpl = open('E:\\wbank\\templates\\wbank\\login.html', 'r', encoding='utf-8').read()
link = '<div style="text-align:center;margin-top:18px;padding-top:16px;border-top:1px solid rgba(255,255,255,0.06);font-size:13px;color:#94a3b8;"><a href="/auth/reg" style="color:#4fc3f7;text-decoration:none;font-weight:600;">立即開户 →</a></div>'
if '</form>' in tpl and '立即開户' not in tpl:
    tpl = tpl.replace('</form>', '</form>\n' + link)
    open('E:\\wbank\\templates\\wbank\\login.html', 'w', encoding='utf-8').write(tpl)
    print('[OK] login.html 加入註册鏈結')
else:
    print('[OK] 已存在')

# 2. Check server is running
import subprocess, os, time
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], capture_output=True, text=True, timeout=10)
if 'python.exe' in result.stdout:
    print('[OK] Server 已運行中')
else:
    print('[INFO] Server not running - restarting...')
    env = os.environ.copy()
    env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
    env['HTTP_PORT'] = '8080'
    env['HTTPS_PORT'] = '8443'
    subprocess.Popen(['python', 'main.py'], cwd='E:\\wbank', env=env,
        stdout=open('E:\\wbank\\run.log', 'w'), stderr=subprocess.STDOUT,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
    print('[OK] Server restarted')

# 3. Check registration page works
try:
    import urllib.request
    r = urllib.request.urlopen('http://localhost:8080/auth/reg', timeout=5)
    print(f'[OK] /auth/reg returns HTTP {r.status}')
except Exception as e:
    print(f'[INFO] /auth/reg check: {e}')

print('\n=== DONE ===')
