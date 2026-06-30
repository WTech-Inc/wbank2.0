import sys, base64

html = '''<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>WBank 管理後台</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { background: #f0f2f5; font-family: 'Segoe UI', -apple-system, sans-serif; }
        .sidebar {
            width: 260px; height: 100vh; position: fixed; top: 0; left: 0;
            background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
            color: white; padding: 0; z-index: 100; display: flex; flex-direction: column;
        }
        .sidebar .brand {
            padding: 24px 24px; font-size: 18px; font-weight: 700;
            border-bottom: 1px solid rgba(255,255,255,0.08); letter-spacing: 1px;
            background: rgba(255,255,255,0.03);
        }
        .sidebar .brand i { margin-right: 10px; color: #4fc3f7; }
        .sidebar .nav-section { padding: 16px 24px 8px; font-size: 11px; text-transform: uppercase; letter-spacing: 2px; color: rgba(255,255,255,0.35); }
        .sidebar a {
            color: rgba(255,255,255,0.65); text-decoration: none; display: flex; align-items: center;
            padding: 12px 24px; transition: all 0.2s; font-size: 14px; border-left: 3px solid transparent;
        }
        .sidebar a:hover, .sidebar a.active { background: rgba(255,255,255,0.06); color: white; border-left-color: #4fc3f7; }
        .sidebar a i { margin-right: 12px; font-size: 18px; width: 20px; text-align: center; }
        .sidebar .logout { margin-top: auto; border-top: 1px solid rgba(255,255,255,0.08); }
        .content { margin-left: 260px; padding: 24px 32px; }
        .topbar {
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 28px; padding-bottom: 16px; border-bottom: 1px solid #e8ecf1;
        }
        .topbar h4 { font-weight: 600; color: #1a1a2e; margin: 0; }
        .topbar .user-badge { display: flex; align-items: center; gap: 8px; color: #64748b; font-size: 14px; }
        .topbar .user-badge i { font-size: 20px; color: #4fc3f7; }
        .stat-card {
            background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            transition: transform 0.2s, box-shadow 0.2s; border: 1px solid #e8ecf1;
        }
        .stat-card:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.08); }
        .stat-card .stat-icon { width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 22px; }
        .stat-card .number { font-size: 28px; font-weight: 700; color: #1a1a2e; }
        .stat-card .label { font-size: 13px; color: #94a3b8; margin-top: 4px; }
        .table-container { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); border: 1px solid #e8ecf1; }
        .section { display: none; }
        .section.active { display: block; }
        .flash-msg { padding: 12px 16px; border-radius: 8px; margin-bottom: 16px; font-size: 14px; }
        .flash-msg.error { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
        .flash-msg.success { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }
        .flash-msg.info { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
        .search-box { border: 1px solid #e2e8f0; border-radius: 8px; padding: 8px 14px; width: 100%; font-size: 14px; }
        .search-box:focus { outline: none; border-color: #4fc3f7; box-shadow: 0 0 0 3px rgba(79,195,247,0.1); }
        .btn-action { padding: 4px 12px; font-size: 12px; border-radius: 6px; }
        .pagination { margin-top: 16px; }
        .page-link { border: none; color: #64748b; padding: 6px 12px; border-radius: 6px !important; margin: 0 2px; }
        .page-link:hover { background: #f1f5f9; color: #1a1a2e; }
        .page-item.active .page-link { background: #1a1a2e; color: white; }
        .export-bar { display: flex; gap: 8px; align-items: center; }
        .export-bar .btn { font-size: 13px; padding: 6px 16px; border-radius: 8px; }
        .login-screen {
            max-width: 420px; margin: 80px auto; background: white; padding: 40px;
            border-radius: 16px; box-shadow: 0 20px 60px rgba(0,0,0,0.08);
        }
        .login-screen h2 { text-align: center; font-weight: 700; color: #1a1a2e; margin-bottom: 8px; }
        .login-screen .subtitle { text-align: center; color: #94a3b8; margin-bottom: 32px; font-size: 14px; }
        .loading { text-align: center; padding: 40px; color: #94a3b8; }
        @media (max-width: 768px) {
            .sidebar { width: 100%; height: auto; position: relative; }
            .content { margin-left: 0; padding: 16px; }
            .stat-card { margin-bottom: 12px; }
        }
    </style>
</head>
<body>

{% if not session.admin_user %}
<!-- Login Screen -->
<div class="login-screen">
    <div style="text-align:center;font-size:48px;margin-bottom:16px;color:#1a1a2e;">🏦</div>
    <h2>WBank 管理後台</h2>
    <p class="subtitle">請使用管理員帳號登入</p>
    {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
    {% for category, message in messages %}
    <div class="flash-msg {{ category }}">{{ message }}</div>
    {% endfor %}
    {% endif %}
    {% endwith %}
    <form action="/admin/login" method="POST">
        <div class="mb-3">
            <label class="form-label" style="font-size:13px;color:#64748b;">用戶名</label>
            <input type="text" name="user" class="form-control" required placeholder="請輸入用戶名">
        </div>
        <div class="mb-3">
            <label class="form-label" style="font-size:13px;color:#64748b;">密碼</label>
            <input type="password" name="pw" class="form-control" required placeholder="請輸入密碼">
        </div>
        <button type="submit" class="btn btn-dark w-100 py-2" style="background:#1a1a2e;">登入</button>
    </form>
    <p class="text-center mt-4" style="font-size:13px;"><a href="/wbank" style="color:#94a3b8;text-decoration:none;">← WBank 首頁</a></p>
</div>
{% else %}

<!-- Sidebar -->
<div class="sidebar">
    <div class="brand"><i class="bi bi-shield-shaded"></i>WBank Admin</div>
    <div class="nav-section">Main</div>
    <a href="#" class="active" onclick="showSection('dashboard', this)"><i class="bi bi-speedometer2"></i> Dashboard</a>
    <a href="#" onclick="showSection('users', this)"><i class="bi bi-people"></i> Users</a>
    <a href="#" onclick="showSection('audit', this)"><i class="bi bi-journal-text"></i> Audit Log</a>
    <div class="nav-section">Data</div>
    <a href="#" onclick="showSection('export', this)"><i class="bi bi-download"></i> Export</a>
    <a href="/admin/logout" class="logout"><i class="bi bi-box-arrow-right"></i> Logout</a>
</div>

<!-- Main Content -->
<div class="content">
    <div class="topbar">
        <h4><i class="bi bi-shield-shaded me-2" style="color:#4fc3f7;"></i>管理後台</h4>
        <div class="user-badge"><i class="bi bi-person-circle"></i> {{ session.admin_user }}</div>
    </div>

    {% with messages = get_flashed_messages(with_categories=true) %}
    {% if messages %}
    {% for category, message in messages %}
    <div class="flash-msg {{ category }}">{{ message }}</div>
    {% endfor %}
    {% endif %}
    {% endwith %}

    <!-- Dashboard -->
    <div id="section-dashboard" class="section active">
        <div class="row g-3" id="stats-container">
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-icon" style="background:#e0f2fe;color:#0284c7;"><i class="bi bi-people"></i></div>
                    <div class="number" id="stat-users">-</div>
                    <div class="label">Total Users</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-icon" style="background:#fef3c7;color:#d97706;"><i class="bi bi-pencil-square"></i></div>
                    <div class="number" id="stat-kyc">-</div>
                    <div class="label">Pending KYC</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-icon" style="background:#fce7f3;color:#db2777;"><i class="bi bi-arrow-left-right"></i></div>
                    <div class="number" id="stat-records">-</div>
                    <div class="label">Transactions</div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="stat-card">
                    <div class="stat-icon" style="background:#dcfce7;color:#16a34a;"><i class="bi bi-journal-text"></i></div>
                    <div class="number" id="stat-audit">-</div>
                    <div class="label">Audit Entries</div>
                </div>
            </div>
        </div>
    </div>

    <!-- Users -->
    <div id="section-users" class="section">
        <div class="table-container">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 style="font-weight:600;color:#1a1a2e;margin:0;">User Management</h5>
                <div class="export-bar">
                    <button class="btn btn-outline-secondary btn-sm" onclick="exportCSV('users')"><i class="bi bi-download"></i> CSV</button>
                </div>
            </div>
            <input type="text" class="search-box mb-3" id="user-search" placeholder="Search username..." onkeyup="filterUsers()">
            <div class="table-responsive">
                <table class="table table-hover align-middle" style="font-size:14px;">
                    <thead style="background:#f8fafc;color:#64748b;font-size:12px;text-transform:uppercase;letter-spacing:0.5px;">
                        <tr><th>Username</th><th>Balance</th><th>Account</th><th>Status</th><th>Role</th><th>Actions</th></tr>
                    </thead>
                    <tbody id="users-tbody"><tr><td colspan="6" class="loading">Loading...</td></tr></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- Audit Log -->
    <div id="section-audit" class="section">
        <div class="table-container">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h5 style="font-weight:600;color:#1a1a2e;margin:0;">Audit Log (ISO 27001)</h5>
                <div class="export-bar">
                    <button class="btn btn-outline-secondary btn-sm" onclick="exportCSV('audit')"><i class="bi bi-download"></i> CSV</button>
                    <button class="btn btn-outline-secondary btn-sm" onclick="exportJSON('audit')"><i class="bi bi-download"></i> JSON</button>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-4"><input type="text" class="search-box" id="audit-action-search" placeholder="Filter by action..." onkeyup="loadAuditLog()"></div>
                <div class="col-md-4"><input type="text" class="search-box" id="audit-user-search" placeholder="Filter by user..." onkeyup="loadAuditLog()"></div>
                <div class="col-md-2"><button class="btn btn-outline-primary btn-sm w-100" onclick="loadAuditLog()"><i class="bi bi-arrow-clockwise"></i> Refresh</button></div>
            </div>
            <div class="table-responsive">
                <table class="table table-sm table-hover" style="font-size:13px;">
                    <thead style="background:#f8fafc;color:#64748b;font-size:11px;text-transform:uppercase;">
                        <tr><th>ID</th><th>Timestamp</th><th>User</th><th>Action</th><th>Detail</th><th>IP</th></tr>
                    </thead>
                    <tbody id="audit-tbody"><tr><td colspan="6" class="loading">Loading...</td></tr></tbody>
                </table>
            </div>
            <nav><ul class="pagination pagination-sm" id="audit-pagination"></ul></nav>
        </div>
    </div>

    <!-- Export -->
    <div id="section-export" class="section">
        <div class="row g-3">
            <div class="col-md-4">
                <div class="table-container text-center p-4">
                    <i class="bi bi-people" style="font-size:48px;color:#4fc3f7;"></i>
                    <h6 class="mt-3 fw-bold">Export Users</h6>
                    <p style="font-size:13px;color:#94a3b8;">Export all user data as CSV</p>
                    <button class="btn btn-dark w-100" onclick="exportCSV('users')"><i class="bi bi-download"></i> Export CSV</button>
                </div>
            </div>
            <div class="col-md-4">
                <div class="table-container text-center p-4">
                    <i class="bi bi-journal-text" style="font-size:48px;color:#4fc3f7;"></i>
                    <h6 class="mt-3 fw-bold">Export Audit Log</h6>
                    <p style="font-size:13px;color:#94a3b8;">Export audit log as CSV or JSON</p>
                    <div class="d-flex gap-2">
                        <button class="btn btn-dark flex-fill" onclick="exportCSV('audit')"><i class="bi bi-download"></i> CSV</button>
                        <button class="btn btn-outline-dark flex-fill" onclick="exportJSON('audit')"><i class="bi bi-download"></i> JSON</button>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="table-container text-center p-4">
                    <i class="bi bi-filetype-json" style="font-size:48px;color:#4fc3f7;"></i>
                    <h6 class="mt-3 fw-bold">Export All Data</h6>
                    <p style="font-size:13px;color:#94a3b8;">Export complete system data as JSON</p>
                    <button class="btn btn-dark w-100" onclick="exportJSON('all')"><i class="bi bi-download"></i> Export JSON</button>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
function showSection(id, el) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.getElementById('section-' + id).classList.add('active');
    document.querySelectorAll('.sidebar a').forEach(a => a.classList.remove('active'));
    if (el) el.classList.add('active');
    if (id === 'dashboard') loadStats();
    if (id === 'users') loadUsers();
    if (id === 'audit') { auditPage = 1; loadAuditLog(); }
}

// Stats
function loadStats() {
    fetch('/admin/api/stats')
        .then(r => r.json())
        .then(d => {
            document.getElementById('stat-users').textContent = d.total_users || 0;
            document.getElementById('stat-kyc').textContent = d.pending_kyc || 0;
            document.getElementById('stat-records').textContent = d.total_records || 0;
            document.getElementById('stat-audit').textContent = d.audit_count || 0;
        }).catch(() => {});
}
loadStats();

// Users
function loadUsers() {
    const tb = document.getElementById('users-tbody');
    tb.innerHTML = '<tr><td colspan="6" class="loading">Loading...</td></tr>';
    fetch('/admin/api/users')
        .then(r => r.json())
        .then(users => {
            if (!Array.isArray(users) || users.length === 0) {
                tb.innerHTML = '<tr><td colspan="6" class="text-center py-4" style="color:#94a3b8;">No users</td></tr>'; return;
            }
            tb.innerHTML = users.map(u => {
                let badge = u.verify === 'yes' ? 'bg-success' : 'bg-warning';
                let label = u.verify === 'yes' ? 'Verified' : 'Pending';
                if (u.sub && u.sub.includes('Freeze')) { badge = 'bg-danger'; label = 'Frozen'; }
                return `<tr class="user-row" data-username="${u.username}">
                    <td><strong>${u.username}</strong></td>
                    <td>WTC$${u.balance}</td>
                    <td style="font-size:12px;color:#64748b;">${u.accnumber || '-'}</td>
                    <td><span class="badge ${badge}">${label}</span></td>
                    <td>${u.role || 'NonVerify'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-success btn-action" onclick="verifyUser('${u.username}')">Verify</button>
                        <button class="btn btn-sm btn-outline-warning btn-action" onclick="toggleFreeze('${u.username}')">Freeze</button>
                        <button class="btn btn-sm btn-outline-info btn-action" onclick="adjustBalance('${u.username}')">Balance</button>
                    </td>
                </tr>`;
            }).join('');
        }).catch(e => tb.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Error: ${e.message}</td></tr>`);
}

function filterUsers() {
    const q = document.getElementById('user-search').value.toLowerCase();
    document.querySelectorAll('.user-row').forEach(r => {
        r.style.display = r.dataset.username.includes(q) ? '' : 'none';
    });
}

function verifyUser(username) {
    if (!confirm(`Verify user ${username}?`)) return;
    fetch('/admin/api/verify_user', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({username: username})})
        .then(r => r.json()).then(d => { if (d.success) { alert('Verified'); loadUsers(); loadAuditLog(); } else alert(d.error); }).catch(e => alert(e));
}
function toggleFreeze(username) {
    if (!confirm(`Toggle freeze for ${username}?`)) return;
    fetch('/admin/api/freeze_user', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({username: username})})
        .then(r => r.json()).then(d => { if (d.success) { alert(d.action); loadUsers(); loadAuditLog(); } else alert(d.error); }).catch(e => alert(e));
}
function adjustBalance(username) {
    const amount = prompt(`Adjust balance for ${username}:\\n(positive = add, negative = subtract)`);
    if (amount === null || isNaN(parseInt(amount))) return;
    if (!confirm(`Adjust ${username} balance by ${parseInt(amount)}?`)) return;
    fetch('/admin/api/update_balance', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({username: username, amount: parseInt(amount)})})
        .then(r => r.json()).then(d => { if (d.success) { alert(`New balance: WTC$${d.new_balance}`); loadUsers(); loadAuditLog(); } else alert(d.error); }).catch(e => alert(e));
}

// Audit Log
let auditPage = 1;
function loadAuditLog() {
    const tb = document.getElementById('audit-tbody');
    tb.innerHTML = '<tr><td colspan="6" class="loading">Loading...</td></tr>';
    const actionFilter = document.getElementById('audit-action-search').value;
    const userFilter = document.getElementById('audit-user-search').value;
    let url = `/admin/api/audit_log?page=${auditPage}&per_page=50`;
    if (actionFilter) url += `&action=${encodeURIComponent(actionFilter)}`;
    if (userFilter) url += `&username=${encodeURIComponent(userFilter)}`;
    fetch(url)
        .then(r => r.json()).then(d => {
            if (!d.entries || d.entries.length === 0) {
                tb.innerHTML = '<tr><td colspan="6" class="text-center py-4" style="color:#94a3b8;">No entries</td></tr>';
                document.getElementById('audit-pagination').innerHTML = ''; return;
            }
            tb.innerHTML = d.entries.map(e => `<tr>
                <td style="color:#94a3b8;">${e.id}</td>
                <td style="font-size:12px;">${e.timestamp}</td>
                <td><strong>${e.username}</strong></td>
                <td><span class="badge bg-secondary" style="font-size:11px;">${e.action}</span></td>
                <td style="max-width:300px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:12px;color:#64748b;" title="${e.detail || ''}">${e.detail || '-'}</td>
                <td style="font-size:12px;color:#94a3b8;">${e.ip_address || '-'}</td>
            </tr>`).join('');
            const totalPages = Math.ceil(d.total / d.per_page);
            let pg = '<li class="page-item"><a class="page-link" href="#" onclick="auditPage=' + Math.max(1, auditPage - 1) + '; loadAuditLog(); return false;">\\u00ab</a></li>';
            for (let i = Math.max(1, auditPage - 2); i <= Math.min(totalPages, auditPage + 2); i++) {
                pg += `<li class="page-item ${i === auditPage ? 'active' : ''}"><a class="page-link" href="#" onclick="auditPage=${i}; loadAuditLog(); return false;">${i}</a></li>`;
            }
            pg += '<li class="page-item"><a class="page-link" href="#" onclick="auditPage=' + Math.min(totalPages, auditPage + 1) + '; loadAuditLog(); return false;">\\u00bb</a></li>';
            document.getElementById('audit-pagination').innerHTML = pg;
        }).catch(e => tb.innerHTML = `<tr><td colspan="6" class="text-center text-danger">Error: ${e.message}</td></tr>`);
}

// Export functions
function exportCSV(type) {
    const url = type === 'users' ? '/admin/api/export/users' : '/admin/api/export/audit_log';
    window.open(url, '_blank');
}
function exportJSON(type) {
    const url = type === 'audit' ? '/admin/api/export/audit_json' : '/admin/api/export/json';
    window.open(url, '_blank');
}
</script>
{% endif %}
</body>
</html>'''

path = 'E:\\wbank\\templates\\admin\\index.html'
with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Written admin template with export features')
