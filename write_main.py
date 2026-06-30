import sys

html = '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>泓財銀行 WBank - 專業金融服務</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #0c0c1d 0%, #1a1a3e 50%, #0c0c1d 100%);
            min-height: 100vh; color: white; overflow-x: hidden;
        }
        /* Particles canvas background */
        #particles-canvas {
            position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            z-index: 0; pointer-events: none; opacity: 0.4;
        }
        .container { position: relative; z-index: 1; max-width: 1200px; margin: 0 auto; padding: 40px 24px; }

        /* Nav */
        .nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 0; margin-bottom: 60px; }
        .nav .logo { font-size: 24px; font-weight: 700; letter-spacing: 2px; background: linear-gradient(135deg, #4fc3f7, #00bcd4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .nav .logo span { font-weight: 300; font-size: 14px; -webkit-text-fill-color: rgba(255,255,255,0.4); display: block; }
        .nav-links { display: flex; gap: 32px; align-items: center; }
        .nav-links a { color: rgba(255,255,255,0.6); text-decoration: none; font-size: 14px; transition: color 0.2s; }
        .nav-links a:hover { color: white; }
        .nav-links .btn-login {
            background: linear-gradient(135deg, #4fc3f7, #00bcd4); color: #0c0c1d !important;
            padding: 10px 28px; border-radius: 8px; font-weight: 600; font-size: 14px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .nav-links .btn-login:hover { transform: translateY(-1px); box-shadow: 0 8px 25px rgba(79,195,247,0.3); }

        /* Hero */
        .hero { display: flex; align-items: center; gap: 60px; margin-bottom: 80px; }
        .hero-text { flex: 1; }
        .hero-text .badge {
            display: inline-block; background: rgba(79,195,247,0.15); color: #4fc3f7;
            padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600;
            margin-bottom: 20px; border: 1px solid rgba(79,195,247,0.2);
        }
        .hero-text h1 { font-size: 48px; font-weight: 700; line-height: 1.15; margin-bottom: 20px; }
        .hero-text h1 span { background: linear-gradient(135deg, #4fc3f7, #00bcd4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .hero-text p { font-size: 16px; line-height: 1.7; color: rgba(255,255,255,0.5); max-width: 500px; margin-bottom: 32px; }
        .hero-text .btn-primary {
            background: linear-gradient(135deg, #4fc3f7, #00bcd4); color: #0c0c1d;
            padding: 14px 36px; border-radius: 10px; font-weight: 600; font-size: 16px;
            text-decoration: none; display: inline-block; transition: transform 0.2s, box-shadow 0.2s;
        }
        .hero-text .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 12px 35px rgba(79,195,247,0.3); }
        .hero-chart { flex: 1; background: rgba(255,255,255,0.03); border-radius: 16px; padding: 24px; border: 1px solid rgba(255,255,255,0.06); }
        .hero-chart canvas { width: 100% !important; height: auto !important; max-height: 300px; }

        /* Stats */
        .stats-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 80px; }
        .stat-card {
            background: rgba(255,255,255,0.03); border-radius: 12px; padding: 24px;
            border: 1px solid rgba(255,255,255,0.06); text-align: center;
            transition: transform 0.2s, background 0.2s;
        }
        .stat-card:hover { transform: translateY(-4px); background: rgba(255,255,255,0.06); }
        .stat-card .num { font-size: 32px; font-weight: 700; background: linear-gradient(135deg, #4fc3f7, #00bcd4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .stat-card .lbl { font-size: 13px; color: rgba(255,255,255,0.4); margin-top: 6px; }

        /* Features */
        .features { margin-bottom: 80px; }
        .features h2 { font-size: 32px; font-weight: 700; text-align: center; margin-bottom: 48px; }
        .features h2 span { background: linear-gradient(135deg, #4fc3f7, #00bcd4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
        .feature-card {
            background: rgba(255,255,255,0.03); border-radius: 12px; padding: 28px;
            border: 1px solid rgba(255,255,255,0.06); transition: transform 0.2s, background 0.2s;
        }
        .feature-card:hover { transform: translateY(-4px); background: rgba(255,255,255,0.06); }
        .feature-card .icon { font-size: 32px; margin-bottom: 16px; }
        .feature-card h4 { font-size: 18px; font-weight: 600; margin-bottom: 8px; }
        .feature-card p { font-size: 14px; color: rgba(255,255,255,0.4); line-height: 1.6; }

        /* Footer */
        .footer {
            text-align: center; padding: 32px 0; border-top: 1px solid rgba(255,255,255,0.06);
            font-size: 14px; color: rgba(255,255,255,0.3);
        }
        .footer a { color: rgba(255,255,255,0.4); text-decoration: none; }
        .footer a:hover { color: #4fc3f7; }

        @media (max-width: 768px) {
            .hero { flex-direction: column; }
            .hero-text h1 { font-size: 32px; }
            .stats-row { grid-template-columns: repeat(2, 1fr); }
            .feature-grid { grid-template-columns: 1fr; }
            .nav-links { gap: 16px; }
        }
    </style>
</head>
<body>
    <canvas id="particles-canvas"></canvas>
    <div class="container">
        <!-- Nav -->
        <div class="nav">
            <div class="logo">WBank<span>泓財銀行</span></div>
            <div class="nav-links">
                <a href="#features">服務</a>
                <a href="/admin" target="_blank">管理</a>
                <a href="/wbank" class="btn-login">登入</a>
            </div>
        </div>

        <!-- Hero -->
        <div class="hero">
            <div class="hero-text">
                <div class="badge">✦ ISO 27001 信息安全認證</div>
                <h1>智慧金融<br><span>由 WBank 開始</span></h1>
                <p>泓財銀行致力於提供安全、高效的金融科技服務。我們結合區塊鏈技術與傳統銀行業務，為您打造新一代的數位銀行體驗。</p>
                <a href="/wbank" class="btn-primary">立即體驗 →</a>
            </div>
            <div class="hero-chart">
                <canvas id="priceChart"></canvas>
            </div>
        </div>

        <!-- Stats -->
        <div class="stats-row">
            <div class="stat-card">
                <div class="num" id="stat_users">--</div>
                <div class="lbl">活躍用戶</div>
            </div>
            <div class="stat-card">
                <div class="num" id="stat_transactions">--</div>
                <div class="lbl">交易總數</div>
            </div>
            <div class="stat-card">
                <div class="num" id="stat_volume">--</div>
                <div class="lbl">交易量 (WTC)</div>
            </div>
            <div class="stat-card">
                <div class="num">99.9%</div>
                <div class="lbl">系統正常運行</div>
            </div>
        </div>

        <!-- Features -->
        <div class="features" id="features">
            <h2>我們的 <span>服務</span></h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="icon">💳</div>
                    <h4>泓通卡</h4>
                    <p>安全便捷的虛擬銀行卡，支援即時轉帳與支付。</p>
                </div>
                <div class="feature-card">
                    <div class="icon">🔄</div>
                    <h4>即時轉帳</h4>
                    <p>支援泓幣 (WCoins) 即時轉帳，秒級到帳。</p>
                </div>
                <div class="feature-card">
                    <div class="icon">🔒</div>
                    <h4>多重安全</h4>
                    <p>雙因素認證 (MFA)、SSL 加密傳輸，符合 ISO 27001 標準。</p>
                </div>
                <div class="feature-card">
                    <div class="icon">📊</div>
                    <h4>理財管理</h4>
                    <p>即時查看資產動態，支援多種貨幣匯率換算。</p>
                </div>
                <div class="feature-card">
                    <div class="icon">📱</div>
                    <h4>無縫體驗</h4>
                    <p>響應式設計，無論桌面或手機都能順暢使用。</p>
                </div>
                <div class="feature-card">
                    <div class="icon">📋</div>
                    <h4>審計追蹤</h4>
                    <p>完整操作記錄，符合 ISO 27001 審計要求。</p>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p>&copy; 2026 <a href="/">泓財銀行 WBank</a> | 專業金融科技服務 | <a href="/admin" target="_blank">管理後台</a></p>
        </div>
    </div>

    <script>
        // Particles background
        const canvas = document.getElementById('particles-canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        const particles = [];
        for (let i = 0; i < 60; i++) {
            particles.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.3,
                vy: (Math.random() - 0.5) * 0.3,
                r: Math.random() * 2 + 0.5,
                a: Math.random() * 0.5 + 0.1
            });
        }
        function drawParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach((p, i) => {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
                ctx.fillStyle = 'rgba(79, 195, 247, ' + p.a + ')';
                ctx.fill();
                p.x += p.vx; p.y += p.vy;
                if (p.x < 0 || p.x > canvas.width) p.vx *= -1;
                if (p.y < 0 || p.y > canvas.height) p.vy *= -1;
                for (let j = i + 1; j < particles.length; j++) {
                    const dx = p.x - particles[j].x;
                    const dy = p.y - particles[j].y;
                    const dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 120) {
                        ctx.beginPath();
                        ctx.moveTo(p.x, p.y);
                        ctx.lineTo(particles[j].x, particles[j].y);
                        ctx.strokeStyle = 'rgba(79, 195, 247, ' + (0.08 * (1 - dist / 120)) + ')';
                        ctx.lineWidth = 0.5;
                        ctx.stroke();
                    }
                }
            });
            requestAnimationFrame(drawParticles);
        }
        drawParticles();
        window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });

        // Chart.js price chart
        const ctx2 = document.getElementById('priceChart').getContext('2d');
        const labels = [];
        const data = [];
        let val = 28000;
        for (let i = 30; i >= 0; i--) {
            const d = new Date();
            d.setDate(d.getDate() - i);
            labels.push(d.toLocaleDateString('zh-HK', { month: 'short', day: 'numeric' }));
            val += (Math.random() - 0.48) * 2000;
            data.push(Math.round(val));
        }
        new Chart(ctx2, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    borderColor: '#4fc3f7',
                    backgroundColor: 'rgba(79, 195, 247, 0.05)',
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    borderWidth: 2,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: '#1a1a3e',
                        titleColor: '#fff',
                        bodyColor: '#4fc3f7',
                        cornerRadius: 8,
                        padding: 12,
                        callbacks: { label: function(ctx) { return 'WTC$' + ctx.parsed.y.toLocaleString(); } }
                    }
                },
                scales: {
                    x: { display: false },
                    y: {
                        display: true,
                        grid: { color: 'rgba(255,255,255,0.04)' },
                        ticks: {
                            color: 'rgba(255,255,255,0.3)',
                            callback: function(v) { return 'WTC$' + v.toLocaleString(); }
                        }
                    }
                }
            }
        });

        // Fetch real stats
        fetch('/wbank/home?accessKey=wbank')
            .then(r => r.json())
            .then(d => {
                if (d.count) document.getElementById('stat_users').textContent = d.count;
            }).catch(() => {});
    </script>
</body>
</html>'''

with open('E:\\wbank\\templates\\wbank.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Written professional wbank.html with Canvas chart')
