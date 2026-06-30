import subprocess, os, time

# Kill old
subprocess.run(['taskkill', '/f', '/im', 'python.exe'], capture_output=True, timeout=10)
time.sleep(2)

# Start new
env = os.environ.copy()
env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
env['HTTP_PORT'] = '8080'
env['HTTPS_PORT'] = '8443'

proc = subprocess.Popen(
    ['python', 'main.py'],
    cwd='E:\\wbank',
    env=env,
    stdout=open('E:\\wbank\\run.log', 'w'),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)

time.sleep(3)

# Verify
r = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe', '/NH'], capture_output=True, text=True, timeout=10)
if 'python' in r.stdout:
    print('OK Server running PID:', proc.pid)
else:
    print('FAIL: Python not running')
    # Check log
    try:
        log = open('E:\\wbank\\run.log', 'r').read()
        print('LOG:', log[-500:])
    except:
        pass
