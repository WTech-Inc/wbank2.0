import requests  
s=requests.Session()  
r=s.post('http://localhost:9002/admin/login',data={'pw':'wbank@2026'},timeout=5)  
print('Login:', r.status_code, r.text[:100])  
r2=s.get('http://localhost:9002/admin/api/swaps',timeout=5)  
print('Swaps:', r2.status_code, r2.text[:300])  
r3=s.get('http://localhost:9002/admin_swap',timeout=5)  
print('Admin swap page:', r3.status_code, len(r3.text), 'bytes')  
