import subprocess, os, sys, time

# Kill old processes
subprocess.run(['wmic', 'process', 'where', "name='python.exe'", 'call', 'terminate'],
               capture_output=True, timeout=10, shell=True)
time.sleep(2)

# Start on original ports
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
sys.stdout.write(f'Started PID: {proc.pid} on HTTP:8080, HTTPS:8443\n')
sys.stdout.flush()
