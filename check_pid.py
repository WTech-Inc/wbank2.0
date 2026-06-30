import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

# Check PID 11780
r = subprocess.run(['tasklist', '/FI', 'PID eq 11780', '/V'], capture_output=True, text=True, timeout=10, shell=True)
print('PID 11780:')
print(r.stdout)

# Check all listening on port 8080
r2 = subprocess.run('netstat -ano | findstr ":8080"', capture_output=True, text=True, timeout=10, shell=True)
lines = r2.stdout.strip().split('\n')
pids = set()
for line in lines:
    parts = line.strip().split()
    if len(parts) >= 5:
        pids.add(parts[-1])
print(f'PIDs on port 8080: {pids}')

# Get process details for each
for pid in pids:
    if pid != '0':
        r3 = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/V'], capture_output=True, text=True, timeout=10, shell=True)
        print(f'\nPID {pid}:')
        print(r3.stdout)

# Try to find the actual python binary
r4 = subprocess.run(['where', 'python*'], capture_output=True, text=True, timeout=10, shell=True)
print(f'\nPython executables:')
print(r4.stdout)
