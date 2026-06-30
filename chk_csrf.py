with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

routes_to_check = ['verify_user', 'freeze_user', 'update_balance']
found = 0
for i, line in enumerate(lines):
    for r in routes_to_check:
        if f'def admin_api_{r}():' in line:
            print(f'--- {r} (line {i+1}) ---')
            for j in range(max(0,i-5), min(len(lines), i+2)):
                print(f'  {j+1}: {lines[j].rstrip()}')
            found += 1
if found == 0:
    print('Did not find any admin API functions')
