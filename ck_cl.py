with open('E:\\wbank\\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in [845, 846, 847, 859, 860, 861, 1120, 1121, 1122, 1675, 1676, 1677, 1687, 1688, 1689]:
    if i < len(lines):
        print(f'{i+1}: {lines[i].rstrip()}')
