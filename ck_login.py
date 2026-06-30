with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

capture = False
for i, line in enumerate(lines):
    if 'def wbank_auth_client():' in line:
        print(f'=== wbank_auth_client (line {i+1}) ===')
        for j in range(i-2, min(i+30, len(lines))):
            if lines[j].strip():
                print(f'  {j+1}: {lines[j].rstrip()}')
        print()
    if 'def wbank_v1_auth_session():' in line:
        print(f'=== wbank_v1_auth_session (line {i+1}) ===')
        for j in range(i-2, min(i+40, len(lines))):
            if lines[j].strip():
                print(f'  {j+1}: {lines[j].rstrip()}')
        print()
