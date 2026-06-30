import subprocess, os, sys

# Kill old server
try:
    subprocess.run(['wmic', 'process', 'where', "name='python.exe'", 'call', 'terminate'],
                   capture_output=True, timeout=10, shell=True)
except:
    pass

import time
time.sleep(2)

# Start new server on ports 80 and 443 directly
env = os.environ.copy()
env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
env['HTTP_PORT'] = '80'
env['HTTPS_PORT'] = '443'

proc = subprocess.Popen(
    ['python', 'main.py'],
    cwd='E:\\wbank',
    env=env,
    stdout=open('E:\\wbank\\run.log', 'w'),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)
sys.stdout.write(f'Started PID: {proc.pid} on HTTP:80, HTTPS:443\n')
sys.stdout.flush()
