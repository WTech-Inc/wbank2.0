import subprocess, os, sys, time

# Kill all python.exe
subprocess.run(['wmic', 'process', 'where', "name='python.exe'", 'call', 'terminate'],
               capture_output=True, timeout=10, shell=True)
time.sleep(3)

env = os.environ.copy()
env['dataurl'] = 'postgresql://neondb_owner:npg_KP2Zat1YscBz@ep-cool-scene-a15ejn0l-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require'
env['HTTP_PORT'] = '8080'
env['HTTPS_PORT'] = '8443'

# CRITICAL: Set working directory to E:\wbank
python_exe = r'C:\Users\wangtry\AppData\Local\Microsoft\WindowsApps\python.exe'
proc = subprocess.Popen(
    [python_exe, 'main.py'],
    cwd='E:\\wbank',  # This is the fix!
    env=env,
    stdout=open('E:\\wbank\\run.log', 'w', encoding='utf-8'),
    stderr=subprocess.STDOUT,
    creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
)
sys.stdout.write(f'Started PID: {proc.pid}\n')
sys.stdout.flush()
