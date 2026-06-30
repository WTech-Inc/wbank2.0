"""Find all occurrences of wcoins/api/chain in main.py"""
f = open('main.py', 'rb')
d = f.read()
f.close()

count = d.count(b'wcoins/api/chain')
print(f'Occurrences: {count}')

pos = d.find(b'wcoins/api/chain', 0)
while pos >= 0:
    print(f'  at byte {pos}')
    pos = d.find(b'wcoins/api/chain', pos + 1)

# Also check for duplicate route decorators
count2 = d.count(b'@app.route("/wcoins/api/chain"')
print(f'Route decorators: {count2}')

count3 = d.count(b'def wcoins_api_chain')
print(f'Function defs: {count3}')
