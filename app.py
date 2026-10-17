import os
import glob
import sqlite3
import requests
from datetime import datetime, timedelta
from flask import Flask, request, render_template_string, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "kurdistan01_super_secret_key_2026")

USERS_DB = "users.db"
ADMIN_USERNAME = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASS", "admin12345")

# لیستی هەموو داتابەیسەکان لە GitHub Releases
DATABASES = {
    "erbil": {"name": "هەولێر (Erbil)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/erbil.db"},
    "sulaymaniyah": {"name": "سلێمانی (Sulaymaniyah)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/sulaymaniyah.db"},
    "duhok": {"name": "دهۆک (Duhok)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/duhok.db"},
    "kirkuk": {"name": "کەرکوک (Kirkuk)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/kirkuk.db"},
    "baghdad": {"name": "بەغداد (Baghdad)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/baghdad.db"},
    "nineveh": {"name": "نەینەوا - مووسڵ (Nineveh)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/nineveh.db"},
    "diyala": {"name": "دیالە (Diyala)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/diyala.db"},
    "salahaldeen": {"name": "سەلاحەدین (Salahaldeen)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/salahaldeen.db"},
    "alanbar": {"name": "ئەنبار (Alanbar)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/alanbar.db"},
    "babylon": {"name": "بابل (Babylon)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/babylon.db"},
    "balad": {"name": "بەلەد (Balad)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/balad.db"},
    "basrah": {"name": "بەسرە (Basrah)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/basrah.db"},
    "dhiqar": {"name": "زیقار (Dhiqar)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/dhiqar.db"},
    "karbalaa": {"name": "کەربەلا (Karbalaa)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/karbalaa.db"},
    "mesan": {"name": "میسان (Mesan)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/mesan.db"},
    "muthana": {"name": "موسەننا (Muthana)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/muthana.db"},
    "najaf": {"name": "نەجەف (Najaf)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/najaf.db"},
    "qadisiya": {"name": "قادسیە (Qadisiya)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/qadisiya.db"},
    "wasit": {"name": "واست (Wasit)", "url": "https://github.com/tofayadnan214-stack/Kurdistan01/releases/download/v1/wasit.db"}
}

# ١. دروستکردنی داتابەیسی بەکارهێنەران و ئەدمین
def init_users_db():
    conn = sqlite3.connect(USERS_DB)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            status TEXT DEFAULT 'pending',
            expires_at TEXT
        )
    """)
    c.execute("SELECT * FROM users WHERE username = ?", (ADMIN_USERNAME,))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users (username, password, role, status, expires_at) VALUES (?, ?, 'admin', 'approved', '9999-12-31')",
            (ADMIN_USERNAME, ADMIN_PASSWORD)
        )
    conn.commit()
    conn.close()

init_users_db()

# ٢. فەنکشنی هێنانی داتابەیس لە گیتهەبەوە بەبێ پڕبوونی ڕامی ڕێندەر
def get_city_db_connection(city_key):
    city_info = DATABASES.get(city_key)
    if not city_info:
        return None
    
    url = city_info["url"]
    db_path = f"{city_key}.db"
    
    if not os.path.exists(db_path):
        # سڕینەوەی داتابەیسی شارەکانی پێشوو تا سێرڤەرەکە نەخنکێت (بێجگە لە users.db)
        for old_file in glob.glob("*.db"):
            if old_file != USERS_DB and old_file != db_path:
                try:
                    os.remove(old_file)
                except OSError:
                    pass
                    
        with requests.get(url, stream=True, timeout=300) as r:
            r.raise_for_status()
            with open(db_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=65536):
                    if chunk:
                        f.write(chunk)
                        
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# ٣. دیزاینی تەواوی ماڵپەڕەکە (HTML + CSS) لەناو خودی app.py
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ku" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سیستەمی زانیاری و گەڕان - Kurdistan01</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: system-ui, -apple-system, sans-serif; }
        body { background-color: #0b0f19; color: #e2e8f0; min-height: 100vh; padding: 15px; }
        .container { max-width: 950px; margin: 0 auto; }
        .card { background: #151c2c; border: 1px solid #263147; border-radius: 14px; padding: 20px; margin-bottom: 20px; box-shadow: 0 8px 25px rgba(0,0,0,0.5); }
        h1, h2, h3 { color: #38bdf8; margin-bottom: 15px; text-align: center; }
        .top-bar { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 20px; background: #151c2c; padding: 12px 18px; border-radius: 12px; border: 1px solid #263147; }
        .btn { display: inline-block; padding: 10px 16px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; text-decoration: none; font-size: 14px; transition: 0.2s; text-align: center; }
        .btn-primary { background: #0284c7; color: #fff; width: 100%; font-size: 16px; padding: 12px; }
        .btn-primary:hover { background: #0369a1; }
        .btn-danger { background: #dc2626; color: #fff; }
        .btn-success { background: #16a34a; color: #fff; padding: 6px 10px; font-size: 12px; }
        .btn-warning { background: #d97706; color: #fff; }
        input, select { width: 100%; padding: 12px; margin-bottom: 14px; border-radius: 8px; border: 1px solid #334155; background: #0f172a; color: #fff; font-size: 15px; }
        input:focus, select:focus { outline: none; border-color: #38bdf8; }
        .alert { padding: 12px; border-radius: 8px; margin-bottom: 15px; background: #7f1d1d; color: #fecaca; text-align: center; }
        .table-wrap { overflow-x: auto; margin-top: 15px; }
        table { width: 100%; border-collapse: collapse; background: #0f172a; border-radius: 8px; overflow: hidden; }
        th, td { padding: 10px 12px; border-bottom: 1px solid #1e293b; text-align: right; font-size: 14px; white-space: nowrap; }
        th { background: #1e293b; color: #38bdf8; }
        tr:hover { background: #172033; }
        .tabs { display: flex; gap: 10px; margin-bottom: 15px; }
        .tab-link { flex: 1; text-align: center; padding: 10px; background: #0f172a; color: #94a3b8; border-radius: 8px; text-decoration: none; font-weight: bold; }
        .tab-link.active { background: #0284c7; color: #fff; }
    </style>
</head>
<body>
<div class="container">
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            {% for msg in messages %}
                <div class="alert">{{ msg }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}

    {% if not session.get('username') %}
        <div class="card" style="max-width: 430px; margin: 40px auto;">
            <h2>🔒 سیستەمی تایبەت</h2>
            <div class="tabs">
                <a href="{{ url_for('login') }}" class="tab-link {% if page == 'login' %}active{% endif %}">چوونەژوورەوە</a>
                <a href="{{ url_for('register') }}" class="tab-link {% if page == 'register' %}active{% endif %}">تۆمارکردن</a>
            </div>

            {% if page == 'register' %}
                <form method="POST" action="{{ url_for('register') }}">
                    <input type="text" name="username" placeholder="ناوی بەکارهێنەر (Username)" required>
                    <input type="password" name="password" placeholder="وشەی تێپەڕ (Password)" required>
                    <button type="submit" class="btn btn-primary">ناردنی داواکاری تۆمارکردن</button>
                </form>
            {% else %}
                <form method="POST" action="{{ url_for('login') }}">
                    <input type="text" name="username" placeholder="ناوی بەکارهێنەر (Username)" required>
                    <input type="password" name="password" placeholder="وشەی تێپەڕ (Password)" required>
                    <button type="submit" class="btn btn-primary">چوونەژوورەوە</button>
                </form>
            {% endif %}
        </div>
    {% else %}
        <div class="top-bar">
            <div>👤 بەخێربێیت: <strong>{{ session.get('username') }}</strong></div>
            <div style="display:flex; gap:8px;">
                {% if session.get('role') == 'admin' %}
                    <a href="{{ url_for('admin_panel') }}" class="btn btn-warning">پانێڵی ئەدمین</a>
                {% endif %}
                <a href="{{ url_for('index') }}" class="btn btn-success" style="font-size:14px; padding:10px 14px;">گەڕان</a>
                <a href="{{ url_for('logout') }}" class="btn btn-danger">دەرچوون</a>
            </div>
        </div>

        {% if page == 'admin' and session.get('role') == 'admin' %}
            <div class="card">
                <h3>⚙️ بەڕێوەبردنی بەکارهێنەران (Admin Portal)</h3>
                <div class="table-wrap">
                    <table>
                        <thead>
                            <tr>
                                <th>ناو</th>
                                <th>دۆخ</th>
                                <th>بەسەرچوون</th>
                                <th>چالاکی و ماوە</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for u in users %}
                            <tr>
                                <td>{{ u['username'] }}</td>
                                <td>{{ u['status'] }}</td>
                                <td>{{ u['expires_at'] or '-' }}</td>
                                <td style="display:flex; gap:5px;">
                                    <a href="{{ url_for('approve_user', user_id=u['id'], days=30) }}" class="btn btn-success">٣٠ ڕۆژ</a>
                                    <a href="{{ url_for('approve_user', user_id=u['id'], days=60) }}" class="btn btn-success">٦٠ ڕۆژ</a>
                                    <a href="{{ url_for('approve_user', user_id=u['id'], days=365) }}" class="btn btn-success">١ ساڵ</a>
                                    <a href="{{ url_for('approve_user', user_id=u['id'], days=99999) }}" class="btn btn-success">هەمیشەیی</a>
                                    {% if u['role'] != 'admin' %}
                                    <a href="{{ url_for('delete_user', user_id=u['id']) }}" class="btn btn-danger" style="padding:6px 10px; font-size:12px;">سڕینەوە</a>
                                    {% endif %}
                                </td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
        {% else %}
            <div class="card">
                <h2>🔍 گەڕانی ناوەندی لە داتابەیسی شارەکان</h2>
                <form method="POST" action="{{ url_for('index') }}">
                    <label style="display:block; margin-bottom:6px; color:#94a3b8;">پارێزگا / فایل هەڵبژێرە:</label>
                    <select name="city" required>
                        {% for key, info in cities.items() %}
                            <option value="{{ key }}" {% if selected_city == key %}selected{% endif %}>{{ info['name'] }}</option>
                        {% endfor %}
                    </select>

                    <label style="display:block; margin-bottom:6px; color:#94a3b8;">زانیاری داواکراو بنووسە (ناو، ژمارە، یان ناونیشان):</label>
                    <input type="text" name="search_word" value="{{ search_query or '' }}" placeholder="لێرە بنووسە بۆ گەڕان..." required>

                    <button type="submit" class="btn btn-primary">دەستپێکردنی گەڕان</button>
                </form>
            </div>

            {% if search_performed %}
                <div class="card">
                    <h3>ئەنجامەکانی گەڕان ({{ results|length }})</h3>
                    {% if results %}
                        <div class="table-wrap">
                            <table>
                                <thead>
                                    <tr>
                                        {% for col in columns %}
                                            <th>{{ col }}</th>
                                        {% endfor %}
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for row in results %}
                                        <tr>
                                            {% for col in columns %}
                                                <td>{{ row[col] }}</td>
                                            {% endfor %}
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <p style="text-align:center; color:#94a3b8;">هیچ ئەنجامێک نەدۆزرایەوە.</p>
                    {% endif %}
                </div>
            {% endif %}
        {% endif %}
    {% endif %}
</div>
</body>
</html>
"""

# ٤. بەڕێوەبردنی پەڕەکان و چوونەژوورەوە
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        conn = sqlite3.connect(USERS_DB)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()
        
        if not user:
            flash("ناوی بەکارهێنەر یان وشەی تێپەڕ هەڵەیە!")
        elif user["status"] != "approved":
            flash("هەژمارەکەت هێشتا لەلایەن ئەدمینەوە پەسەند نەکراوە!")
        else:
            if user["expires_at"] and user["expires_at"] < datetime.now().strftime("%Y-%m-%d"):
                flash("ماوەی بەکارهێنانی هەژمارەکەت کۆتایی هاتووە!")
            else:
                session["username"] = user["username"]
                session["role"] = user["role"]
                return redirect(url_for("index"))
                
    return render_template_string(HTML_TEMPLATE, page="login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        conn = sqlite3.connect(USERS_DB)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, role, status) VALUES (?, ?, 'user', 'pending')", (username, password))
            conn.commit()
            flash("داواکارییەکەت نێردرا! چاوەڕێی پەسەندکردنی ئەدمین بکە.")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("ئەم ناوە پێشتر تۆمار کراوە!")
        finally:
            conn.close()
            
    return render_template_string(HTML_TEMPLATE, page="register")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin")
def admin_panel():
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    conn = sqlite3.connect(USERS_DB)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY id DESC")
    users = c.fetchall()
    conn.close()
    return render_template_string(HTML_TEMPLATE, page="admin", users=users)

@app.route("/admin/approve/<int:user_id>/<int:days>")
def approve_user(user_id, days):
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    exp_date = "9999-12-31" if days > 30000 else (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    conn = sqlite3.connect(USERS_DB)
    c = conn.cursor()
    c.execute("UPDATE users SET status = 'approved', expires_at = ? WHERE id = ?", (exp_date, user_id))
    conn.commit()
    conn.close()
    flash("بەکارهێنەر بە سەرکەوتوویی چالاک کرا!")
    return redirect(url_for("admin_panel"))

@app.route("/admin/delete/<int:user_id>")
def delete_user(user_id):
    if session.get("role") != "admin":
        return redirect(url_for("index"))
    conn = sqlite3.connect(USERS_DB)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ? AND role != 'admin'", (user_id,))
    conn.commit()
    conn.close()
    flash("بەکارهێنەر سڕایەوە.")
    return redirect(url_for("admin_panel"))

# ٥. پەڕەی سەرەکی و گەڕان لەناو داتابەیسە گەورەکان
@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("username"):
        return redirect(url_for("login"))
        
    results = []
    columns = []
    selected_city = "erbil"
    search_query = ""
    search_performed = False
    
    if request.method == "POST":
        selected_city = request.form.get("city", "erbil")
        search_query = request.form.get("search_word", "").strip()
        search_performed = True
        
        if selected_city and search_query:
            try:
                conn = get_city_db_connection(selected_city)
                if conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
                    tables = cursor.fetchall()
                    
                    for tbl in tables:
                        table_name = tbl[0]
                        cursor.execute(f"PRAGMA table_info(\"{table_name}\")")
                        cols = [col[1] for col in cursor.fetchall()]
                        if not cols:
                            continue
                            
                        where_clause = " OR ".join([f"CAST(\"{c}\" AS TEXT) LIKE ?" for c in cols])
                        params = [f"%{search_query}%" for _ in cols]
                        query = f"SELECT * FROM \"{table_name}\" WHERE {where_clause} LIMIT 100"
                        
                        cursor.execute(query, params)
                        rows = cursor.fetchall()
                        if rows:
                            columns = cols
                            results.extend([dict(row) for row in rows])
                            break
                    conn.close()
            except Exception as e:
                flash(f"کێشەیەک لە خوێندنەوەی داتابەیس ڕوویدا: {str(e)}")
                
    return render_template_string(
        HTML_TEMPLATE,
        page="search",
        cities=DATABASES,
        selected_city=selected_city,
        search_query=search_query,
        results=results,
        columns=columns,
        search_performed=search_performed
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
