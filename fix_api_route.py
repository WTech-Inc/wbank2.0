import sys
sys.stdout.reconfigure(encoding='utf-8')

# 1. Fix allowed routes in main.py
m = open('E:\\wbank\\main.py', 'r', encoding='utf-8').read()
old = "or path == '/auth/reg' or path.startswith('/auth/'):"
new = "or path == '/auth/reg' or path.startswith('/auth/') or path.startswith('/api/'):"
m = m.replace(old, new)
open('E:\\wbank\\main.py', 'w', encoding='utf-8').write(m)
print('[OK] /api/ added to allowed routes')

# 2. Re-add queue overlay to wbank.html
tpl = open('E:\\wbank\\templates\\wbank.html', 'r', encoding='utf-8').read()

queue_system = '''<!-- ===== QUEUE OVERLAY ===== -->
<div id="queue-overlay" style="position:fixed;top:0;left:0;width:100%;height:100%;z-index:99999;background:linear-gradient(135deg,#0c0c1d 0%,#1a1a3e 50%,#0c0c1d 100%);display:flex;justify-content:center;align-items:center;transition:opacity 0.8s ease,visibility 0.8s ease;font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,sans-serif;">
<div style="text-align:center;padding:40px;max-width:480px;width:100%;">
<div style="font-size:28px;font-weight:700;margin-bottom:8px;"><span style="background:linear-gradient(135deg,#4fc3f7,#00bcd4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;">WBank</span><span style="color:rgba(255,255,255,0.3);font-weight:300;font-size:14px;display:block;margin-top:4px;">泓財銀行</span></div>
<div style="margin:40px auto;width:80px;height:80px;position:relative;">
<svg viewBox="0 0 80 80" style="animation:qr 1.5s linear infinite;width:80px;height:80px;"><circle cx="40" cy="40" r="35" fill="none" stroke="rgba(79,195,247,0.1)" stroke-width="4"/><circle cx="40" cy="40" r="35" fill="none" stroke="#4fc3f7" stroke-width="4" stroke-dasharray="220" stroke-dashoffset="180" stroke-linecap="round" style="animation:qd 1.5s ease-in-out infinite alternate;"/></svg>
<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);"><span id="queue-number" style="color:#4fc3f7;font-size:20px;font-weight:700;">A042</span></div></div>
<h2 style="color:white;font-size:20px;font-weight:600;margin-bottom:12px;">系統繁忙，請按順序排隊</h2>
<p style="color:rgba(255,255,255,0.4);font-size:14px;margin-bottom:24px;line-height:1.6;">目前等待人數: <span id="wait-count" style="color:#4fc3f7;font-weight:600;">3</span> 人<br>預計等待時間: <span id="wait-time" style="color:#4fc3f7;font-weight:600;">約 5-8 秒</span></p>
<div style="background:rgba(255,255,255,0.08);border-radius:10px;height:6px;overflow:hidden;margin-bottom:8px;"><div id="queue-progress" style="height:100%;width:0%;border-radius:10px;background:linear-gradient(90deg,#4fc3f7,#00bcd4);transition:width 0.5s ease;"></div></div>
<p style="color:rgba(255,255,255,0.2);font-size:12px;">正在為您分配連線...</p>
<div style="margin-top:40px;display:flex;justify-content:center;gap:24px;flex-wrap:wrap;"><span style="color:rgba(255,255,255,0.15);font-size:11px;">SSL加密傳輸</span><span style="color:rgba(255,255,255,0.15);font-size:11px;">ISO 27001認證</span><span style="color:rgba(255,255,255,0.15);font-size:11px;">即時監控系統</span></div></div>
<style>@keyframes qr{100%{transform:rotate(360deg)}}@keyframes qd{0%{stroke-dashoffset:180}50%{stroke-dashoffset:60}100%{stroke-dashoffset:180}}</style></div>
<script>(function(){var Q={o:null,r:false,f:null,s:function(c){if(this.r)return;this.r=true;this.o=document.getElementById('queue-overlay');if(!this.o)return;this.o.style.opacity='1';this.o.style.visibility='visible';this.o.style.pointerEvents='auto';var q='A'+String(Math.floor(Math.random()*900)+100).padStart(3,'0');document.getElementById('queue-number').textContent=q;var w=Math.floor(Math.random()*5)+1;document.getElementById('wait-count').textContent=w;var d=Math.random()*3000+5000;var s=Date.now();var t=this;!function u(){var e=Date.now()-s,p=Math.min(e/d*100,100);document.getElementById('queue-progress').style.width=p+'%';if(e<d){var r=Math.max(0,Math.ceil((d-e)/1000));document.getElementById('wait-time').textContent='約 '+r+' 秒';document.getElementById('wait-count').textContent=Math.max(0,Math.ceil(w*(1-p/100)));requestAnimationFrame(u)}else{document.getElementById('wait-time').textContent='0 秒';document.getElementById('queue-progress').style.width='100%';setTimeout(function(){t.o.style.opacity='0';t.o.style.visibility='hidden';t.o.style.pointerEvents='none';t.r=false;if(t.f){clearTimeout(t.f);t.f=null}if(typeof c==='function')c()},500)}}();t.f=setTimeout(function(){t.o.style.opacity='0';t.o.style.visibility='hidden';t.o.style.pointerEvents='none';t.r=false;if(typeof c==='function')c()},d+2000)}};Q.s();document.querySelectorAll('.btn-login, .btn-primary').forEach(function(b){var h=b.getAttribute('href');if(h&&(h.indexOf('/wbank/auth')>=0||h.indexOf('/wbank/client')>=0)){b.addEventListener('click',function(e){e.preventDefault();Q.s(function(){window.location.href=h})})}})})();</script>
<!-- ===== END QUEUE OVERLAY ===== -->'''

if 'queue-overlay' not in tpl and '<body>' in tpl:
    tpl = tpl.replace('<body>', '<body>\n' + queue_system)
    open('E:\\wbank\\templates\\wbank.html', 'w', encoding='utf-8').write(tpl)
    print('[OK] Queue overlay re-added to wbank.html')
else:
    print('[OK] Queue already exists or no <body> found')

# 3. Verify syntax
import py_compile
py_compile.compile('E:\\wbank\\main.py', doraise=True)
print('[OK] main.py syntax OK')

print('\n=== Now restart server ===')
