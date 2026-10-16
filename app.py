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

LOCKED_HTML_PAGE = """<!DOCTYPE html>
<html lang="ckb" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Darkness Eagle | سیستەمی چاوی هەڵۆی تاریکی</title>
    <style>
        body { background: #020408; color: #f3f4f6; font-family: Tahoma, sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; text-align: center; }
        .box { background: rgba(14, 18, 26, 0.96); border: 1.5px solid #ef4444; border-radius: 16px; padding: 30px 24px; max-width: 440px; width: 90%; box-shadow: 0 0 40px rgba(239, 68, 68, 0.25); }
        h1 { color: #facc15; font-size: 20px; margin-bottom: 12px; }
        p { color: #cbd5e1; font-size: 13.5px; line-height: 1.8; margin-bottom: 20px; }
        .admin-unlock { margin-top: 15px; border-top: 1px solid #1f2937; padding-top: 14px; }
        input { width: 100%; padding: 9px; background: #04060a; border: 1px solid #374151; border-radius: 7px; color: #fff; margin-bottom: 8px; text-align: center; }
        button { width: 100%; padding: 9px; background: #065f46; border: 1px solid #10b981; color: #fff; border-radius: 7px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="box">
        <div style="font-size:42px; margin-bottom:10px;">🔒</div>
        <h1>سیستەمی چاوی هەڵۆی تاریکی لە ئێستادا داخراوە</h1>
        <p>ئەم وێبسایتە لەلایەن بەڕێوەبەری گشتییەوە بە شێوەی کاتی ڕاگیراوە و لەژێر نۆژەنکردنەوەدایە. تکایە دواتر سەردان بکەنەوە.</p>
        <div class="admin-unlock">
            <input type="password" id="adminKey" placeholder="کلیلی نهێنی خاوەنی سایت بۆ کردنەوە...">
            <button onclick="unlockSite()">کردنەوەی سایت (تەنها ئەدمین)</button>
        </div>
    </div>
    <script>
        async function unlockSite() {
            const pass = document.getElementById('adminKey').value;
            const res = await fetch('/api/admin/lock', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({password: pass, lock: false})
            });
            const data = await res.json();
            if (data.success) { location.reload(); } else { alert('کلیلی ئەدمین هەڵەیە!'); }
        }
    </script>
</body>
</html>"""

@app.route('/')
def home():
    if SITE_LOCKED:
        return LOCKED_HTML_PAGE, 503
    
    html_path = os.path.join(os.getcwd(), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
            
    return "سیستەمی چاوی هەڵۆی تاریکی چالاکە. تکایە فایلی index.html باربکە.", 200

@app.route('/api/admin/lock', methods=['POST'])
def toggle_site_lock():
    global SITE_LOCKED
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    if password == "Kurdistan01" or hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
        SITE_LOCKED = bool(data.get("lock", not SITE_LOCKED))
        return jsonify({
            "success": True,
            "site_locked": SITE_LOCKED,
            "message": "سایتەکە بە سەرکەوتوویی داخرا بۆ خەڵک!" if SITE_LOCKED else "سایتەکە کرایەوە بۆ بەکارهێنان!"
        })
    return jsonify({"success": False, "error": "تەنها خاوەنی سایت دەسەڵاتی داخستن و کردنەوەی هەیە!"}), 403

def get_all_db_files():
    db_files = glob.glob("*.db") + glob.glob("*.sqlite") + glob.glob("*.sqlite3")
    db_files += glob.glob("databases/*.db") + glob.glob("databases/*.sqlite")
    return sorted(list(set(db_files)))

@app.route('/api/search', methods=['POST', 'GET'])
def search_database():
    if SITE_LOCKED:
        return jsonify({"error": "سایتەکە لەلایەن ئەدمینەوە داخراوە!"}), 503

    if request.method == 'POST':
        payload = request.get_json(silent=True) or {}
        filters = payload.get("filters", {})
        general_q = payload.get("q", "").strip()
    else:
        general_q = request.args.get("q", "").strip()
        filters = {"q": general_q} if general_q else {}

    search_terms = [str(v).strip() for v in filters.values() if str(v).strip()]
    if not search_terms and not general_q:
        return jsonify({"error": "تکایە لانیکەم زانیارییەک بنووسە بۆ گەڕان!"}), 400

    db_files = get_all_db_files()
    if not db_files:
        return jsonify({"error": "هیچ فایلێکی داتابەیس (.db) لەسەر سێرڤەر نەدۆزرایەوە!"}), 404

    results = []
    for db_path in db_files:
        try:
            uri = f"file:{db_path}?mode=ro"
            conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = [r["name"] for r in cursor.fetchall()]

            for table in tables:
                cursor.execute(f'PRAGMA table_info("{table}")')
                columns = [col["name"] for col in cursor.fetchall()]
                if not columns:
                    continue

                where_clauses = []
                params = []
                for term in search_terms:
                    col_checks = [f'CAST("{col}" AS TEXT) LIKE ?' for col in columns]
                    where_clauses.append("(" + " OR ".join(col_checks) + ")")
                    params.extend([f"%{term}%"] * len(columns))

                where_sql = " AND ".join(where_clauses)
                query_sql = f'SELECT * FROM "{table}" WHERE {where_sql} LIMIT 25'

                cursor.execute(query_sql, params)
                rows = cursor.fetchall()
                for row in rows:
                    row_dict = {k: row[k] for k in row.keys() if row[k] is not None and str(row[k]).strip() != ""}
                    row_dict["_table"] = f"{os.path.basename(db_path)} -> {table}"
                    results.append(row_dict)
                    if len(results) >= 25:
                        break
                if len(results) >= 25:
                    break
            conn.close()
        except Exception:
            continue
        if len(results) >= 25:
            break

    return jsonify({
        "count": len(results),
        "records": results
    })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
