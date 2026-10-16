import os
import glob
import sqlite3
import time
import hashlib
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

ADMIN_USERNAME = "kurdistan01"
ADMIN_PASSWORD_HASH = hashlib.sha256("Kurdistan@2026#Eagle".encode()).hexdigest()
SITE_LOCKED = False

ip_requests = {}
BLOCKED_IPS = set()
MAX_REQ_PER_MINUTE = 25

def check_rate_limit(ip):
    now = time.time()
    if ip in BLOCKED_IPS:
        return False
    reqs = ip_requests.get(ip, [])
    reqs = [t for t in reqs if now - t < 60]
    reqs.append(now)
    ip_requests[ip] = reqs
    if len(reqs) > MAX_REQ_PER_MINUTE:
        BLOCKED_IPS.add(ip)
        return False
    return True

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'no-referrer'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.before_request
def block_sensitive_files():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    if not check_rate_limit(ip):
        return jsonify({"error": "ئایپییەکەت بلۆک کرا بەهۆی زۆری داواکاری گوماناوی!"}), 429
    
    path = request.path.lower()
    if ".db" in path or ".sqlite" in path or ".py" in path or ".env" in path:
        abort(403)

# دیزاینی تەواوی ڕووکاری تاریکی (Darkness Eagle) بە شێوەی ڕاستەوخۆ
MAIN_HTML_PAGE = """<!DOCTYPE html>
<html lang="ckb" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Darkness Eagle | سیستەمی چاوی هەڵۆی تاریکی</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: Tahoma, sans-serif; }
        body { background-color: #020408; color: #f3f4f6; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 20px; }
        .container { width: 100%; max-width: 800px; margin-top: 40px; }
        header { text-align: center; margin-bottom: 30px; }
        h1 { color: #facc15; font-size: 26px; margin-bottom: 8px; text-shadow: 0 0 15px rgba(250,204,21,0.3); }
        p.sub { color: #9ca3af; font-size: 14px; }
        .search-box { background: rgba(14, 18, 26, 0.95); border: 1.5px solid #1f2937; border-radius: 14px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
        .input-group { display: flex; gap: 10px; margin-bottom: 15px; }
        input[type="text"] { flex: 1; padding: 12px 16px; background: #04060a; border: 1px solid #374151; border-radius: 8px; color: #fff; font-size: 15px; outline: none; }
        input[type="text"]:focus { border-color: #10b981; box-shadow: 0 0 10px rgba(16,185,129,0.2); }
        button { padding: 12px 24px; background: #065f46; border: 1px solid #10b981; color: #fff; border-radius: 8px; font-weight: bold; cursor: pointer; transition: 0.2s; }
        button:hover { background: #047857; }
        #results { margin-top: 20px; display: flex; flex-direction: column; gap: 10px; }
        .result-card { background: rgba(17, 24, 39, 0.8); border: 1px solid #374151; border-radius: 8px; padding: 14px; font-size: 13.5px; }
        .result-card b { color: #34d399; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🦅 سیستەمی چاوی هەڵۆی تاریکی</h1>
            <p class="sub">گەڕانی خێرا و پێشکەوتوو لە ناو داتابەیسەکاندا</p>
        </header>
        <div class="search-box">
            <div class="input-group">
                <input type="text" id="searchInput" placeholder="ناوی سیانی، ژمارە، یان هەر زانیارییەک بنووسە بۆ گەڕان..." onkeypress="if(event.key==='Enter') doSearch()">
                <button onclick="doSearch()">گەڕان</button>
            </div>
            <div id="results"></div>
        </div>
    </div>
    <script>
        async function doSearch() {
            const query = document.getElementById('searchInput').value.trim();
            const resDiv = document.getElementById('results');
            if(!query) { alert('تکایە شتێک بنووسە بۆ گەڕان!'); return; }
            resDiv.innerHTML = '<p style="text-align:center; color:#9ca3af; padding:10px;">پشکنین و گەڕان بەڕێوەیە...</p>';
            try {
                const response = await fetch('/api/search', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({q: query})
                });
                const data = await response.json();
                if(data.error) { resDiv.innerHTML = '<p style="color:#ef4444; text-align:center;">'+data.error+'</p>'; return; }
                if(!data.records || data.records.length === 0) { resDiv.innerHTML = '<p style="color:#facc15; text-align:center;">هیچ ئەنجامێک نەدۆزرایەوە.</p>'; return; }
                let html = '<p style="font-size:12px; color:#9ca3af; margin-bottom:5px;">ژمارەی ئەنجامەکان: '+data.count+'</p>';
                data.records.forEach(rec => {
                    html += '<div class="result-card">';
                    for(let key in rec) {
                        if(key !== '_table') {
                            html += '<div><b>'+key+':</b> '+rec[key]+'</div>';
                        }
                    }
                    html += '<div style="margin-top:6px; font-size:11px; color:#60a5fa;">چاوگە: '+rec._table+'</div>';
                    html += '</div>';
                });
                resDiv.innerHTML = html;
            } catch(e) {
                resDiv.innerHTML = '<p style="color:#ef4444; text-align:center;">کێشەیەک روویدا لە پەیوەندیکردن بە سێرڤەرەوە.</p>';
            }
        }
    </script>
</body>
</html>"""

@app.route('/')
def home():
    if SITE_LOCKED:
        return "سایتەکە داخراوە", 503
    return MAIN_HTML_PAGE, 200

@app.route('/api/search', methods=['POST', 'GET'])
def search_database():
    if SITE_LOCKED:
        return jsonify({"error": "سایتەکە داخراوە!"}), 503

    payload = request.get_json(silent=True) or {}
    general_q = payload.get("q", "").strip() if request.method == 'POST' else request.args.get("q", "").strip()
    
    if not general_q:
        return jsonify({"error": "تکایە زانیاری بنووسە بۆ گەڕان!"}), 400

    db_files = glob.glob("*.db") + glob.glob("*.sqlite") + glob.glob("*.sqlite3") + glob.glob("databases/*.db")
    db_files = sorted(list(set(db_files)))
    
    if not db_files:
        return jsonify({"error": "هیچ فایلێکی داتابەیس لەسەر سێرڤەر نییە!"}), 404

    results = []
    for db_path in db_files:
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [r["name"] for r in cursor.fetchall()]

            for table in tables:
                cursor.execute(f'PRAGMA table_info("{table}")')
                columns = [col["name"] for col in cursor.fetchall()]
                if not columns:
                    continue
                col_checks = [f'CAST("{col}" AS TEXT) LIKE ?' for col in columns]
                query_sql = f'SELECT * FROM "{table}" WHERE ' + " OR ".join(col_checks) + ' LIMIT 20'
                params = [f"%{general_q}%"] * len(columns)
                
                cursor.execute(query_sql, params)
                for row in cursor.fetchall():
                    row_dict = {k: row[k] for k in row.keys() if row[k] is not None and str(row[k]).strip() != ""}
                    row_dict["_table"] = f"{os.path.basename(db_path)} -> {table}"
                    results.append(row_dict)
                    if len(results) >= 20:
                        break
                if len(results) >= 20:
                    break
            conn.close()
        except Exception:
            continue
        if len(results) >= 20:
            break

    return jsonify({"count": len(results), "records": results})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
