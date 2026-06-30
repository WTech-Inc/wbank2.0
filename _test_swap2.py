import requests,json  
r=requests.post('http://localhost:9002/wbank/swap/apply',json={'amount':10},timeout=5)  
print('POST /wbank/swap/apply:')  
print(r.status_code, r.text[:300])  
r2=requests.get('http://localhost:9002/wbank/swap/history',timeout=5)  
print('GET /wbank/swap/history:')  
print(r2.status_code, r2.text[:300])  
