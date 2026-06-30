import requests,json  
r=requests.get('http://localhost:9002/wbank/swap/info',timeout=5)  
print(r.status_code, r.json())  
r2=requests.post('http://localhost:9002/wbank/swap/apply',json={amount:10},headers={'Content-Type':'application/json'},timeout=5)  
print('POST /wbank/swap/apply:')  
print(r2.status_code, r2.text[:200])  
r3=requests.get('http://localhost:9002/wbank/swap/history',timeout=5)  
print('GET /wbank/swap/history:')  
print(r3.status_code, r3.text[:200])  
