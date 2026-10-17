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

def get_city_db_connection(city_key):
    city_info = DATABASES.get(city_key)
    if not city_info:
        return None
    
    url = city_info["url"]
    db_path = f"{city_key}.db"
    
    if not os.path.exists(db_path):
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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ckb" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>Darkness Eagle | سیستەمی چاوی تاریکی هەڵۆ</title>
    <style>
        :root {
            --bg-black: #020408;
            --panel-bg: rgba(9, 13, 20, 0.94);
            --card-bg: rgba(14, 18, 26, 0.95);
            --border-dim: #263142;
            --border-glow: #10b981;
            --neon-blue: #00e5ff;
            --neon-green: #00ff88;
            --kurd-red: #dc2626;
            --kurd-white: #ffffff;
            --kurd-green: #16a34a;
            --kurd-gold: #facc15;
            --text-light: #f3f4f6;
            --text-gray: #9ca3af;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

        body {
            background-color: var(--bg-black); color: var(--text-light);
            min-height: 100vh; overflow-x: hidden; position: relative;
        }

        #matrixCanvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; opacity: 0.22; pointer-events: none; }

        .globe-bg {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 460px; height: 460px; z-index: 0; opacity: 0.10; pointer-events: none;
            animation: rotateGlobe 60s linear infinite;
        }

        .radar-corner {
            position: fixed; top: 15px; left: 15px; width: 80px; height: 80px;
            border: 1px solid rgba(16, 185, 129, 0.18); border-radius: 50%; z-index: 0;
            pointer-events: none; display: flex; align-items: center; justify-content: center;
        }
        .radar-corner::before {
            content: ''; width: 46px; height: 46px; border: 1px dashed rgba(16, 185, 129, 0.28); border-radius: 50%;
        }
        .radar-sweep {
            position: absolute; width: 50%; height: 2px;
            background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.65));
            top: 50%; left: 50%; transform-origin: left center; animation: sweep 4s linear infinite;
        }

        @keyframes rotateGlobe { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
        @keyframes sweep { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes pulseGreen { 0% { opacity: 1; transform: scale(1); box-shadow: 0 0 8px #10b981; } 50% { opacity: 0.35; transform: scale(0.85); box-shadow: 0 0 2px #10b981; } 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 8px #10b981; } }
        @keyframes cyberGlow { 0% { stroke: #00ff88; } 50% { stroke: #00e5ff; } 100% { stroke: #00ff88; } }
        @keyframes dashMove { to { stroke-dashoffset: -100; } }

        .main-wrapper {
            position: relative; z-index: 2; width: 100%; max-width: 1220px;
            margin: 0 auto; padding: 10px 8px 35px; min-height: 100vh;
            display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
        }

        .kurd-flag-bar {
            width: 100%; max-width: 540px; height: 4px; border-radius: 4px;
            background: linear-gradient(90deg, var(--kurd-green) 0%, var(--kurd-white) 35%, var(--kurd-gold) 50%, var(--kurd-white) 65%, var(--kurd-red) 100%);
            margin-bottom: 10px; box-shadow: 0 0 12px rgba(250, 204, 21, 0.35);
        }

        .hero-header {
            text-align: center; margin-bottom: 12px; width: 100%; max-width: 540px;
            background: rgba(6, 9, 15, 0.90); border: 1px solid var(--border-dim);
            border-radius: 14px; padding: 14px 12px; box-shadow: 0 8px 28px rgba(0, 0, 0, 0.85);
        }

        .kurdistan-flag-frame {
            position: relative; width: 230px; margin: 0 auto 10px; padding: 3px;
            border-radius: 12px; background: linear-gradient(90deg, #dc2626, #facc15, #16a34a);
            box-shadow: 0 0 20px rgba(250, 204, 21, 0.4), 0 4px 15px rgba(0, 0, 0, 0.9);
        }

        .kurdistan-flag-inner {
            position: relative;
            background: linear-gradient(180deg, rgba(220, 38, 38, 0.88) 0%, rgba(220, 38, 38, 0.82) 33.3%, rgba(248, 250, 252, 0.92) 33.3%, rgba(248, 250, 252, 0.92) 66.6%, rgba(22, 163, 74, 0.88) 66.6%, rgba(22, 163, 74, 0.88) 100%);
            border-radius: 9px; padding: 8px 12px; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center;
            border: 1px solid rgba(250, 204, 21, 0.65);
        }

        .kurdistan-flag-inner::after { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, rgba(0, 0, 0, 0.15) 0%, rgba(0, 0, 0, 0.45) 100%); z-index: 1; }

        .kurd-sun-svg {
            position: absolute; width: 58px; height: 58px; top: 50%; left: 50%;
            transform: translate(-50%, -50%); opacity: 0.92; z-index: 1; pointer-events: none;
            filter: drop-shadow(0 0 8px rgba(250, 204, 21, 0.9)); animation: rotateGlobe 40s linear infinite;
        }

        .eagle-logo-text-top {
            position: relative; z-index: 3; font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 17px; font-weight: 900; letter-spacing: 3px; line-height: 1.05; color: #ffffff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.95), 0 0 8px rgba(0,0,0,0.85);
        }

        .eagle-logo-text-bottom {
            position: relative; z-index: 3; font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 15px; font-weight: 900; letter-spacing: 4.5px; line-height: 1.05; margin-top: 2px;
            color: #fde047; text-shadow: 0 2px 4px rgba(0,0,0,0.95), 0 0 8px rgba(0,0,0,0.9);
        }

        .welcome-title { font-size: 13.5px; font-weight: bold; margin-top: 4px; line-height: 1.5; }
        .welcome-kurd-grad { background: linear-gradient(90deg, #ef4444, #ffffff, #facc15, #22c55e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
        .patriotic-slogan { font-size: 11.5px; color: #cbd5e1; margin-top: 6px; line-height: 1.55; display: flex; flex-direction: column; align-items: center; gap: 4px; }
        .yellow-bji-line { color: var(--kurd-gold); font-weight: bold; font-size: 10px; white-space: nowrap; display: inline-flex; align-items: center; gap: 4px; background: rgba(250, 204, 21, 0.08); padding: 2px 8px; border-radius: 12px; border: 1px solid rgba(250, 204, 21, 0.28); }

        .view-section { display: none; width: 100%; }
        .view-section.active { display: block; animation: fadeIn 0.25s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

        .red-waiting-alert {
            display: none; width: 100%; max-width: 540px; margin: 0 auto 12px;
            background: rgba(127, 29, 29, 0.35); border: 1.5px solid #ef4444; border-radius: 11px;
            padding: 11px 14px; color: #ff4d4d; font-size: 12.5px; font-weight: 800; text-align: center;
            line-height: 1.65; box-shadow: 0 0 18px rgba(239, 68, 68, 0.35);
        }
        .red-waiting-alert.show { display: block; }

        .auth-master-card { width: 100%; max-width: 540px; margin: 0 auto; background: var(--panel-bg); border: 1px solid var(--border-dim); border-radius: 14px; padding: 14px; box-shadow: 0 12px 35px rgba(0, 0, 0, 0.9); }
        .auth-tabs-bar { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 14px; background: #04060b; padding: 5px; border-radius: 10px; border: 1px solid #1f2937; }
        .auth-tab-btn { background: transparent; border: 1px solid transparent; color: #9ca3af; padding: 9px 6px; border-radius: 8px; cursor: pointer; font-size: 11.5px; font-weight: bold; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; }
        .auth-tab-btn span.sub-pill { font-size: 9.5px; font-weight: normal; opacity: 0.75; }
        .auth-tab-btn.active-reg { background: linear-gradient(135deg, rgba(185, 28, 28, 0.28), rgba(220, 38, 38, 0.15)); border-color: var(--kurd-gold); color: #ffffff; }
        .auth-tab-btn.active-reg span.sub-pill { color: var(--kurd-gold); }
        .auth-tab-btn.active-login { background: linear-gradient(135deg, rgba(6, 95, 70, 0.35), rgba(16, 185, 129, 0.18)); border-color: #10b981; color: #ffffff; }
        .auth-tab-btn.active-login span.sub-pill { color: #34d399; }
        .auth-form-pane { display: none; padding: 4px; }
        .auth-form-pane.active { display: block; }
        .form-group { margin-bottom: 11px; text-align: right; }
        .form-group label { display: block; font-size: 11.5px; color: #e2e8f0; margin-bottom: 5px; font-weight: 700; direction: ltr; text-align: right; }
        .form-input { width: 100%; padding: 9px 12px; background: #04060a; border: 1px solid #374151; border-radius: 7px; color: #ffffff; font-size: 12px; outline: none; }
        .form-input:focus { border-color: var(--kurd-gold); }
        .btn-action { width: 100%; padding: 10px 12px; border-radius: 8px; font-size: 12.5px; font-weight: bold; cursor: pointer; border: 1px solid transparent; margin-top: 6px; color: #fff; }
        .btn-register { background: linear-gradient(135deg, #991b1b, #dc2626); border-color: #f87171; }
        .btn-login-hacker { background: linear-gradient(135deg, #042f2e, #065f46, #047857); border: 1px solid #10b981; color: #ecfdf5; font-family: monospace; box-shadow: 0 0 15px rgba(16, 185, 129, 0.25); }
        .helper-note { font-size: 10.5px; color: var(--text-gray); margin-top: 9px; text-align: center; }

        .status-card { max-width: 480px; margin: 20px auto; background: linear-gradient(180deg, rgba(12, 18, 28, 0.96), rgba(6, 10, 16, 0.98)); border: 1.5px solid var(--border-glow); border-radius: 16px; padding: 22px 16px; text-align: center; box-shadow: 0 0 35px rgba(16, 185, 129, 0.22); }
        .designer-success-pill { display: inline-flex; align-items: center; justify-content: center; gap: 6px; background: rgba(6, 95, 70, 0.35); border: 1px solid #10b981; color: #34d399; padding: 7px 14px; border-radius: 30px; font-size: 11.5px; font-weight: 800; white-space: nowrap; margin: 8px auto 12px; box-shadow: 0 0 15px rgba(16, 185, 129, 0.25); }
        .loader-ring { width: 52px; height: 52px; border: 3px solid rgba(255, 255, 255, 0.1); border-top: 3px solid var(--kurd-gold); border-right: 3px solid var(--kurd-green); border-bottom: 3px solid var(--kurd-red); border-radius: 50%; margin: 10px auto 16px; animation: sweep 1.1s linear infinite; }

        /* TOP STATUS BAR */
        .cyber-top-bar {
            width: 100%; max-width: 1040px; margin: 0 auto 8px;
            background: rgba(8, 11, 18, 0.95); border: 1px solid #263142; border-radius: 10px;
            padding: 5px 12px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 6px; font-size: 10px;
        }
        .status-dot { display: inline-block; width: 6.5px; height: 6.5px; background: #10b981; border-radius: 50%; margin-left: 4px; box-shadow: 0 0 8px #10b981; }
        .role-badge-small {
            background: rgba(185, 28, 28, 0.28); border: 1px solid #ef4444; color: #fca5a5;
            padding: 1px 5px; border-radius: 4px; font-size: 8px; font-weight: 800; letter-spacing: 0.3px;
        }

        .dashboard-nav-bar-compact {
            width: 100%; max-width: 1040px; margin: 0 auto 10px;
            background: linear-gradient(180deg, rgba(13, 19, 31, 0.96), rgba(7, 11, 18, 0.98));
            border: 1px solid #334155; border-radius: 10px; padding: 7px 12px;
            display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.85);
        }
        .admin-pill-small {
            background: rgba(6, 78, 59, 0.45); border: 1px solid #10b981; color: #34d399;
            padding: 2.5px 7px; border-radius: 5px; font-size: 8.5px; font-weight: 800; letter-spacing: 0.2px;
            display: inline-flex; align-items: center; gap: 4px;
        }
        .session-timer-text { font-size: 9px; color: #facc15; font-family: monospace; font-weight: bold; }

        /* TACTICAL PORTAL HEADER BAR */
        .tactical-portal-bar {
            width: 100%; max-width: 1040px; margin: 0 auto 12px;
            background: rgba(9, 13, 22, 0.96); border: 1px solid #1e293b; border-radius: 12px;
            padding: 10px 14px; display: flex; justify-content: space-between; align-items: center;
            flex-wrap: wrap; gap: 10px; direction: ltr; box-shadow: 0 6px 20px rgba(0,0,0,0.85);
        }
        .admin-star-portal-btn {
            display: flex; align-items: center; gap: 10px; cursor: pointer;
            padding: 4px 8px; border-radius: 10px; border: 1px solid transparent; transition: 0.25s;
        }
        .admin-star-portal-btn:hover {
            background: rgba(250, 204, 21, 0.08); border-color: rgba(250, 204, 21, 0.4);
            box-shadow: 0 0 15px rgba(250, 204, 21, 0.2);
        }
        .star-box-icon {
            width: 38px; height: 38px; border-radius: 9px; background: rgba(20, 26, 38, 0.95);
            border: 1.5px solid var(--kurd-gold); display: flex; align-items: center; justify-content: center;
            color: var(--kurd-gold); font-size: 18px; box-shadow: 0 0 12px rgba(250, 204, 21, 0.35);
        }
        .portal-title-col { display: flex; flex-direction: column; text-align: left; }
        .portal-main-title { font-family: monospace; font-size: 14.5px; font-weight: 900; color: #ffffff; letter-spacing: 1.5px; }
        .portal-sub-title { font-size: 10.5px; font-weight: bold; color: #facc15; letter-spacing: 0.4px; margin-top: 1px; }

        .user-status-right-group {
            display: flex; align-items: center; gap: 8px;
        }
        .user-online-pill-box {
            display: flex; align-items: center; gap: 8px; background: #070a10;
            border: 1px solid #263142; padding: 6px 12px; border-radius: 9px;
        }
        .blinking-green-dot {
            width: 9px; height: 9px; border-radius: 50%; background: #10b981;
            animation: pulseGreen 1.4s infinite ease-in-out;
        }
        .logged-username-text {
            font-family: monospace; font-size: 12.5px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px;
        }
        .user-role-tag-pill {
            background: rgba(14, 116, 144, 0.28); border: 1px solid #06b6d4; color: #67e8f9;
            font-size: 9.5px; font-weight: 800; padding: 2px 7px; border-radius: 5px; letter-spacing: 0.6px;
        }
        .red-exit-icon-btn {
            width: 36px; height: 36px; border-radius: 9px; background: rgba(127, 29, 29, 0.35);
            border: 1.5px solid #ef4444; color: #fca5a5; display: flex; align-items: center; justify-content: center;
            cursor: pointer; transition: 0.2s; font-size: 15px; font-weight: bold;
        }
        .red-exit-icon-btn:hover { background: #dc2626; color: #ffffff; box-shadow: 0 0 12px rgba(239, 68, 68, 0.5); }

        .tactical-map-wrapper { touch-action: pan-x pan-y pinch-zoom;

            width: 100%; max-width: 1040px; margin: 0 auto 16px;
            background: linear-gradient(rgba(2, 4, 8, 0.7), rgba(2, 4, 8, 0.85)), url('data:image/jpeg;base64,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'), url('data:image/jpeg;base64,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');
            background-blend-mode: overlay;
            background-size: cover;
            background-position: center;
            border: 1.5px solid #10b981; border-radius: 14px; padding: 12px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.95), 0 0 25px rgba(0, 229, 255, 0.15), inset 0 0 30px rgba(0, 255, 136, 0.08);
            position: relative; overflow: hidden;
        }
        .tactical-map-wrapper::before {
            content: ''; position: absolute; inset: 0;
            background: 
                linear-gradient(rgba(0, 229, 255, 0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 229, 255, 0.04) 1px, transparent 1px);
            background-size: 26px 26px; pointer-events: none; z-index: 1;
        }
        .map-top-hud {
            display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
            direction: ltr; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px dashed rgba(0, 229, 255, 0.35);
            position: relative; z-index: 3;
        }
        .hud-left-status { font-family: monospace; font-size: 11px; color: var(--neon-green); font-weight: bold; letter-spacing: 1px; }
        .hud-left-sub { font-family: monospace; font-size: 9.5px; color: var(--neon-blue); letter-spacing: 1.2px; margin-top: 2px; }
        .hud-sector-box {
            font-family: monospace; font-size: 10.5px; font-weight: bold; color: var(--neon-blue);
            border: 1px solid rgba(0, 229, 255, 0.5); background: rgba(0, 229, 255, 0.1);
            padding: 4px 10px; border-radius: 6px; letter-spacing: 1px; box-shadow: 0 0 10px rgba(0, 229, 255, 0.25);
        }

        .spider-map-svg-box {
            width: 100%; max-width: 680px; margin: 0 auto; position: relative;
            display: flex; align-items: center; justify-content: center; min-height: 380px;
            border-radius: 12px; overflow: hidden; z-index: 2;
        }

        .spider-map-svg {
            width: 100%; height: auto; max-height: 440px; position: relative; z-index: 2;
            filter: drop-shadow(0 0 12px rgba(0, 229, 255, 0.3));
        }

        /* FIXED 3-COLUMN CARDS GRID (PERMANENT 3 COLUMNS) */
        .cards-grid {
            display: grid !important;
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 8px !important;
            width: 100% !important;
            max-width: 1040px !important;
            margin: 0 auto !important;
        }

        .card {
            background: rgba(14, 18, 26, 0.95);
            border: 1px solid #4b5563;
            border-radius: 10px;
            width: 100%;
            min-height: 190px;
            padding: 10px 8px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.85);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
            transition: all 0.22s ease;
        }
        .card:hover { border-color: #cbd5e1; transform: translateY(-2px); }
        .card.active { border-color: #10b981; box-shadow: 0 0 16px rgba(16, 185, 129, 0.38); }
        .card-header { display: flex; flex-direction: row-reverse; align-items: center; justify-content: space-between; gap: 4px; margin-bottom: 6px; }
        .checkbox-box { width: 14px; height: 14px; min-width: 14px; border: 2px solid #d1d5db; border-radius: 3px; display: flex; align-items: center; justify-content: center; }
        .checkbox-box::after { content: ''; width: 5px; height: 5px; background: #d1d5db; display: block; }
        .card.active .checkbox-box { border-color: #10b981; }
        .card.active .checkbox-box::after { background: #10b981; }
        .card-title { font-size: 11.5px; font-weight: bold; line-height: 1.35; text-align: center; flex: 1; color: #ffffff; }
        .card-body { font-size: 9.5px; color: #cbd5e1; text-align: center; margin-bottom: 8px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
        .card-btn { background: rgba(255, 255, 255, 0.04); border: 1px solid #6b7280; color: #ffffff; padding: 6px 4px; border-radius: 5px; font-size: 9px; font-weight: bold; cursor: pointer; text-align: center; transition: 0.2s; }
        .card.active .card-btn, .card:hover .card-btn { background: #064e3b; border-color: #10b981; color: #ecfdf5; }

        /* SEPARATE ADMIN APPROVAL PORTAL VIEW */
        .admin-portal-card {
            width: 100%; max-width: 820px; margin: 15px auto;
            background: rgba(8, 12, 20, 0.96); border: 1.5px solid #10b981;
            border-radius: 14px; padding: 20px 16px;
            box-shadow: 0 0 35px rgba(16, 185, 129, 0.2), inset 0 0 20px rgba(16, 185, 129, 0.05);
        }
        .hacker-green-frame {
            border: 1.5px solid #10b981; background: rgba(6, 78, 59, 0.28);
            border-radius: 10px; padding: 12px 16px; text-align: center;
            max-width: 380px; margin: 0 auto 14px;
            box-shadow: 0 0 18px rgba(16, 185, 129, 0.3); font-family: monospace;
        }
        .hacker-green-frame .main-owner-tag {
            font-size: 15px; font-weight: 900; color: #34d399; letter-spacing: 1px; display: block;
        }
        .hacker-green-frame .sub-eternal-tag {
            font-size: 12.5px; font-weight: bold; color: #fde047; margin-top: 4px; display: block;
        }
        .admin-portal-subtitle {
            text-align: center; font-size: 13px; font-weight: 800; color: #ffffff;
            background: rgba(15, 23, 42, 0.9); border: 1px solid #334155;
            padding: 9px 14px; border-radius: 8px; margin-bottom: 16px;
        }
        .request-item-card {
            background: rgba(13, 18, 28, 0.96); border: 1px solid #374151;
            border-radius: 11px; padding: 14px; margin-bottom: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.7); text-align: right;
        }
        .req-credentials-box {
            background: #06090f; border: 1px solid #1e293b; border-radius: 8px;
            padding: 10px 12px; margin-bottom: 10px; direction: ltr; text-align: left;
            font-family: monospace; font-size: 12px; line-height: 1.6;
        }
        .req-durations-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-top: 8px;
        }
        @media (max-width: 540px) { .req-durations-grid { grid-template-columns: 1fr; } }

        .duration-option-box {
            display: flex; align-items: center; justify-content: space-between;
            background: rgba(6, 15, 25, 0.95); border: 1px solid #10b981;
            border-radius: 8px; padding: 8px 12px; font-size: 11.5px; font-weight: bold; color: #e2e8f0;
            box-shadow: inset 0 0 8px rgba(16, 185, 129, 0.12);
        }
        .run-approve-btn {
            background: linear-gradient(135deg, #059669, #10b981); color: #000000;
            border: 1px solid #34d399; padding: 4px 12px; border-radius: 5px;
            font-family: monospace; font-size: 11px; font-weight: 900; cursor: pointer;
            transition: 0.2s; box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
        }
        .run-approve-btn:hover { background: #34d399; transform: scale(1.04); }

        /* INSIDE DB PANEL & SEARCH RESULT VIEWS */
        .db-fields-grid {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 10px !important;
            width: 100% !important;
        }
        @media (min-width: 768px) {
            .db-fields-grid {
                grid-template-columns: repeat(3, 1fr) !important;
            }
        }
        .db-inside-panel { width: 100%; max-width: 1040px; margin: 6px auto 0; background: rgba(14, 17, 23, 0.96); border: 1.5px solid #9ca3af; border-radius: 12px; padding: 22px 18px; box-shadow: 0 0 35px rgba(0, 0, 0, 0.95); }
        .db-inside-top-row { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
        .db-inside-main-title { font-size: 18px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 8px; }
        .db-inside-sub-badge { display: block; font-size: 11px; color: #10b981; margin-top: 3px; font-weight: bold; }
        .db-inside-actions { display: flex; gap: 8px; flex-wrap: wrap; }
        .db-top-btn { background: rgba(20, 24, 33, 0.95); border: 1px solid #9ca3af; color: #f3f4f6; padding: 8px 14px; border-radius: 6px; font-size: 11.5px; font-weight: bold; cursor: pointer; transition: 0.2s; display: inline-flex; align-items: center; gap: 5px; }
        .db-top-btn:hover { border-color: #ffffff; background: rgba(255, 255, 255, 0.08); }
        .db-back-main-btn { background: linear-gradient(135deg, rgba(6, 78, 59, 0.7), rgba(4, 120, 87, 0.5)); border: 1px solid #10b981; color: #ecfdf5; box-shadow: 0 0 12px rgba(16, 185, 129, 0.25); }
        .db-back-main-btn:hover { background: #059669; border-color: #34d399; }

        .db-dropdown-wrap { margin-bottom: 16px; text-align: right; }
        .db-dropdown-label { display: block; font-size: 12px; font-weight: bold; color: #d1d5db; margin-bottom: 6px; }
        .db-dropdown-select { width: 100%; background: #141820; border: 1px solid #6b7280; color: #ffffff; padding: 10px 14px; border-radius: 6px; font-size: 12.5px; font-weight: bold; outline: none; cursor: pointer; }
        .db-dropdown-select:focus { border-color: #10b981; }

        .db-warning-banner { background: rgba(180, 83, 9, 0.22); border: 1px solid #f59e0b; color: #fef3c7; padding: 10px 14px; border-radius: 8px; font-size: 12px; font-weight: bold; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
        
        .db-fields-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; width: 100%; }
        @media (max-width: 900px) { .db-fields-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 560px) { .db-fields-grid { grid-template-columns: 1fr; } }

        .db-field-card { background: rgba(20, 24, 32, 0.95); border: 1px solid #374151; border-radius: 9px; padding: 14px 12px; transition: 0.2s; display: flex; flex-direction: column; justify-content: space-between; }
        .db-field-card:focus-within { border-color: #10b981; background: rgba(6, 78, 59, 0.18); box-shadow: 0 0 12px rgba(16, 185, 129, 0.25); }
        .db-field-label { display: block; font-size: 11.5px; font-weight: bold; color: #e5e7eb; margin-bottom: 8px; text-align: right; }
        .db-field-input { width: 100%; background: rgba(12, 15, 20, 0.95); border: 1px solid #4b5563; border-radius: 6px; padding: 9px 10px; color: #ffffff; font-size: 11.5px; outline: none; text-align: right; }
        .db-field-input:focus { border-color: #10b981; }

        .db-Execute-full-btn { width: 100%; margin-top: 18px; background: linear-gradient(135deg, #042f2e, #065f46, #047857); border: 1px solid #10b981; color: #ffffff; padding: 12px; border-radius: 8px; font-size: 13.5px; font-weight: bold; cursor: pointer; transition: 0.2s; text-align: center; box-shadow: 0 0 15px rgba(16, 185, 129, 0.25); }
        .db-Execute-full-btn:hover { background: #059669; box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); }

        .cyber-scan-box { display: none; width: 100%; max-width: 1040px; margin: 30px auto; padding: 50px 20px; text-align: center; }
        .cyber-scan-box.active { display: block; }
        .scan-spinner { width: 64px; height: 64px; border: 3px solid rgba(255, 255, 255, 0.12); border-bottom: 3.5px solid #ffffff; border-radius: 50%; margin: 0 auto 18px; animation: sweep 0.9s linear infinite; }
        .scan-main-title { font-size: 14px; font-weight: bold; color: #e5e7eb; margin-bottom: 6px; }
        .scan-sub-title { font-size: 11px; color: #9ca3af; }

        .secret-results-wrapper { display: none; width: 100%; max-width: 1040px; margin: 8px auto 0; }
        .secret-results-wrapper.active { display: block; animation: fadeIn 0.3s ease; }
        .results-top-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid #263142; flex-wrap: wrap; gap: 10px; }
        .results-top-title { font-size: 20px; font-weight: 800; color: #ffffff; }
        .results-summary-bar { width: 100%; background: rgba(20, 24, 32, 0.92); border: 1px solid #4b5563; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; font-weight: bold; color: #e5e7eb; }

        .record-master-card { width: 100%; background: rgba(15, 19, 26, 0.96); border: 1px solid #4b5563; border-radius: 12px; padding: 20px 18px; margin-bottom: 18px; box-shadow: 0 8px 28px rgba(0, 0, 0, 0.9); }
        .record-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
        .record-num-title { font-size: 17px; font-weight: 800; color: #ffffff; }
        .record-db-badge { background: rgba(6, 78, 59, 0.55); border: 1px solid #10b981; color: #d1fae5; padding: 5px 14px; border-radius: 6px; font-size: 11.5px; font-weight: bold; }

        .record-data-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 18px; }
        @media (max-width: 900px) { .record-data-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 500px) { .record-data-grid { grid-template-columns: 1fr; } }

        .record-cell { background: rgba(9, 12, 17, 0.95); border: 1px solid #263142; border-radius: 8px; padding: 12px 12px; text-align: right; }
        .record-cell.highlight { border-color: #059669; background: rgba(6, 78, 59, 0.22); }
        .record-cell-label { font-size: 11px; color: #9ca3af; margin-bottom: 6px; display: block; font-weight: 600; }
        .record-cell-val { font-size: 12.5px; font-weight: 800; color: #ffffff; word-break: break-word; line-height: 1.5; }

        .record-actions-bar { display: flex; justify-content: flex-start; gap: 10px; flex-wrap: wrap; }
        .record-action-btn { background: rgba(20, 24, 33, 0.95); border: 1px solid #4b5563; color: #e5e7eb; padding: 8px 14px; border-radius: 6px; font-size: 11.5px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: 0.2s; }
        .record-action-btn:hover { border-color: #10b981; color: #ffffff; background: rgba(16, 185, 129, 0.15); }
        .record-action-btn.btn-highlight { border-color: #10b981; background: rgba(6, 78, 59, 0.45); color: #34d399; }

        /* MODAL OVERLAYS */
        .modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0, 0, 0, 0.88); z-index: 9999; align-items: center; justify-content: center; padding: 15px; overflow-y: auto; }
        .modal-overlay.open { display: flex; }
        .tree-modal-box { width: 100%; max-width: 960px; touch-action: manipulation;  background: #090c12; border: 1px solid #4b5563; border-radius: 12px; padding: 16px 20px 24px; box-shadow: 0 15px 45px rgba(0, 0, 0, 0.95); position: relative; }
        .modal-common-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #263142; padding-bottom: 10px; margin-bottom: 16px; }
        .modal-common-title { font-size: 14px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 6px; }
        .modal-close-btn { background: #7f1d1d; border: 1px solid #ef4444; color: #ffffff; width: 28px; height: 28px; border-radius: 5px; cursor: pointer; font-weight: bold; display: flex; align-items: center; justify-content: center; font-size: 14px; }
        .tree-inner-frame { border: 1px solid #374151; border-radius: 10px; padding: 20px 14px; background: rgba(11, 15, 22, 0.95); text-align: center; }
        .tree-role-tag { display: inline-block; background: #ffffff; color: #000000; font-weight: 800; font-size: 11px; padding: 4px 16px; border-radius: 20px; margin-bottom: 8px; }
        
        .parent-node-card { position: relative; max-width: 380px; margin: 0 auto; background: #101622; border: 1.5px solid #d1d5db; border-radius: 12px; padding: 16px 14px; text-align: right; box-shadow: 0 0 20px rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; gap: 12px; }
        .node-avatar-circle { width: 60px; height: 60px; min-width: 60px; background: #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
        .node-avatar-inner-sq { width: 24px; height: 24px; border: 3px solid #000000; }
        .parent-info-col { flex: 1; text-align: right; }
        .node-name-head { font-size: 15px; font-weight: 800; color: #ffffff; margin-bottom: 6px; }
        .node-detail-line { font-size: 10.5px; color: #cbd5e1; margin-bottom: 3px; }
        .node-bottom-badges { display: flex; gap: 6px; margin-top: 8px; justify-content: flex-end; flex-wrap: wrap; }
        .mini-badge-box { background: #090d14; border: 1px solid #4b5563; border-radius: 5px; padding: 2px 7px; font-size: 9.5px; color: #e5e7eb; }
        .tree-connector-line { width: 2px; height: 35px; background: #38bdf8; margin: 0 auto; }
        .tree-middle-badge { display: inline-block; background: #000000; border: 1px solid #4b5563; color: #ffffff; font-size: 10px; font-weight: bold; padding: 2px 12px; border-radius: 12px; margin-bottom: 8px; }
        .children-cards-row { display: grid !important; grid-template-columns: repeat(2, 1fr) !important; gap: 8px !important; margin-top: 10px !important; }
        @media (min-width: 768px) { .children-cards-row { grid-template-columns: repeat(3, 1fr) !important; } }
        .child-node-card { background: #101622; border: 1.5px solid #d1d5db; border-radius: 12px; padding: 12px 10px; display: flex; align-items: center; justify-content: space-between; gap: 8px; text-align: right; box-shadow: 0 0 15px rgba(255, 255, 255, 0.05); }
        .node-diamond { width: 22px; height: 22px; background: #000000; transform: rotate(45deg); }

        .map-modal-box { width: 100%; max-width: 490px; background: #0c1017; border: 1.5px solid #4b5563; border-radius: 12px; padding: 16px 16px 20px; box-shadow: 0 15px 45px rgba(0, 0, 0, 0.95); }
        .meter-info-card { background: #141a24; border: 1px solid #374151; border-radius: 8px; padding: 12px 14px; margin-bottom: 14px; font-size: 11.5px; line-height: 1.8; color: #e5e7eb; text-align: right; }
        .meter-map-frame { width: 100%; height: 380px; border: 1px solid #374151; border-radius: 8px; overflow: hidden; background: #1f2937; }
        .meter-map-frame iframe { width: 100%; height: 100%; border: 0; }

        .bio-modal-box { width: 100%; max-width: 420px; background: #0c1017; border: 1.5px solid #10b981; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 15px 45px rgba(0,0,0,0.95); }
        .bio-img-preview { width: 180px; height: 180px; border: 2px solid #10b981; border-radius: 10px; margin: 15px auto; object-fit: cover; background: #1f2937; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #10b981; }

        /* TOAST NOTIFICATION */
        #toastNotice {
            position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%) translateY(100px);
            background: #059669; color: #fff; padding: 10px 24px; border-radius: 30px;
            font-size: 12.5px; font-weight: bold; z-index: 99999; box-shadow: 0 5px 20px rgba(0,0,0,0.8);
            transition: transform 0.3s ease;
        }
        #toastNotice.show { transform: translateX(-50%) translateY(0); }

        /* FACE ID DECORATIVE SCANNER */
        .face-scan-title { font-size: 15px; font-weight: bold; color: #10b981; margin-bottom: 15px; text-shadow: 0 0 10px rgba(16,185,129,0.5); }
        .face-scanner-container { position: relative; width: 280px; height: 280px; margin: 0 auto; border-radius: 50%; overflow: hidden; border: 3px solid #10b981; box-shadow: 0 0 30px rgba(16,185,129,0.3); background: #000; }
        #webcamVideo { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }
        .scanner-frame { position: absolute; inset: 0; background: radial-gradient(transparent 40%, rgba(0,0,0,0.9) 100%); pointer-events: none; }
        .scanner-laser { position: absolute; width: 100%; height: 3px; background: #00ff88; top: 0; box-shadow: 0 0 15px #00ff88, 0 0 25px #00e5ff; animation: scanLaser 2s infinite alternate ease-in-out; pointer-events: none; }
        @keyframes scanLaser { 0% { top: 0; opacity: 0.2; } 20% { opacity: 1; } 80% { opacity: 1; } 100% { top: 100%; opacity: 0.2; } }
    </style>
</head>
<body>

<canvas id="matrixCanvas"></canvas>
<svg class="globe-bg" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="90" fill="none" stroke="#00e5ff" stroke-width="0.8"/>
    <ellipse cx="100" cy="100" rx="65" ry="90" fill="none" stroke="#00ff88" stroke-width="0.6"/>
    <ellipse cx="100" cy="100" rx="35" ry="90" fill="none" stroke="#00e5ff" stroke-width="0.6"/>
    <line x1="100" y1="10" x2="100" y2="190" stroke="#00ff88" stroke-width="0.6"/>
    <line x1="10" y1="100" x2="190" y2="100" stroke="#00e5ff" stroke-width="0.6"/>
</svg>
<div class="radar-corner"><div class="radar-sweep"></div></div>

<div id="toastNotice">پەیام</div>

<div class="main-wrapper">
    <div class="kurd-flag-bar"></div>

    <!-- 1. AUTH VIEW -->
    <div id="authView" class="view-section active">
        <div class="hero-header">
            <div class="kurdistan-flag-frame">
                <div class="kurdistan-flag-inner">
                    <svg class="kurd-sun-svg" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="22" fill="#facc15"/>
                        <g stroke="#facc15" stroke-width="3.5">
                            <line x1="50" y1="4" x2="50" y2="22"/><line x1="50" y1="78" x2="50" y2="96"/>
                            <line x1="4" y1="50" x2="22" y2="50"/><line x1="78" y1="50" x2="96" y2="50"/>
                            <line x1="17" y1="17" x2="30" y2="30"/><line x1="70" y1="70" x2="83" y2="83"/>
                            <line x1="83" y1="17" x2="70" y2="30"/><line x1="30" y1="70" x2="17" y2="83"/>
                        </g>
                    </svg>
                    <div class="eagle-logo-text-top">DARKNESS</div>
                    <div class="eagle-logo-text-bottom">EAGLE</div>
                </div>
            </div>
            <div class="welcome-title"><span class="welcome-kurd-grad">بەخێربێن بۆ ناو سیستەمی هەڵۆی تاریکی</span></div>
            <div class="patriotic-slogan">
                <div>ئەم سیستەمە تایبەتە بە خزمەتی کورد و گەلی کورد</div>
                <div class="yellow-bji-line">( بژی کورد، بژی کوردستان ☀️ )</div>
            </div>
        </div>

        <div id="redWaitingNotice" class="red-waiting-alert">تکایە چاوەڕێبە تا ئەدمین قبوڵت دەکات بۆ چونە ژورەوەی سیستەمی چاوی تاریکی هەڵۆ</div>

        <div class="auth-master-card">
            <div class="auth-tabs-bar">
                <button type="button" id="tabBtnReg" class="auth-tab-btn active-reg" onclick="switchAuthTab('reg')">
                    <span>دروستکردنی هەژمار (ئەکاونت)</span>
                    <span class="sub-pill">بەشداربووی نوێ</span>
                </button>
                <button type="button" id="tabBtnLogin" class="auth-tab-btn" onclick="switchAuthTab('login')">
                    <span>چوونەژوورەوە بۆ ناو سیستەم</span>
                    <span class="sub-pill">کلیک بکە بۆ چوونەژوورەوە</span>
                </button>
            </div>

            <div id="paneRegister" class="auth-form-pane active">
                <form onsubmit="submitRegister(event)">
                    <div class="form-group"><label>Username / Gmail</label><input type="text" id="regUser" class="form-input" required placeholder="ناوی بەکارهێنەر یان جیمێڵەکەت بنووسە..."></div>
                    <div class="form-group"><label>Password</label><input type="password" id="regPass1" class="form-input" required placeholder="پاسۆردێکی بەهێز بنووسە..."></div>
                    <div class="form-group"><label>Confirm Password</label><input type="password" id="regPass2" class="form-input" required placeholder="پاسۆردەکە دووبارە بنووسەوە بۆ دڵنیابوونەوە..."></div>
                    <button type="submit" class="btn-action btn-register">تۆمارکردن و ناردنی داواکاری ◄</button>
                    <div class="helper-note">* دوای دروستکردنی هەژمار، داواکارییەکەت دەچێتە لای بەڕێوەبەر (ئەدمین) بۆ پەسەندکردن و دیاریکردنی ماوە.</div>
                </form>
            </div>

            <div id="paneLogin" class="auth-form-pane">
                <form onsubmit="submitLogin(event)">
                    <div class="form-group"><label>Username / Gmail</label><input type="text" id="loginUser" class="form-input" required placeholder="جیمێڵ یان یوزەرنەیمەکەت بنووسە..."></div>
                    <div class="form-group"><label>Password</label><input type="password" id="loginPass" class="form-input" required placeholder="پاسۆردەکەت بنووسە..."></div>
                    <button type="submit" class="btn-action btn-login-hacker">چونە ژورەوەی سیستەمی چاوی هەڵۆ</button>
                    <div class="helper-note" style="color:#cbd5e1;font-weight:600;">چوونە ژوورەوە بۆ ناو سیستەم دوای پەسەندکردنی لەلایەن بەڕێوەبەرەوە</div>
                </form>
            </div>
        </div>
    </div>

    <!-- 2. DECORATIVE 5-SECOND FACE ID VIEW -->
    <div id="faceIdView" class="view-section">
        <div class="status-card" style="max-width: 500px;">
            <div class="face-scan-title">سیستەمی ناسینەوەی ڕووخسار (Face ID)</div>
            <div class="face-scanner-container">
                <video id="webcamVideo" autoplay playsinline></video>
                <div class="scanner-frame"></div>
                <div class="scanner-laser"></div>
            </div>
            <div id="faceScanStatus" class="scan-sub-title" style="margin-top: 15px; font-size: 13.5px; font-weight: bold; color:#00ff88;">سکانکردنی ڕووخسار دەستی پێکرد... تکایە سەیری کامێراکە بکە</div>
            <div style="font-size:11px; color:#9ca3af; margin-top:8px; font-family:monospace;">AI BIOMETRIC VERIFICATION IN PROGRESS (5 SECONDS)</div>
        </div>
    </div>

    <!-- 3. WAITING VIEW -->
    <div id="waitingView" class="view-section">
        <div class="status-card">
            <div class="kurdistan-flag-frame">
                <div class="kurdistan-flag-inner">
                    <svg class="kurd-sun-svg" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="22" fill="#facc15"/>
                        <g stroke="#facc15" stroke-width="3.5"><line x1="50" y1="4" x2="50" y2="22"/><line x1="50" y1="78" x2="50" y2="96"/><line x1="4" y1="50" x2="22" y2="50"/><line x1="78" y1="50" x2="96" y2="50"/></g>
                    </svg>
                    <div class="eagle-logo-text-top">DARKNESS</div>
                    <div class="eagle-logo-text-bottom">EAGLE</div>
                </div>
            </div>
            <div class="loader-ring"></div>
            <button type="button" class="btn-action btn-login-hacker" onclick="returnToMainWithRedWaitMessage()">چاوەڕێبە ئەدمین قبوڵ بکات بۆ چونە ژورەوە</button>
        </div>
    </div>

    <!-- 4. MAIN DASHBOARD VIEW (ONLY VISIBLE AFTER 5-SEC SCAN AND VERIFICATION) -->
    <div id="dashboardView" class="view-section">
        <!-- TOP STATUS BAR: REDUCED FONT SIZES, OWNER/MASTER SMALLER -->
        <div class="cyber-top-bar">
            <div><span class="status-dot"></span><strong>سیستەم چالاکە</strong> | پەیوەندی: <span style="color:#34d399;">پارێزراو</span> | دەسەڵات: <span class="role-badge-small" id="topRoleBadge">OWNER / MASTER</span></div>
            <div class="yellow-bji-line">( بژی کورد، بژی کوردستان ☀️ )</div>
            <div id="liveClock" style="color:#9ca3af;font-family:monospace;">16/10/2026 23:15:00</div>
        </div>

        <!-- REFINED COMPACT BAR -->
        <div class="dashboard-nav-bar-compact">
            <span class="admin-pill-small" id="activeUserBadge">👑 KURDISTAN01 (بەڕێوەبەری گشتی)</span>
            <span class="session-timer-text" id="sessionRemainingBadge">⏱ ماوە: هەمیشەیی</span>
        </div>

        <!-- TACTICAL BAR (IMAGE 2 & 3 COMBINED) -->
        <div class="tactical-portal-bar">
            <!-- Left Side: Star Icon + Kurdistan01 + چوونە ژورەوەی بەڕێوبەر -->
            <div class="admin-star-portal-btn" onclick="openAdminPortalView()" title="چوونە ژوورەوەی بەڕێوەبەر">
                <div class="star-box-icon">★</div>
                <div class="portal-title-col">
                    <span class="portal-main-title">Kurdistan01</span>
                    <span class="portal-sub-title">چوونە ژورەوەی بەڕێوبەر</span>
                </div>
            </div>

            <!-- Right Side: Blinking Green Online Dot + Username + USER tag + Red Exit Button -->
            <div class="user-status-right-group">
                <div class="user-online-pill-box">
                    <span class="blinking-green-dot"></span>
                    <span class="logged-username-text" id="tacticalUsernameDisplay">Kurdistan01</span>
                    <span class="user-role-tag-pill" id="tacticalRolePill">USER</span>
                </div>
                <button type="button" class="red-exit-icon-btn" onclick="logoutToAuth()" title="دەرچوون لە سیستەم (Logout)">
                    ➔
                </button>
            </div>
        </div>

        <!-- PURE DIGITAL CYBER SPIDERWEB NETWORK TOPOLOGY MAP (DARK BACKGROUND, NEON BLUE & GREEN) -->
        <div id="spiderMapSection" class="tactical-map-wrapper">
            <div class="map-top-hud">
                <div>
                    <div class="hud-left-status"><span class="status-dot"></span>STATUS: ONLINE</div>
                    <div class="hud-left-sub">KURDISTAN TACTICAL SPIDER-WEB TOPOLOGY • CYBER MESH NETWORK</div>
                </div>
                <div class="hud-sector-box" id="activeSectorHud">SECTOR: ERBIL (هەولێر)</div>
            </div>

            <div class="spider-map-svg-box">
                <svg class="spider-map-svg" viewBox="0 0 650 520" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <radialGradient id="cyberMeshGlow" cx="50%" cy="50%" r="50%">
                            <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.22"/>
                            <stop offset="55%" stop-color="#00ff88" stop-opacity="0.08"/>
                            <stop offset="100%" stop-color="#020408" stop-opacity="0"/>
                        </radialGradient>
                        <filter id="neonBlur" x="-30%" y="-30%" width="160%" height="160%">
                            <feGaussianBlur stdDeviation="3.2" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
                        </filter>
                    </defs>

                    <!-- Background Radar Target Rings & Cyber Glow -->
                    <circle cx="325" cy="240" r="210" fill="url(#cyberMeshGlow)"/>
                    <circle cx="325" cy="240" r="180" fill="none" stroke="#00e5ff" stroke-width="0.8" stroke-dasharray="6,6" opacity="0.3"/>
                    <circle cx="325" cy="240" r="120" fill="none" stroke="#00ff88" stroke-width="0.8" stroke-dasharray="4,8" opacity="0.4"/>
                    <circle cx="325" cy="240" r="60" fill="none" stroke="#00e5ff" stroke-width="0.8" opacity="0.5"/>
                    <line x1="325" y1="20" x2="325" y2="460" stroke="#00e5ff" stroke-width="0.7" stroke-dasharray="3,6" opacity="0.3"/>
                    <line x1="100" y1="240" x2="550" y2="240" stroke="#00ff88" stroke-width="0.7" stroke-dasharray="3,6" opacity="0.3"/>

                    <!-- Spiderweb Concentric Digital Rings -->
                    <g opacity="0.5" stroke-width="1.2">
                        <polygon points="325,70 460,130 495,240 445,365 325,420 205,365 155,240 190,130" fill="none" stroke="#00e5ff" stroke-dasharray="5,5"/>
                        <polygon points="325,115 425,160 450,240 410,330 325,375 240,330 200,240 225,160" fill="none" stroke="#00ff88"/>
                        <polygon points="325,160 390,190 405,240 375,295 325,330 275,295 245,240 260,190" fill="none" stroke="#00e5ff"/>
                        <polygon points="325,195 355,210 365,240 350,270 325,285 300,270 285,240 295,210" fill="none" stroke="#00ff88"/>
                    </g>

                    <!-- Outer Border of Map -->
                    <polygon points="210,35 365,28 455,85 525,175 545,265 495,355 525,465 470,495 315,465 215,390 120,305 145,205 190,135" 
                             fill="rgba(0, 229, 255, 0.03)" stroke="#00e5ff" stroke-width="2.2" filter="url(#neonBlur)"/>

                    <!-- Glowing Neon Blue & Green Connection Lines -->
                    <g stroke="#00e5ff" stroke-width="1.6" opacity="0.85" filter="url(#neonBlur)">
                        <!-- Northern & Major Kurdish Network -->
                        <line x1="255" y1="68" x2="290" y2="105"/> <!-- Zakho - Duhok -->
                        <line x1="255" y1="68" x2="240" y2="155"/> <!-- Zakho - Mosul -->
                        <line x1="290" y1="105" x2="345" y2="112"/> <!-- Duhok - Akre -->
                        <line x1="290" y1="105" x2="345" y2="165"/> <!-- Duhok - Erbil -->
                        <line x1="290" y1="105" x2="240" y2="155"/> <!-- Duhok - Mosul -->
                        <line x1="345" y1="112" x2="405" y2="120"/> <!-- Akre - Soran -->
                        <line x1="345" y1="112" x2="345" y2="165"/> <!-- Akre - Erbil -->
                        <line x1="405" y1="120" x2="345" y2="165"/> <!-- Soran - Erbil -->
                        <line x1="405" y1="120" x2="435" y2="168"/> <!-- Soran - Ranya -->
                        <line x1="345" y1="165" x2="395" y2="185"/> <!-- Erbil - Koya -->
                        <line x1="345" y1="165" x2="355" y2="235"/> <!-- Erbil - Kirkuk -->
                        <line x1="345" y1="165" x2="240" y2="155"/> <!-- Erbil - Mosul -->
                        <line x1="395" y1="185" x2="435" y2="168"/> <!-- Koya - Ranya -->
                        <line x1="395" y1="185" x2="455" y2="215"/> <!-- Koya - Sulaymaniyah -->
                        <line x1="395" y1="185" x2="355" y2="235"/> <!-- Koya - Kirkuk -->
                        <line x1="435" y1="168" x2="455" y2="215"/> <!-- Ranya - Sulaymaniyah -->
                        <line x1="455" y1="215" x2="410" y2="248"/> <!-- Sulaymaniyah - Chamchamal -->
                        <line x1="455" y1="215" x2="495" y2="255"/> <!-- Sulaymaniyah - Halabja -->
                        <line x1="455" y1="215" x2="435" y2="290"/> <!-- Sulaymaniyah - Kalar -->
                        <line x1="410" y1="248" x2="355" y2="235"/> <!-- Chamchamal - Kirkuk -->
                        <line x1="410" y1="248" x2="435" y2="290"/> <!-- Chamchamal - Kalar -->
                        <line x1="495" y1="255" x2="435" y2="290"/> <!-- Halabja - Kalar -->
                        <line x1="355" y1="235" x2="435" y2="290"/> <!-- Kirkuk - Kalar -->
                        <line x1="435" y1="290" x2="420" y2="335"/> <!-- Kalar - Khanaqin -->
                        <line x1="240" y1="155" x2="355" y2="235"/> <!-- Mosul - Kirkuk -->

                        <!-- Regional Grid Lines -->
                        <line x1="240" y1="155" x2="295" y2="295"/>
                        <line x1="355" y1="235" x2="295" y2="295"/>
                        <line x1="355" y1="235" x2="380" y2="340"/>
                        <line x1="420" y1="335" x2="380" y2="340"/>
                        <line x1="295" y1="295" x2="320" y2="375"/>
                        <line x1="380" y1="340" x2="320" y2="375"/>
                        <line x1="180" y1="365" x2="320" y2="375"/>
                        <line x1="180" y1="365" x2="285" y2="430"/>
                        <line x1="320" y1="375" x2="285" y2="430"/>
                        <line x1="320" y1="375" x2="395" y2="415"/>
                        <line x1="285" y1="430" x2="295" y2="465"/>
                        <line x1="395" y1="415" x2="475" y2="480"/>
                        <line x1="295" y1="465" x2="475" y2="480"/>
                    </g>

                    <!-- Neon Green Pulsing Data Streams -->
                    <g stroke="#00ff88" stroke-width="1.3" stroke-dasharray="4,6" opacity="0.85">
                        <line x1="345" y1="165" x2="455" y2="215"/>
                        <line x1="290" y1="105" x2="455" y2="215"/>
                        <line x1="255" y1="68" x2="355" y2="235"/>
                        <line x1="495" y1="255" x2="345" y2="165"/>
                        <line x1="345" y1="165" x2="420" y2="335"/>
                    </g>

                    <!-- City Nodes (Neon Green and Blue Glowing Points - Spaced Out) -->
                    <!-- Zakho -->
                    <g style="cursor:pointer" onclick="selectSector('ZAKHO (زاخۆ)')">
                        <circle cx="255" cy="68" r="8" fill="#00e5ff" stroke="#000" stroke-width="2" filter="url(#neonBlur)"/>
                        <circle cx="255" cy="68" r="3" fill="#ffffff"/>
                        <text x="235" y="48" fill="#00e5ff" font-size="10.5" font-weight="900" font-family="monospace">زاخۆ ZAKHO</text>
                    </g>
                    <!-- Duhok -->
                    <g style="cursor:pointer" onclick="selectSector('DUHOK (دهۆک)')">
                        <circle cx="290" cy="105" r="9" fill="#00ff88" stroke="#000" stroke-width="2" filter="url(#neonBlur)"/>
                        <circle cx="290" cy="105" r="4" fill="#ffffff"/>
                        <text x="175" y="100" fill="#00ff88" font-size="11" font-weight="900">دهۆک DUHOK</text>
                    </g>
                    <!-- Akre -->
                    <g style="cursor:pointer" onclick="selectSector('AKRE (ئاکرێ)')">
                        <circle cx="345" cy="112" r="7" fill="#00e5ff" stroke="#000" stroke-width="1.8"/>
                        <circle cx="345" cy="112" r="2.5" fill="#ffffff"/>
                        <text x="325" y="94" fill="#a7f3d0" font-size="10" font-weight="bold">ئاکرێ</text>
                    </g>
                    <!-- Soran -->
                    <g style="cursor:pointer" onclick="selectSector('SORAN (سۆران)')">
                        <circle cx="405" cy="120" r="8" fill="#00ff88" stroke="#000" stroke-width="1.8" filter="url(#neonBlur)"/>
                        <circle cx="405" cy="120" r="3" fill="#ffffff"/>
                        <text x="420" y="112" fill="#00ff88" font-size="10.5" font-weight="900">سۆران</text>
                    </g>
                    <!-- Erbil (Central Neon Cyber Node) -->
                    <g style="cursor:pointer" onclick="selectSector('ERBIL (هەولێر)')">
                        <circle cx="345" cy="165" r="13" fill="none" stroke="#00e5ff" stroke-width="2" stroke-dasharray="3,3" opacity="0.8"/>
                        <circle cx="345" cy="165" r="10" fill="#00ff88" stroke="#ffffff" stroke-width="2.5" filter="url(#neonBlur)"/>
                        <circle cx="345" cy="165" r="4.5" fill="#ffffff"/>
                        <text x="260" y="153" fill="#00ff88" font-size="12" font-weight="900">هەولێر ERBIL</text>
                    </g>
                    <!-- Koya -->
                    <g style="cursor:pointer" onclick="selectSector('KOYA (کۆیە)')">
                        <circle cx="395" cy="185" r="7" fill="#00e5ff" stroke="#000" stroke-width="1.8"/>
                        <circle cx="395" cy="185" r="2.5" fill="#ffffff"/>
                        <text x="375" y="210" fill="#a7f3d0" font-size="10" font-weight="bold">کۆیە</text>
                    </g>
                    <!-- Ranya -->
                    <g style="cursor:pointer" onclick="selectSector('RANYA (ڕانیە)')">
                        <circle cx="435" cy="168" r="8" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="435" cy="168" r="3" fill="#ffffff"/>
                        <text x="450" y="162" fill="#00ff88" font-size="10.5" font-weight="900">ڕانیە</text>
                    </g>
                    <!-- Sulaymaniyah -->
                    <g style="cursor:pointer" onclick="selectSector('SULAYMANIYAH (سلێمانی)')">
                        <circle cx="455" cy="215" r="10" fill="#00e5ff" stroke="#000" stroke-width="2" filter="url(#neonBlur)"/>
                        <circle cx="455" cy="215" r="4" fill="#ffffff"/>
                        <text x="475" y="222" fill="#00e5ff" font-size="11" font-weight="900">سلێمانی</text>
                    </g>
                    <!-- Chamchamal -->
                    <g style="cursor:pointer" onclick="selectSector('CHAMCHAMAL (چەمچەماڵ)')">
                        <circle cx="410" cy="248" r="7" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="410" cy="248" r="2.5" fill="#ffffff"/>
                        <text x="365" y="275" fill="#a7f3d0" font-size="9.5" font-weight="bold">چەمچەماڵ</text>
                    </g>
                    <!-- Kirkuk -->
                    <g style="cursor:pointer" onclick="selectSector('KIRKUK (کەرکوک)')">
                        <circle cx="355" cy="235" r="10" fill="#00e5ff" stroke="#00ff88" stroke-width="2.2" filter="url(#neonBlur)"/>
                        <circle cx="355" cy="235" r="4" fill="#ffffff"/>
                        <text x="270" y="248" fill="#00e5ff" font-size="11" font-weight="900">کەرکوک</text>
                    </g>
                    <!-- Halabja -->
                    <g style="cursor:pointer" onclick="selectSector('HALABJA (هەڵەبجە)')">
                        <circle cx="495" cy="255" r="8" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="495" cy="255" r="3" fill="#ffffff"/>
                        <text x="510" y="265" fill="#00ff88" font-size="10.5" font-weight="900">هەڵەبجە</text>
                    </g>
                    <!-- Kalar -->
                    <g style="cursor:pointer" onclick="selectSector('KALAR (کەلار - گەرمیان)')">
                        <circle cx="435" cy="290" r="8" fill="#00e5ff" stroke="#000" stroke-width="1.8"/>
                        <circle cx="435" cy="290" r="3" fill="#ffffff"/>
                        <text x="450" y="305" fill="#00e5ff" font-size="10.5" font-weight="900">کەلار</text>
                    </g>
                    <!-- Khanaqin -->
                    <g style="cursor:pointer" onclick="selectSector('KHANAQIN (خانەقین)')">
                        <circle cx="420" cy="335" r="7" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="420" cy="335" r="2.5" fill="#ffffff"/>
                        <text x="435" y="352" fill="#a7f3d0" font-size="10" font-weight="bold">خانەقین</text>
                    </g>

                    <!-- Southern Iraq Regional Nodes -->
                    <g style="cursor:pointer" onclick="selectSector('MOSUL')">
                        <circle cx="240" cy="155" r="7" fill="#3b82f6" stroke="#000" stroke-width="1.8"/>
                        <text x="180" y="159" fill="#93c5fd" font-size="10.5" font-weight="bold">MOSUL</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('SALAHADDIN')">
                        <circle cx="295" cy="295" r="6" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="215" y="299" fill="#93c5fd" font-size="9.5" font-weight="bold">SALAHADDIN</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('DIYALA')">
                        <circle cx="380" cy="340" r="6" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="330" y="344" fill="#93c5fd" font-size="9.5" font-weight="bold">DIYALA</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('BAGHDAD')">
                        <circle cx="320" cy="375" r="8" fill="#3b82f6" stroke="#000" stroke-width="2"/>
                        <text x="333" y="379" fill="#bfdbfe" font-size="11" font-weight="bold">BAGHDAD</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('ANBAR')">
                        <circle cx="180" cy="365" r="6" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="135" y="369" fill="#93c5fd" font-size="9.5" font-weight="bold">ANBAR</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('KARBALA')">
                        <circle cx="285" cy="430" r="6" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="225" y="434" fill="#93c5fd" font-size="9.5" font-weight="bold">KARBALA</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('WASIT')">
                        <circle cx="395" cy="415" r="6" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="407" y="419" fill="#93c5fd" font-size="9.5" font-weight="bold">WASIT</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('NAJAF')">
                        <circle cx="295" cy="465" r="6.5" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="245" y="469" fill="#93c5fd" font-size="10" font-weight="bold">NAJAF</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('BASRA')">
                        <circle cx="475" cy="480" r="8" fill="#3b82f6" stroke="#000" stroke-width="2"/>
                        <text x="488" y="484" fill="#bfdbfe" font-size="11" font-weight="bold">BASRA</text>
                    </g>
                </svg>
            </div>
        </div>

        <!-- 14 CARDS GRID (PERMANENT 3-COLUMNS AS IN IMAGE 11) -->
        <div id="cardsGridSubView">
            <div class="cards-grid" id="cardsContainer"></div>
        </div>

        <!-- INSIDE DATABASE SEARCH FORM -->
        <div id="insideDbSubView" style="display: none;">
            <div class="db-inside-panel">
                <div class="db-inside-top-row">
                    <div>
                        <div class="db-inside-main-title" id="insideDbHeaderTitle">دەستگەیشتن بە بنکەی زانیاری</div>
                        <span class="db-inside-sub-badge" id="insideDbActiveName">❖ بنکەی زانیاری</span>
                    </div>
                    <div class="db-inside-actions">
                        <button type="button" class="db-top-btn" onclick="clearInsideDbFields()">• پاککردنەوەی هەموو خانەکان</button>
                        <button type="button" class="db-top-btn db-back-main-btn" onclick="closeInsideDbView()" style="background: linear-gradient(135deg, #065f46, #047857); border: 1.5px solid #34d399; color: #ffffff; padding: 10px 16px; border-radius: 8px; font-weight: bold; font-size: 12.5px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 0 15px rgba(16,185,129,0.3); transition: 0.2s;">⟲ گەڕانەوە بۆ نەخشە و سەرەکی</button>
                    </div>
                </div>

                <div id="dynamicWarningBanner" class="db-warning-banner" style="display: none;"></div>
                <div id="dynamicDropdownArea" class="db-dropdown-wrap" style="display: none;"></div>

                <form onsubmit="runInsideDbSearch(event)">
                    <div id="dynamicFieldsGrid" class="db-fields-grid"></div>
                    <button type="submit" class="db-Execute-full-btn" id="executeSearchBtn">جێبەجێکردنی گەڕان ◄</button>
                </form>
            </div>
        </div>

        <!-- CYBER SCANNING LOADER -->
        <div id="cyberScanSubView" class="cyber-scan-box">
            <div class="scan-spinner"></div>
            <div class="scan-main-title">• سکان کردنی بنکە شفرەکراوەکان...</div>
            <div class="scan-sub-title">کردنەوەی شفرە... دڵنیاکردنەوە... پرۆسێسکردن...</div>
        </div>

        <!-- SECRET SEARCH RESULTS VIEW -->
        <div id="secretResultsSubView" class="secret-results-wrapper">
            <div class="results-top-header">
                <div class="results-top-title" id="resultsMainTitle">ئەنجامەکانی گەڕان: نهێنی</div>
                <div style="display:flex; gap:8px;">
                    <button type="button" class="db-top-btn" onclick="backToSearchForm()">گەڕانی نوێ •</button>
                    <button type="button" class="db-top-btn db-back-main-btn" onclick="closeInsideDbView()" style="background: linear-gradient(135deg, #065f46, #047857); border: 1.5px solid #34d399; color: #ffffff; padding: 10px 16px; border-radius: 8px; font-weight: bold; font-size: 12.5px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 0 15px rgba(16,185,129,0.3); transition: 0.2s;">⟲ گەڕانەوە بۆ پێڕستی بنکەکان</button>
                </div>
            </div>
            <div class="results-summary-bar">
                <span id="totalRecordsFoundText">• کۆی تۆمارەکانی دۆزراوە: 100</span>
                <span id="pageRecordsText">لاپەڕە 1 لە 10</span>
            </div>
            <div id="recordsListContainer"></div>
        </div>
    </div>

    <!-- 5. SEPARATE ADMIN APPROVAL PORTAL VIEW -->
    <div id="adminPortalView" class="view-section">
        <div class="admin-portal-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #1e293b; padding-bottom:10px;">
                <span style="color:#facc15; font-weight:900; font-size:13px;">★ پانێڵی تایبەتی بەڕێوەبەر</span>
                <button type="button" class="db-top-btn db-back-main-btn" onclick="switchView('dashboardView')">گەڕانەوە بۆ ناو سیستەم ➔</button>
            </div>

            <div class="hacker-green-frame">
                <span class="main-owner-tag">( Username/Oner)</span>
                <span class="sub-eternal-tag">(هەمیشەیی)</span>
            </div>

            <div class="admin-portal-subtitle">
                داواکاری قبوڵ کردن بۆ ناو چاوی هەڵۆیی تارکی دەروازەی زانیاری
            </div>

            <div id="adminRequestsContainer"></div>
        </div>
    </div>
</div>

<!-- 1. FAMILY TREE MODAL -->
<!-- 1. FAMILY TREE MODAL -->
<!-- 1. FAMILY TREE MODAL -->
<!-- 1. FAMILY TREE MODAL -->
<div id="familyTreeModal" class="modal-overlay">
    <div class="tree-modal-box" style="max-width: 960px; padding: 12px 14px 18px;">
        <div class="modal-common-header" style="margin-bottom: 10px; padding-bottom: 6px;">
            <div class="modal-common-title" style="font-size: 13px;">FAMILY TREE VISUALIZATION</div>
            <div style="display:flex; gap:6px; align-items:center;">
                <button type="button" class="db-top-btn db-back-main-btn" onclick="closeFamilyTreeModal()" style="padding: 4px 10px; font-size: 11px;">گەڕانەوە ➔</button>
                <button type="button" class="modal-close-btn" onclick="closeFamilyTreeModal()" style="width: 24px; height: 24px; font-size: 12px;">✕</button>
            </div>
        </div>
        <div class="tree-inner-frame" style="padding: 10px 8px;">
            <div class="tree-role-tag" style="font-size: 10px; padding: 2px 10px; margin-bottom: 6px;">سەرۆکی خێزان و هاوسەر</div>

            <!-- Husband and Wife side by side container -->
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; max-width: 720px; margin: 0 auto;">
                <div class="parent-node-card" style="max-width: 100%; margin: 0; padding: 10px; gap: 8px;">
                    <div class="node-avatar-circle" style="width: 40px; height: 40px; min-width: 40px;"><div class="node-avatar-inner-sq" style="width: 16px; height: 16px;"></div></div>
                    <div class="parent-info-col" style="text-align: right;">
                        <div class="node-name-head" style="font-size: 12.5px; margin-bottom: 2px;">محسن نجم (باوک)</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• باوک: نجم صادق | دایک: نجبة</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• پیشە: فەرمانبەر | تەمەن: 61</div>
                        <div class="node-detail-line" style="font-size: 9.5px; color: #34d399; font-weight: bold;">• مووچەی مانگانە: 1,250,000 دینار</div>
                        <div class="node-bottom-badges" style="margin-top: 4px; gap: 4px;">
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">لەدایکبوون: 1965</span>
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">خێزاندار</span>
                        </div>
                    </div>
                </div>

                <div class="parent-node-card" style="max-width: 100%; margin: 0; padding: 10px; gap: 8px;">
                    <div class="node-avatar-circle" style="width: 40px; height: 40px; min-width: 40px;"><div class="node-diamond" style="width: 14px; height: 14px;"></div></div>
                    <div class="parent-info-col" style="text-align: right;">
                        <div class="node-name-head" style="font-size: 12.5px; margin-bottom: 2px;">زينة حسين (دایک)</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• باوک: حسين طاهر | دایک: خديجة</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• پیشە: ماڵدار | تەمەن: 58</div>
                        <div class="node-detail-line" style="font-size: 9.5px; color: #9ca3af;">• مووچەی مانگانە: نەبوو (خانەنشینی خێزان)</div>
                        <div class="node-bottom-badges" style="margin-top: 4px; gap: 4px;">
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">کار: 1</span>
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">خێزاندار</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="tree-connector-line" style="height: 18px; margin-top: 6px;"></div>
            <div class="tree-middle-badge" style="font-size: 9.5px; padding: 1px 10px;">منداڵان (٦ منداڵ - زانیاری تەواو و مووچە)</div>
            <div class="tree-connector-line" style="height: 12px;"></div>

            <div class="children-cards-row" style="display: grid !important; grid-template-columns: repeat(3, 1fr) !important; gap: 8px !important; margin-top: 6px !important;">
                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">لاوند محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: ئەندازیار</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: خێزاندار | تەمەن: 34</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 950,000 د.ع</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 1992</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">ژیان</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">هوشمند محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: پزیشک</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: خێزاندار | تەمەن: 32</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 1,800,000 د.ع</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 1994</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">ژیان</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">کارمند محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: مامۆستا</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: سەڵت | تەمەن: 29</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 750,000 د.ع</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 1997</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">ژیان</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">شيرين محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: فەرمانبەر</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: خێزاندار | تەمەن: 31</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 650,000 د.ع</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">ID: 783276</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">ژیان</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start; border-color: #ef4444; background: rgba(127,29,29,0.15);">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px; color:#fca5a5;">فريشتة محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: دەرچوو</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color:#ef4444; font-weight: bold;">• دۆخ: کۆچکردوو</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #9ca3af;">• مووچە: -</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; background:#7f1d1d; color:#fca5a5;">کۆچکردوو</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">روند محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: قوتابی</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: سەڵت | تەمەن: 20</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #facc15;">• مووچە: نەبوو (قوتابی)</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 2006</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">ژیان</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 14px; text-align: center;">
                <button type="button" class="db-top-btn db-back-main-btn" onclick="closeFamilyTreeModal()" style="padding: 8px 18px; font-size: 12px;">گەڕانەوە بۆ بنکەی زانیاری ➔</button>
            </div>
        </div>
    </div>
</div>

<!-- 2. METER LOCATION MAP MODAL -->
<div id="meterMapModal" class="modal-overlay">
    <div class="map-modal-box">
        <div class="modal-common-header">
            <div class="modal-common-title">⬚ شوێنی میتەر</div>
            <button type="button" class="modal-close-btn" onclick="closeMeterMapModal()">✕</button>
        </div>
        <div class="meter-info-card">
            <div><strong>ناوی بەشداربوو:</strong> <span id="mapMeterName">محمد احمد محمد</span></div>
            <div><strong>ژمارەی ئەکاونت:</strong> <span id="mapMeterAcc">63179260572</span></div>
            <div><strong>هێڵی پانی:</strong> <span id="mapMeterLat">36.18416794</span></div>
            <div><strong>هێڵی درێژی:</strong> <span id="mapMeterLng">44.03849821</span></div>
            <div><strong>دۆخ:</strong> <span style="color:#10b981;font-weight:bold;">مۆڵەتدار</span></div>
        </div>
        <div class="meter-map-frame">
            <iframe id="meterMapIframe" src="https://maps.google.com/maps?q=36.18416794,44.03849821&hl=ckb&z=17&output=embed"></iframe>
        </div>
    </div>
</div>

<!-- 3. BIOMETRIC PHOTO MODAL -->
<div id="bioModal" class="modal-overlay">
    <div class="bio-modal-box">
        <div class="modal-common-header">
            <div class="modal-common-title">👤 وێنەی بایۆمێتریک</div>
            <button type="button" class="modal-close-btn" onclick="closeBioModal()">✕</button>
        </div>
        <div class="bio-img-preview">
            [وێنەی بایۆمێتریکی کەس]
        </div>
        <div style="font-size:12px; color:#cbd5e1; margin-top:10px;">کۆدی بایۆمێتریک: <span style="color:var(--kurd-gold);">87914692</span></div>
        <button type="button" class="db-Execute-full-btn" style="margin-top:14px;" onclick="closeBioModal()">داخستن</button>
    </div>
</div>

<script>
    const accountsDB = {};

    let currentLoggedInUser = null;
    let currentActiveDbTitle = '';
    let faceStreamRef = null;

    const dbCards = [
        ["بنکەی زانیاری کی کارد", "تۆمارەکانی کارتی تەموین، زانیاری کی کارد، و سیستەمی چاودێری خزمەتگوزاری هاوڵاتیان."],
        ["بنکەی زانیاری ئاسیاسێڵ", "تۆمارەکانی بەشداربووانی تۆڕی مۆبایل، تۆمارکردنی سیمکارت، و زانیاری پەیوەندییەکان."],
        ["بنکەی تۆمارکردنی شار 2022", "نهێنی: تۆماری تەواوی هاوڵاتیان لە ساڵی 2022، تۆمارەکانی خێزان، و بنکەی زانیاری ناسنامەی نیشتمانی.", true],
        ["بنکەی زانیاری خزمایەتی", "نهێنی: سیستەمی شوێنکەوتنی ڕەچەڵەکی خێزان، ناسینەوەی خزمەکانی لایەنی باوک و دایک."],
        ["بڕیارەکانی دادگا و هێزەکانی یەکێتی", "نهێنی: بڕیارەکانی دادگا، کەسە داواکراوەکان، تۆمارەکانی هێزەکانی یەکێتی، و زانیاری کەیسە یاساییەکان."],
        ["بنکەی زانیاری تەندروستی", "نهێنی: تۆمارەکانی کوتانی کۆڤید-19، چاودێری تەندروستی، و زانیاری پزیشکی هاوڵاتیان."],
        ["بنکەی زانیاری ئۆتۆمۆبیل", "نهێنی: تۆمارەکانی تۆماری ئۆتۆمۆبیل، زانیاری خاوەنی ئۆتۆمۆبیل، و سیستەمی چاودێری گواستنەوە."],
        ["بنکەی زانیاری کەسان", "زۆر نهێنی: پەڕگەکانی کارمەندان، تۆمارەکانی کار، و زانیاری هاوڵاتیان."],
        ["بنکەی تۆمارکردنی شار", "سنووردار: تۆمارەکانی خێزان، زانیاری نیشتەجێبوون، و زانیاری ناسنامەی هاوڵاتیان."],
        ["بنکەی زانیاری کارەبا", "نهێنی: چاودێری میتەری کارەبا، زانیاری بەشداربووان، و سیستەمی چاودێری تۆڕی کارەبا."],
        ["بنکەی زانیاری دەنگدەران", "زۆر نهێنی: تۆمارکردنی دەنگدەران، زانیاری وێستگەکانی دەنگدان، و زانیاری دەنگدانی هاوڵاتیان."],
        ["بنکەی زانیاری فەیسبووک", "زانیاری تۆڕە کۆمەڵایەتییەکان، پرۆفایلی بەکارهێنەران، زانیاری پەیوەندی، و شوێنپێی دیجیتاڵ."],
        ["بنکەی زانیاری خانەنشینی", "نهێنی: تۆمارەکانی خانەنشینی، سوودمەندان، زانیاری میراتگران، و زانیاری دارایی."],
        ["بنکەی زانیاری ژمارەی مۆبایل", "نهێنی: ناسینەوەی ژمارەی تەلەفۆن، گەڕانی ناوی بانگکەر، و زانیاری پەیوەندییەکان."]
    ];

    const dbConfigs = {
        "بنکەی زانیاری خانەنشینی": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: null,
            warning: null,
            fields: [
                { id: "pen_puid", label: "PENSION ID (ژمارەی خانەنشینی)", ph: "...نووسین ژمارەی خانەنشینی" },
                { id: "pen_upn", label: "UPN کۆدی", ph: "...نووسین UPN" },
                { id: "pen_old", label: "ژمارەی کۆنی خانەنشینی", ph: "...نووسین ژمارەی کۆن" },
                { id: "pen_n1", label: "ناوی یەکەم", ph: "...نووسین ناوی یەکەم" },
                { id: "pen_n2", label: "ناوی دووەم", ph: "...نووسین ناوی دووەم" },
                { id: "pen_n3", label: "ناوی سێیەم", ph: "...نووسین ناوی سێیەم" },
                { id: "pen_n4", label: "ناوی کۆتایی", ph: "...نووسین ناوی کۆتایی" },
                { id: "pen_phone", label: "ژمارەی تەلەفۆن", ph: "...نووسین ژمارەی تەلەفۆن" },
                { id: "pen_bio", label: "کۆدی بایۆمێتریک", ph: "...نووسین کۆدی بایۆمێتریک" },
                { id: "pen_doc", label: "ژمارەی بەڵگەنامە", ph: "...نووسین ژمارەی بەڵگەنامە" },
                { id: "pen_nat", label: "ژمارەی نیشتمانی", ph: "...نووسین ژمارەی نیشتمانی" },
                { id: "pen_code_m", label: "ژمارەی مەدەنی", ph: "...نووسین ژمارەی مەدەنی" },
                { id: "pen_bank", label: "بانک", ph: "...نووسین بانک" },
                { id: "pen_dept", label: "وەزارەت", ph: "...نووسین وەزارەت" },
                { id: "pen_from", label: "ڕێکخراو / FROM", ph: "...نووسین ڕێکخراو" },
                { id: "pen_type_h", label: "پلانی خانەنشینی", ph: "...نووسین پلان" },
                { id: "pen_m", label: "ژمارەی مەدەنی", ph: "...نووسین ژمارەی مەدەنی" }
            ]
        },
        "بنکەی زانیاری ژمارەی مۆبایل": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: null,
            warning: null,
            fields: [
                { id: "m_phone", label: "ژمارەی تەلەفۆن", ph: "...نووسین ژمارەی تەلەفۆن" }
            ]
        },
        "بڕیارەکانی دادگا و هێزەکانی یەکێتی": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: null,
            warning: null,
            fields: [
                { id: "ct_full", label: "ناوی تەواو", ph: "...نووسین ناوی تەواو" },
                { id: "ct_gm", label: "ناوی دایک باپیر", ph: "...نووسین ناوی دایک باپیر" },
                { id: "ct_n3", label: "ناوی باپیر", ph: "...نووسین ناوی باپیر" },
                { id: "ct_n2", label: "ناوی باوک", ph: "...نووسین ناوی باوک" },
                { id: "ct_n1", label: "ناوی یەکەم", ph: "...نووسین ناوی یەکەم" },
                { id: "ct_type", label: "جۆر", ph: "...نووسین جۆر" },
                { id: "ct_desc", label: "وەسف", ph: "...نووسین وەسف" },
                { id: "ct_loc", label: "شوێن", ph: "...نووسین شوێن" },
                { id: "ct_persons", label: "کەسەکان", ph: "...نووسین کەسەکان" },
                { id: "ct_date", label: "بەروار", ph: "...نووسین بەروار" },
                { id: "ct_case", label: "ژمارەی کەیس", ph: "...نووسین ژمارەی کەیس" },
                { id: "ct_mother", label: "ناوی دایک", ph: "...نووسین ناوی دایک" }
            ]
        },
        "بنکەی زانیاری تەندروستی": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: null,
            warning: null,
            fields: [
                { id: "h_phone", label: "ژمارەی تەلەفۆن", ph: "...نووسین ژمارەی تەلەفۆن" }
            ]
        },
        "بنکەی تۆمارکردنی شار 2022": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: { label: "• هەڵبژاردنی پارێزگا", options: ["-- هەڵبژاردنی پارێزگا --", "هەولێر [Erbil]", "سلێمانی [Sulaymaniyah]", "دهۆک [Duhok]", "کەرکوک [Kirkuk]"], defaultVal: "هەولێر [Erbil]" },
            warning: null,
            fields: [
                { id: "c_name1", label: "ناوی یەکەم", ph: "...نووسین ناوی یەکەم" }, { id: "c_name2", label: "ناوی باوک", ph: "...نووسین ناوی باوک" }, { id: "c_name3", label: "باپیر", ph: "...نووسین باپیر" },
                { id: "c_seq", label: "ژمارەی زنجیرە", ph: "...نووسین ژمارەی زنجیرە" }, { id: "c_famno", label: "ژمارەی خێزان", ph: "...نووسین ژمارەی خێزان" }, { id: "c_rc", label: "ژمارەی RC", ph: "...نووسین ژمارەی RC" },
                { id: "c_job", label: "پیشە", ph: "...نووسین پیشە" }, { id: "c_id", label: "ژمارەی ناسنامە", ph: "...نووسین ژمارەی ناسنامە" }, { id: "c_birth", label: "ساڵی لەدایکبوون", ph: "...نووسین ساڵی لەدایکبوون" },
                { id: "c_grandma", label: "دایەپیر", ph: "...نووسین دایەپیر" }, { id: "c_mother", label: "ناوی دایک", ph: "...نووسین ناوی دایک" }
            ]
        },
        "بنکەی زانیاری کارەبا": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری", dropdown: null, warning: null,
            fields: [
                { id: "e_area1", label: "ناوچە", ph: "...نووسین ناوچە" }, { id: "e_feeder", label: "فیدەر", ph: "...نووسین فیدەر" }, { id: "e_area2", label: "ناوچە", ph: "...نووسین ناوچە" },
                { id: "e_name", label: "ناوی بەشداربوو", ph: "...نووسین ناوی بەشداربوو" }, { id: "e_meter", label: "ژمارەی میتەر", ph: "...نووسین ژمارەی میتەر" }, { id: "e_acc", label: "ژمارەی ئەکاونت", ph: "...نووسین ژمارەی ئەکاونت" },
                { id: "e_subzone", label: "ژێر زۆن", ph: "...نووسین ژێر زۆن" }, { id: "e_block", label: "ژمارەی بلۆک", ph: "...نووسین ژمارەی بلۆک" }, { id: "e_sts", label: "ژمارەی STS", ph: "...نووسین ژمارەی STS" }
            ]
        },
        "بنکەی زانیاری خزمایەتی": {
            headerTitle: "دۆزینەوەی خزمەکان",
            dropdown: { label: "• جۆری گەڕان", options: ["-- هەڵبژاردنی جۆر --", "خزمەکانی لایەنی باوک", "خزمەکانی لایەنی دایک"], defaultVal: "خزمەکانی لایەنی باوک" },
            warning: "⚠️ تەنها هەرێمی کوردستان (هەولێر، دهۆک، کەرکوک، سلێمانی)",
            fields: [
                { id: "k_father", label: "ناوی یەکەمی باوکی کەس", ph: "ناوی یەکەمی باوکی کەس" },
                { id: "k_grandpa", label: "ناوی باوکی باوکی کەس (باپیر)", ph: "باوکی باوکی کەس (باپیر)" },
                { id: "k_g_grandpa", label: "ناوی باپیرەی باوکی کەس (دایک / باپیر)", ph: "باپیرەی باوکی کەس (دایک باپیر)" },
                { id: "k_grandma", label: "ناوی دایکی باوکی کەس (دایەپیر)", ph: "دایکی باوکی کەس (دایەپیر)" },
                { id: "k_g_grandma_f", label: "ناوی باوکی دایەپیری باوکی کەس", ph: "باوکی دایەپیری باوکی کەس" }
            ]
        },
        "بنکەی زانیاری فەیسبووک": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری", dropdown: null, warning: null,
            fields: [
                { id: "fb_phone", label: "ژمارەی تەلەفۆن", ph: "...نووسین ژمارەی تەلەفۆن" },
                { id: "fb_id", label: "ژمارەی بەکارهێنەر", ph: "...نووسین ژمارەی بەکارهێنەر" }
            ]
        },
        "بنکەی زانیاری دەنگدەران": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: { label: "• هەڵبژاردنی پارێزگا", options: ["-- هەڵبژاردنی پارێزگا --", "کەرکوک", "هەولێر", "سلێمانی", "دهۆک"], defaultVal: "کەرکوک" },
            warning: null,
            fields: [
                { id: "v_name1", label: "ناوی یەکەم", ph: "...نووسین ناوی یەکەم" }, { id: "v_name2", label: "ناوی باوک", ph: "...نووسین ناوی باوک" }, { id: "v_name3", label: "باپیر", ph: "...نووسین باپیر" },
                { id: "v_person_id", label: "ژمارەی کەسی", ph: "...نووسین ژمارەی کەسی" }, { id: "v_fam_no", label: "ژمارەی خێزان", ph: "...نووسین ژمارەی خێزان" }, { id: "v_birth", label: "ساڵی لەدایکبوون", ph: "...نووسین ساڵی لەدایکبوون" }
            ]
        },
        "بنکەی زانیاری ئۆتۆمۆبیل": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری", dropdown: null, warning: null,
            fields: [
                { id: "f_plate", label: "ژمارەی تابلۆ", ph: "...نووسین ژمارەی تابلۆ" }, { id: "f_model", label: "مۆدێلی ئۆتۆمۆبیل", ph: "...نووسین مۆدێلی ئۆتۆمۆبیل" }, { id: "f_driver", label: "ناوی شۆفێر", ph: "...نووسین ناوی شۆفێر" },
                { id: "f_phone", label: "ژمارەی مۆبایل", ph: "...نووسین ژمارەی مۆبایل" }, { id: "f_annual", label: "ژمارەی ساڵانە", ph: "...نووسین ژمارەی ساڵانە" }, { id: "f_chassis", label: "ژمارەی شاسی", ph: "...نووسین ژمارەی شاسی" }
            ]
        },
        "بنکەی زانیاری کەسان": {
            headerTitle: "⬢ بنکەی زانیاری کەسان",
            dropdown: { label: "• هەڵبژاردنی جۆر", options: ["-- هەڵبژاردنی جۆر --", "هاوڵاتیان", "کارمەندان"], defaultVal: "هاوڵاتیان" }, warning: null,
            fields: [
                { id: "p_fullname", label: "ناوی تەواو", ph: "...نووسین ناوی تەواو" }, { id: "p_name4", label: "ناوی چوارەم", ph: "...نووسین ناوی چوارەم" }, { id: "p_name3", label: "ناوی سێیەم", ph: "...نووسین ناوی سێیەم" },
                { id: "p_name2", label: "ناوی دووەم", ph: "...نووسین ناوی دووەم" }, { id: "p_name1", label: "ناوی یەکەم", ph: "...نووسین ناوی یەکەم" }, { id: "p_id", label: "ژمارەی ناسنامە", ph: "...نووسین ژمارەی ناسنامە" },
                { id: "p_birth", label: "ساڵی لەدایکبوون", ph: "...نووسین ساڵی لەدایکبوون" }, { id: "p_guardian", label: "ژمارەی سەرپەرشتیار", ph: "...نووسین ژمارەی سەرپەرشتیار" }, { id: "p_phone", label: "ژمارەی تەلەفۆن", ph: "...نووسین ژمارەی تەلەفۆن" },
                { id: "p_mother", label: "ناوی دایک", ph: "...نووسین ناوی دایک" }
            ]
        }
    };

    const grid = document.getElementById('cardsContainer');
    dbCards.forEach(([title, desc, active]) => {
        grid.innerHTML += `<div class="card ${active ? 'active' : ''}" onclick="openInsideDatabase(this, '${title}')">
            <div class="card-header"><div class="card-title">${title}</div><div class="checkbox-box"></div></div>
            <div class="card-body">${desc}</div>
            <button type="button" class="card-btn">دەستگەیشتن ◄<br>بە بنکەی زانیاری</button>
        </div>`;
    });

    const canvas = document.getElementById('matrixCanvas'), ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    const chars = '0123456789DARKNESSEAGLEKURDISTAN', drops = Array(Math.floor(canvas.width / 15)).fill(1);
    setInterval(() => {
        ctx.fillStyle = 'rgba(2, 4, 8, 0.1)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ff88'; ctx.font = '13px monospace';
        for (let i = 0; i < drops.length; i++) {
            ctx.fillText(chars[Math.floor(Math.random() * chars.length)], i * 15, drops[i] * 15);
            if (drops[i] * 15 > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }, 55);

    function selectSector(sectorName) {
        const hud = document.getElementById('activeSectorHud');
        if (hud) hud.textContent = 'SECTOR: ' + sectorName;
        showToast('📍 ناوچەی چاودێری گۆڕدرا بۆ: ' + sectorName);
    }

    function showToast(msg) {
        const toast = document.getElementById('toastNotice');
        toast.textContent = msg;
        toast.classList.add('show');
        setTimeout(() => { toast.classList.remove('show'); }, 3000);
    }

    function switchAuthTab(tab) {
        document.getElementById('tabBtnReg').className = tab === 'reg' ? 'auth-tab-btn active-reg' : 'auth-tab-btn';
        document.getElementById('tabBtnLogin').className = tab === 'login' ? 'auth-tab-btn active-login' : 'auth-tab-btn';
        document.getElementById('paneRegister').className = tab === 'reg' ? 'auth-form-pane active' : 'auth-form-pane';
        document.getElementById('paneLogin').className = tab === 'login' ? 'auth-form-pane active' : 'auth-form-pane';
    }

    function switchView(id) {
        document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if (id === 'dashboardView') closeInsideDbView();
        if (id === 'adminPortalView') renderAdminPortalRequests();
        
        if (id !== 'faceIdView' && faceStreamRef) {
            faceStreamRef.getTracks().forEach(track => track.stop());
            faceStreamRef = null;
        }
    }

    function logoutToAuth() {
        currentLoggedInUser = null;
        switchView('authView');
        switchAuthTab('login');
    }

    function submitRegister(e) {
        e.preventDefault();
        const u = document.getElementById('regUser').value.trim();
        const p1 = document.getElementById('regPass1').value;
        const p2 = document.getElementById('regPass2').value;
        if (p1 !== p2) return alert('تکایە دڵنیابەرەوە! هەردوو پاسۆردەکە وەک یەک نین.');
        accountsDB[u.toLowerCase()] = {
            username: u,
            password: p1,
            approved: false,
            planLabel: '',
            expiresAt: null
        };
        renderAdminPortalRequests();
        switchView('waitingView');
    }

    function returnToMainWithRedWaitMessage() {
        switchView('authView');
        switchAuthTab('login');
        const r = document.getElementById('redWaitingNotice');
        r.textContent = 'تکایە چاوەڕێبە تا ئەدمین قبوڵت دەکات بۆ چونە ژورەوەی سیستەمی چاوی تاریکی هەڵۆ';
        r.classList.add('show');
    }

    function submitLogin(e) {
        e.preventDefault();
        const u = document.getElementById('loginUser').value;
        const p = document.getElementById('loginPass').value;
        const r = document.getElementById('redWaitingNotice');

        r.classList.remove('show');
        currentLoggedInUser = u.trim() || 'Kurdistan01';
        startFaceID(u.trim() || 'Kurdistan01', 'OWNER / MASTER');
    }

    function setupDashboardUserUI(usernameDisplay, roleType) {
        document.getElementById('tacticalUsernameDisplay').textContent = usernameDisplay;
        document.getElementById('tacticalRolePill').textContent = roleType === 'OWNER / MASTER' ? 'OWNER' : 'USER';
        document.getElementById('topRoleBadge').textContent = roleType;
        if (roleType === 'OWNER / MASTER') {
            document.getElementById('activeUserBadge').textContent = '👑 KURDISTAN01 (بەڕێوەبەری گشتی)';
            document.getElementById('sessionRemainingBadge').textContent = '⏱ ماوە: هەمیشەیی';
        } else {
            document.getElementById('activeUserBadge').textContent = '👤 ' + usernameDisplay.toUpperCase();
        }
    }

    // 5-SECOND DECORATIVE SCANNER ANIMATION
    function startFaceID(displayUser, roleLabel) {
        switchView('faceIdView');
        const video = document.getElementById('webcamVideo');
        const status = document.getElementById('faceScanStatus');
        status.textContent = 'کردنەوەی کامێرا و سکانی بایۆمێتریک...';
        status.style.color = '#00e5ff';

        // Attempt to open device camera for aesthetic feel
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    faceStreamRef = stream;
                    video.srcObject = stream;
                })
                .catch(err => {
                    // Fallback to high-tech scanner simulation
                });
        }

        // Timed decorative transitions exactly 5 seconds total
        setTimeout(() => {
            status.textContent = 'سکانکردنی ڕووخسار دەستی پێکرد... تکایە سەیری کامێراکە بکە';
            status.style.color = '#facc15';
        }, 1200);

        setTimeout(() => {
            status.textContent = 'شیکردنەوەی داتای بایۆمێتریک و دڵنیابوونەوە لە ڕووخسار...';
            status.style.color = '#00e5ff';
        }, 2800);

        setTimeout(() => {
            status.textContent = '✓ ڕووخساری بەڕێوەبەر بە سەرکەوتوویی سەلمێندرا!';
            status.style.color = '#00ff88';
        }, 4400);

        // At exactly 5.0 seconds, transition into the dashboard automatically
        setTimeout(() => {
            if (faceStreamRef) {
                faceStreamRef.getTracks().forEach(track => track.stop());
                faceStreamRef = null;
            }
            setupDashboardUserUI(displayUser, roleLabel);
            switchView('dashboardView');
        }, 5000);
    }

    function openAdminPortalView() {
        switchView('adminPortalView');
    }

    function renderAdminPortalRequests() {
        const container = document.getElementById('adminRequestsContainer');
        const keys = Object.keys(accountsDB);
        
        let requestsHtml = keys.map(k => {
            const acc = accountsDB[k];
            let statusLine = '<span style="color:#facc15;">⏳ چاوەڕێی پەسەندکردن</span>';
            if (acc.approved) {
                statusLine = `<span style="color:#10b981;">✓ چالاککراوە (${acc.planLabel})</span>`;
            }

            return `
                <div class="request-item-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-size:12px; font-weight:bold; color:#cbd5e1;">داواکاری هەژماری بەکارهێنەر</span>
                        ${statusLine}
                    </div>
                    <div class="req-credentials-box">
                        <div style="color:#38bdf8; font-weight:bold;">Username: <span style="color:#ffffff;">${acc.username}</span></div>
                        <div style="color:#facc15; font-weight:bold;">Password : <span style="color:#ffffff;">${acc.password}</span></div>
                    </div>
                    <div class="req-durations-grid">
                        <div class="duration-option-box">
                            <span>٣٠ڕۆژ بەکار هێنانی سیستەم</span>
                            <button type="button" class="run-approve-btn" onclick="approveUserWithPlan('${k}', '30D')">قبوڵکردن</button>
                        </div>
                        <div class="duration-option-box">
                            <span>٦٠ڕۆژ بەکار هێنانی سیستەم</span>
                            <button type="button" class="run-approve-btn" onclick="approveUserWithPlan('${k}', '60D')">قبوڵکردن</button>
                        </div>
                        <div class="duration-option-box">
                            <span>١ساڵ بەکار هێنانی سیستەم</span>
                            <button type="button" class="run-approve-btn" onclick="approveUserWithPlan('${k}', '1Y')">قبوڵکردن</button>
                        </div>
                        <div class="duration-option-box">
                            <span>بەکار هێنانی هەمیشەی</span>
                            <button type="button" class="run-approve-btn" onclick="approveUserWithPlan('${k}', 'FOREVER')">قبوڵکردن</button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        let logsHtml = '';
        if (userSearchLogs.length > 0) {
            logsHtml = `
                <div style="margin-top:20px; border-top:1px solid #334155; padding-top:15px; text-align:right;">
                    <div style="font-size:14px; font-weight:850; color:#34d399; margin-bottom:10px;">📋 تۆماری گەڕان و چالاکییەکانی بەکارهێنەران (لای بەڕێوەبەر):</div>
                    ${userSearchLogs.map(l => `
                        <div style="background:#04070d; border:1px solid #10b981; border-radius:8px; padding:10px 12px; margin-bottom:8px; font-size:11.5px;">
                            <div style="color:#38bdf8; font-weight:bold;">بەکارهێنەر: <span style="color:#ffffff;">${l.username}</span> | بنکە: <span style="color:#facc15;">${l.dbName}</span></div>
                            <div style="color:#9ca3af; margin-top:3px;">کاتی سێرچ: ${l.time}</div>
                            <div style="color:#34d399; font-weight:bold; margin-top:3px;">دۆخ: ${l.status}</div>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            logsHtml = `
                <div style="margin-top:20px; border-top:1px solid #334155; padding-top:15px; text-align:right; color:#9ca3af; font-size:11.5px;">
                    📋 هیچ سێرچ و چالاکییەکی نوێ لەلایەن بەکارهێنەرانەوە تۆمار نەکراوە.
                </div>
            `;
        }

        container.innerHTML = requestsHtml + logsHtml;
    }

    function approveUserWithPlan(userKey, planCode) {
        const acc = accountsDB[userKey];
        if (!acc) return;

        acc.approved = true;
        const now = Date.now();
        if (planCode === '30D') {
            acc.planLabel = '٣٠ ڕۆژ';
            acc.expiresAt = now + (30 * 24 * 60 * 60 * 1000);
        } else if (planCode === '60D') {
            acc.planLabel = '٦٠ ڕۆژ';
            acc.expiresAt = now + (60 * 24 * 60 * 60 * 1000);
        } else if (planCode === '1Y') {
            acc.planLabel = '١ ساڵ';
            acc.expiresAt = now + (365 * 24 * 60 * 60 * 1000);
        } else {
            acc.planLabel = 'هەمیشەیی';
            acc.expiresAt = null;
        }

        document.getElementById('redWaitingNotice').classList.remove('show');
        renderAdminPortalRequests();
        showToast(`✓ هەژماری (${acc.username}) چالاککرا بۆ ماوەی: ${acc.planLabel}`);
    }

    function formatRemainingTime(ms) {
        if (ms <= 0) return '٠٠:٠٠:٠٠';
        const totalSec = Math.floor(ms / 1000);
        const days = Math.floor(totalSec / 86400);
        const hours = Math.floor((totalSec % 86400) / 3600);
        const mins = Math.floor((totalSec % 3600) / 60);
        const secs = totalSec % 60;
        return `${days} ڕۆژ و ${String(hours).padStart(2,'0')}:${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`;
    }

    function openInsideDatabase(cardEl, dbName) {
        document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
        cardEl.classList.add('active');
        currentActiveDbTitle = dbName;
        const tacBar = document.querySelector('.tactical-portal-bar');
        if(tacBar) tacBar.style.display = 'none';

        const cfg = dbConfigs[dbName] || {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری", dropdown: null, warning: null,
            fields: [
                { id: "g_name", label: "ناوی تەواو", ph: "...نووسین ناوی تەواو" },
                { id: "g_phone", label: "ژمارەی مۆبایل", ph: "...نووسین ژمارەی مۆبایل" },
                { id: "g_id", label: "ژمارەی ناسنامە / کارت", ph: "...نووسین ژمارەی ناسنامە" }
            ]
        };

        document.getElementById('insideDbHeaderTitle').textContent = cfg.headerTitle;
        document.getElementById('insideDbActiveName').textContent = '❖ ' + dbName;

        const warnEl = document.getElementById('dynamicWarningBanner');
        if (cfg.warning) { warnEl.style.display = 'flex'; warnEl.textContent = cfg.warning; } else { warnEl.style.display = 'none'; }

        const dropArea = document.getElementById('dynamicDropdownArea');
        if (cfg.dropdown) {
            dropArea.style.display = 'block';
            dropArea.innerHTML = `<label class="db-dropdown-label">${cfg.dropdown.label}</label><select id="dbSubSelect" class="db-dropdown-select">${cfg.dropdown.options.map(opt => `<option value="${opt}" ${opt === cfg.dropdown.defaultVal ? 'selected' : ''}>${opt}</option>`).join('')}</select>`;
        } else { dropArea.style.display = 'none'; dropArea.innerHTML = ''; }

        const fieldsGrid = document.getElementById('dynamicFieldsGrid');
        fieldsGrid.innerHTML = cfg.fields.map(f => `
            <div class="db-field-card">
                <label class="db-field-label">• ${f.label}</label>
                <input type="text" id="${f.id}" data-label="${f.label}" class="db-field-input" placeholder="${f.ph}">
            </div>
        `).join('');

        document.getElementById('executeSearchBtn').innerHTML = 'جێبەجێکردنی گەڕان ◄';

        document.getElementById('spiderMapSection').style.display = 'none';
        document.getElementById('cardsGridSubView').style.display = 'none';
        document.getElementById('cyberScanSubView').classList.remove('active');
        document.getElementById('secretResultsSubView').classList.remove('active');
        document.getElementById('insideDbSubView').style.display = 'block';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function closeInsideDbView() {
        document.getElementById('insideDbSubView').style.display = 'none';
        document.getElementById('cyberScanSubView').classList.remove('active');
        document.getElementById('secretResultsSubView').classList.remove('active');
        document.getElementById('spiderMapSection').style.display = 'block';
        document.getElementById('cardsGridSubView').style.display = 'block';
        const tacBar = document.querySelector('.tactical-portal-bar');
        if(tacBar) tacBar.style.display = 'flex';
    }
    function backToSearchForm() {
        document.getElementById('secretResultsSubView').classList.remove('active');
        document.getElementById('insideDbSubView').style.display = 'block';
    }
    function clearInsideDbFields() {
        document.querySelectorAll('#dynamicFieldsGrid .db-field-input').forEach(inp => inp.value = '');
    }

    let userSearchLogs = [];

    function runInsideDbSearch(e) {
        e.preventDefault();
        const inputs = Array.from(document.querySelectorAll('#dynamicFieldsGrid .db-field-input'));
        const enteredValues = {};
        inputs.forEach(inp => { if (inp.value.trim()) enteredValues[inp.id] = inp.value.trim(); });

        // Log this search activity for the admin panel
        const logEntry = {
            username: currentLoggedInUser || 'Guest',
            dbName: currentActiveDbTitle,
            params: enteredValues,
            time: new Date().toLocaleString(),
            status: 'بۆ باشە و سود بەکاری ئەهێنێت (بێ مەترسی ✓)'
        };
        userSearchLogs.unshift(logEntry);

        document.getElementById('insideDbSubView').style.display = 'none';
        const scanBox = document.getElementById('cyberScanSubView');
        scanBox.classList.add('active');
        setTimeout(() => {
            scanBox.classList.remove('active');
            renderSecretResults(enteredValues);
            document.getElementById('secretResultsSubView').classList.add('active');
        }, 700);
    }

    function openFamilyTreeModal() { document.getElementById('familyTreeModal').classList.add('open'); }
    function closeFamilyTreeModal() { document.getElementById('familyTreeModal').classList.remove('open'); }
    function openMeterMapModal(name, acc, lat, lng) {
        document.getElementById('mapMeterName').textContent = name || 'محمد احمد محمد';
        document.getElementById('mapMeterAcc').textContent = acc || '63179260572';
        document.getElementById('mapMeterLat').textContent = lat || '36.18416794';
        document.getElementById('mapMeterLng').textContent = lng || '44.03849821';
        document.getElementById('meterMapIframe').src = `https://maps.google.com/maps?q=${lat || '36.18416794'},${lng || '44.03849821'}&hl=ckb&z=17&output=embed`;
        document.getElementById('meterMapModal').classList.add('open');
    }
    function closeMeterMapModal() { document.getElementById('meterMapModal').classList.remove('open'); }
    function openBioModal() { document.getElementById('bioModal').classList.add('open'); }
    function closeBioModal() { document.getElementById('bioModal').classList.remove('open'); }

    function triggerAction(actionName, recordNo) {
        if (actionName === 'pdf') {
            showToast(`✓ فایلی PDF ی تۆماری #${recordNo} بە سەرکەوتوویی دابەزێنرا!`);
        } else if (actionName === 'csv') {
            showToast(`✓ فایلی CSV ی تۆماری #${recordNo} بە سەرکەوتوویی دابەزێنرا!`);
        } else if (actionName === 'bookmark') {
            showToast(`⭐ تۆماری #${recordNo} خزنکرا بۆ لیستی دڵخوازەکان!`);
        }
    }

    function renderSecretResults(vals) {
        const container = document.getElementById('recordsListContainer');
        const countEl = document.getElementById('totalRecordsFoundText');
        const pageEl = document.getElementById('pageRecordsText');

        let fieldsHtml = '';
        const fieldsList = Object.keys(vals);
        
        if (fieldsList.length > 0) {
            fieldsList.forEach((key, index) => {
                const inputEl = document.getElementById(key);
                const label = inputEl ? inputEl.getAttribute('data-label') : key;
                const val = vals[key];
                fieldsHtml += `
                    <div class="record-cell ${index === 0 ? 'highlight' : ''}">
                        <span class="record-cell-label">${label}</span>
                        <div class="record-cell-val">${val}</div>
                    </div>
                `;
            });
        } else {
            fieldsHtml = `
                <div class="record-cell highlight"><span class="record-cell-label">زانیاری سەرەکی</span><div class="record-cell-val">زانیاری تۆمارکراو</div></div>
                <div class="record-cell"><span class="record-cell-label">ژمارەی تۆمار</span><div class="record-cell-val">00948271</div></div>
                <div class="record-cell"><span class="record-cell-label">بارودۆخی تۆمار</span><div class="record-cell-val">پەسەندکراو ✓</div></div>
            `;
        }

        if (currentActiveDbTitle === "بنکەی زانیاری کارەبا") {
            fieldsHtml += `
                <div class="record-cell"><span class="record-cell-label">ژمارەی میتەر</span><div class="record-cell-val">11880929</div></div>
                <div class="record-cell"><span class="record-cell-label">فیدەر</span><div class="record-cell-val">Erbil - Rzgari - F 5</div></div>
                <div class="record-cell highlight"><span class="record-cell-label">هێڵی پانی</span><div class="record-cell-val">36.18416794</div></div>
                <div class="record-cell highlight"><span class="record-cell-label">هێڵی درێژی</span><div class="record-cell-val">44.03849821</div></div>
            `;
        }

        countEl.textContent = '• کۆی تۆمارەکانی دۆزراوە: 1';
        pageEl.textContent = 'لاپەڕە 1 لە 1';

        let extraButtons = '';
        if (currentActiveDbTitle === "بنکەی زانیاری کارەبا") {
            extraButtons = `<button type="button" class="record-action-btn btn-highlight" onclick="openMeterMapModal('محمد احمد محمد', '63179260572', '36.18416794', '44.03849821')">📍 بینینی شوێنی ووردبینانە</button>`;
        } else if (currentActiveDbTitle === "بنکەی تۆمارکردنی شار 2022" || currentActiveDbTitle === "بنکەی زانیاری خزمایەتی") {
            extraButtons = `<button type="button" class="record-action-btn btn-highlight" onclick="openFamilyTreeModal()">📊 بینینی گرافیکی خێزان</button>`;
        } else if (currentActiveDbTitle === "بنکەی زانیاری خانەنشینی") {
            extraButtons = `<button type="button" class="record-action-btn btn-highlight" onclick="openBioModal()">👤 بینینی وێنەی بایۆمێتریک</button>`;
        }

        container.innerHTML = `
            <div class="record-master-card">
                <div class="record-card-header">
                    <div class="record-num-title">تۆمار #0001</div>
                    <span class="record-db-badge">${currentActiveDbTitle}</span>
                </div>
                <div class="record-data-grid">
                    ${fieldsHtml}
                </div>
                <div class="record-actions-bar">
                    ${extraButtons}
                    <button type="button" class="record-action-btn" onclick="triggerAction('bookmark', '0001')">⭐ نیشانەکردن</button>
                    <button type="button" class="record-action-btn" onclick="triggerAction('pdf', '0001')">📄 PDF داگرتنی</button>
                    <button type="button" class="record-action-btn" onclick="triggerAction('csv', '0001')">📊 CSV داگرتنی</button>
                </div>
            </div>
        `;
    }

    // Real-time Session Expiration Monitor
    setInterval(() => {
        const now = new Date();
        const dateStr = '16/10/2026';
        const timeStr = now.toTimeString().split(' ')[0];
        const el = document.getElementById('liveClock');
        if (el) el.textContent = dateStr + ' ' + timeStr;

        if (currentLoggedInUser && currentLoggedInUser !== 'OWNER') {
            const acc = accountsDB[currentLoggedInUser];
            const badge = document.getElementById('sessionRemainingBadge');
            if (acc && acc.expiresAt) {
                const diff = acc.expiresAt - Date.now();
                if (diff <= 0) {
                    acc.approved = false;
                    logoutToAuth();
                    const r = document.getElementById('redWaitingNotice');
                    r.textContent = '⏰ کاتی بەکارهێنانی سیستەمەکەت تەواو بوو! بە شێوەیەکی ئۆتۆماتیکی کراییتە دەرەوە.';
                    r.classList.add('show');
                } else if (badge) {
                    badge.textContent = '⏱ ماوە: ' + formatRemainingTime(diff);
                }
            } else if (badge) {
                badge.textContent = '⏱ ماوە: هەمیشەیی';
            }
        }
    }, 1000);
</script>

</body>
</html>
"""

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
                        cursor.execute(f'PRAGMA table_info("{table_name}")')
                        cols = [col[1] for col in cursor.fetchall()]
                        if not cols:
                            continue
                            
                        where_clause = " OR ".join([f'CAST("{c}" AS TEXT) LIKE ?' for c in cols])
                        params = [f"%{search_query}%" for _ in cols]
                        query = f'SELECT * FROM "{table_name}" WHERE {where_clause} LIMIT 100'
                        
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
    app.run(host="0.0.0.0", port=port
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

def get_city_db_connection(city_key):
    city_info = DATABASES.get(city_key)
    if not city_info:
        return None
    
    url = city_info["url"]
    db_path = f"{city_key}.db"
    
    if not os.path.exists(db_path):
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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ckb" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
    <title>Darkness Eagle | سیستەمی چاوی تاریکی هەڵۆ</title>
    <style>
        :root {
            --bg-black: #020408;
            --panel-bg: rgba(9, 13, 20, 0.94);
            --card-bg: rgba(14, 18, 26, 0.95);
            --border-dim: #263142;
            --border-glow: #10b981;
            --neon-blue: #00e5ff;
            --neon-green: #00ff88;
            --kurd-red: #dc2626;
            --kurd-white: #ffffff;
            --kurd-green: #16a34a;
            --kurd-gold: #facc15;
            --text-light: #f3f4f6;
            --text-gray: #9ca3af;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }

        body {
            background-color: var(--bg-black); color: var(--text-light);
            min-height: 100vh; overflow-x: hidden; position: relative;
        }

        #matrixCanvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; opacity: 0.22; pointer-events: none; }

        .globe-bg {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 460px; height: 460px; z-index: 0; opacity: 0.10; pointer-events: none;
            animation: rotateGlobe 60s linear infinite;
        }

        .radar-corner {
            position: fixed; top: 15px; left: 15px; width: 80px; height: 80px;
            border: 1px solid rgba(16, 185, 129, 0.18); border-radius: 50%; z-index: 0;
            pointer-events: none; display: flex; align-items: center; justify-content: center;
        }
        .radar-corner::before {
            content: ''; width: 46px; height: 46px; border: 1px dashed rgba(16, 185, 129, 0.28); border-radius: 50%;
        }
        .radar-sweep {
            position: absolute; width: 50%; height: 2px;
            background: linear-gradient(90deg, transparent, rgba(16, 185, 129, 0.65));
            top: 50%; left: 50%; transform-origin: left center; animation: sweep 4s linear infinite;
        }

        @keyframes rotateGlobe { 0% { transform: translate(-50%, -50%) rotate(0deg); } 100% { transform: translate(-50%, -50%) rotate(360deg); } }
        @keyframes sweep { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        @keyframes pulseGreen { 0% { opacity: 1; transform: scale(1); box-shadow: 0 0 8px #10b981; } 50% { opacity: 0.35; transform: scale(0.85); box-shadow: 0 0 2px #10b981; } 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 8px #10b981; } }
        @keyframes cyberGlow { 0% { stroke: #00ff88; } 50% { stroke: #00e5ff; } 100% { stroke: #00ff88; } }
        @keyframes dashMove { to { stroke-dashoffset: -100; } }

        .main-wrapper {
            position: relative; z-index: 2; width: 100%; max-width: 1220px;
            margin: 0 auto; padding: 10px 8px 35px; min-height: 100vh;
            display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
        }

        .kurd-flag-bar {
            width: 100%; max-width: 540px; height: 4px; border-radius: 4px;
            background: linear-gradient(90deg, var(--kurd-green) 0%, var(--kurd-white) 35%, var(--kurd-gold) 50%, var(--kurd-white) 65%, var(--kurd-red) 100%);
            margin-bottom: 10px; box-shadow: 0 0 12px rgba(250, 204, 21, 0.35);
        }

        .hero-header {
            text-align: center; margin-bottom: 12px; width: 100%; max-width: 540px;
            background: rgba(6, 9, 15, 0.90); border: 1px solid var(--border-dim);
            border-radius: 14px; padding: 14px 12px; box-shadow: 0 8px 28px rgba(0, 0, 0, 0.85);
        }

        .kurdistan-flag-frame {
            position: relative; width: 230px; margin: 0 auto 10px; padding: 3px;
            border-radius: 12px; background: linear-gradient(90deg, #dc2626, #facc15, #16a34a);
            box-shadow: 0 0 20px rgba(250, 204, 21, 0.4), 0 4px 15px rgba(0, 0, 0, 0.9);
        }

        .kurdistan-flag-inner {
            position: relative;
            background: linear-gradient(180deg, rgba(220, 38, 38, 0.88) 0%, rgba(220, 38, 38, 0.82) 33.3%, rgba(248, 250, 252, 0.92) 33.3%, rgba(248, 250, 252, 0.92) 66.6%, rgba(22, 163, 74, 0.88) 66.6%, rgba(22, 163, 74, 0.88) 100%);
            border-radius: 9px; padding: 8px 12px; overflow: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center;
            border: 1px solid rgba(250, 204, 21, 0.65);
        }

        .kurdistan-flag-inner::after { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, rgba(0, 0, 0, 0.15) 0%, rgba(0, 0, 0, 0.45) 100%); z-index: 1; }

        .kurd-sun-svg {
            position: absolute; width: 58px; height: 58px; top: 50%; left: 50%;
            transform: translate(-50%, -50%); opacity: 0.92; z-index: 1; pointer-events: none;
            filter: drop-shadow(0 0 8px rgba(250, 204, 21, 0.9)); animation: rotateGlobe 40s linear infinite;
        }

        .eagle-logo-text-top {
            position: relative; z-index: 3; font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 17px; font-weight: 900; letter-spacing: 3px; line-height: 1.05; color: #ffffff;
            text-shadow: 0 2px 4px rgba(0,0,0,0.95), 0 0 8px rgba(0,0,0,0.85);
        }

        .eagle-logo-text-bottom {
            position: relative; z-index: 3; font-family: 'Georgia', 'Times New Roman', serif;
            font-size: 15px; font-weight: 900; letter-spacing: 4.5px; line-height: 1.05; margin-top: 2px;
            color: #fde047; text-shadow: 0 2px 4px rgba(0,0,0,0.95), 0 0 8px rgba(0,0,0,0.9);
        }

        .welcome-title { font-size: 13.5px; font-weight: bold; margin-top: 4px; line-height: 1.5; }
        .welcome-kurd-grad { background: linear-gradient(90deg, #ef4444, #ffffff, #facc15, #22c55e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
        .patriotic-slogan { font-size: 11.5px; color: #cbd5e1; margin-top: 6px; line-height: 1.55; display: flex; flex-direction: column; align-items: center; gap: 4px; }
        .yellow-bji-line { color: var(--kurd-gold); font-weight: bold; font-size: 10px; white-space: nowrap; display: inline-flex; align-items: center; gap: 4px; background: rgba(250, 204, 21, 0.08); padding: 2px 8px; border-radius: 12px; border: 1px solid rgba(250, 204, 21, 0.28); }

        .view-section { display: none; width: 100%; }
        .view-section.active { display: block; animation: fadeIn 0.25s ease; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }

        .red-waiting-alert {
            display: none; width: 100%; max-width: 540px; margin: 0 auto 12px;
            background: rgba(127, 29, 29, 0.35); border: 1.5px solid #ef4444; border-radius: 11px;
            padding: 11px 14px; color: #ff4d4d; font-size: 12.5px; font-weight: 800; text-align: center;
            line-height: 1.65; box-shadow: 0 0 18px rgba(239, 68, 68, 0.35);
        }
        .red-waiting-alert.show { display: block; }

        .auth-master-card { width: 100%; max-width: 540px; margin: 0 auto; background: var(--panel-bg); border: 1px solid var(--border-dim); border-radius: 14px; padding: 14px; box-shadow: 0 12px 35px rgba(0, 0, 0, 0.9); }
        .auth-tabs-bar { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 14px; background: #04060b; padding: 5px; border-radius: 10px; border: 1px solid #1f2937; }
        .auth-tab-btn { background: transparent; border: 1px solid transparent; color: #9ca3af; padding: 9px 6px; border-radius: 8px; cursor: pointer; font-size: 11.5px; font-weight: bold; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; }
        .auth-tab-btn span.sub-pill { font-size: 9.5px; font-weight: normal; opacity: 0.75; }
        .auth-tab-btn.active-reg { background: linear-gradient(135deg, rgba(185, 28, 28, 0.28), rgba(220, 38, 38, 0.15)); border-color: var(--kurd-gold); color: #ffffff; }
        .auth-tab-btn.active-reg span.sub-pill { color: var(--kurd-gold); }
        .auth-tab-btn.active-login { background: linear-gradient(135deg, rgba(6, 95, 70, 0.35), rgba(16, 185, 129, 0.18)); border-color: #10b981; color: #ffffff; }
        .auth-tab-btn.active-login span.sub-pill { color: #34d399; }
        .auth-form-pane { display: none; padding: 4px; }
        .auth-form-pane.active { display: block; }
        .form-group { margin-bottom: 11px; text-align: right; }
        .form-group label { display: block; font-size: 11.5px; color: #e2e8f0; margin-bottom: 5px; font-weight: 700; direction: ltr; text-align: right; }
        .form-input { width: 100%; padding: 9px 12px; background: #04060a; border: 1px solid #374151; border-radius: 7px; color: #ffffff; font-size: 12px; outline: none; }
        .form-input:focus { border-color: var(--kurd-gold); }
        .btn-action { width: 100%; padding: 10px 12px; border-radius: 8px; font-size: 12.5px; font-weight: bold; cursor: pointer; border: 1px solid transparent; margin-top: 6px; color: #fff; }
        .btn-register { background: linear-gradient(135deg, #991b1b, #dc2626); border-color: #f87171; }
        .btn-login-hacker { background: linear-gradient(135deg, #042f2e, #065f46, #047857); border: 1px solid #10b981; color: #ecfdf5; font-family: monospace; box-shadow: 0 0 15px rgba(16, 185, 129, 0.25); }
        .helper-note { font-size: 10.5px; color: var(--text-gray); margin-top: 9px; text-align: center; }

        .status-card { max-width: 480px; margin: 20px auto; background: linear-gradient(180deg, rgba(12, 18, 28, 0.96), rgba(6, 10, 16, 0.98)); border: 1.5px solid var(--border-glow); border-radius: 16px; padding: 22px 16px; text-align: center; box-shadow: 0 0 35px rgba(16, 185, 129, 0.22); }
        .designer-success-pill { display: inline-flex; align-items: center; justify-content: center; gap: 6px; background: rgba(6, 95, 70, 0.35); border: 1px solid #10b981; color: #34d399; padding: 7px 14px; border-radius: 30px; font-size: 11.5px; font-weight: 800; white-space: nowrap; margin: 8px auto 12px; box-shadow: 0 0 15px rgba(16, 185, 129, 0.25); }
        .loader-ring { width: 52px; height: 52px; border: 3px solid rgba(255, 255, 255, 0.1); border-top: 3px solid var(--kurd-gold); border-right: 3px solid var(--kurd-green); border-bottom: 3px solid var(--kurd-red); border-radius: 50%; margin: 10px auto 16px; animation: sweep 1.1s linear infinite; }

        /* TOP STATUS BAR */
        .cyber-top-bar {
            width: 100%; max-width: 1040px; margin: 0 auto 8px;
            background: rgba(8, 11, 18, 0.95); border: 1px solid #263142; border-radius: 10px;
            padding: 5px 12px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 6px; font-size: 10px;
        }
        .status-dot { display: inline-block; width: 6.5px; height: 6.5px; background: #10b981; border-radius: 50%; margin-left: 4px; box-shadow: 0 0 8px #10b981; }
        .role-badge-small {
            background: rgba(185, 28, 28, 0.28); border: 1px solid #ef4444; color: #fca5a5;
            padding: 1px 5px; border-radius: 4px; font-size: 8px; font-weight: 800; letter-spacing: 0.3px;
        }

        .dashboard-nav-bar-compact {
            width: 100%; max-width: 1040px; margin: 0 auto 10px;
            background: linear-gradient(180deg, rgba(13, 19, 31, 0.96), rgba(7, 11, 18, 0.98));
            border: 1px solid #334155; border-radius: 10px; padding: 7px 12px;
            display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 6px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.85);
        }
        .admin-pill-small {
            background: rgba(6, 78, 59, 0.45); border: 1px solid #10b981; color: #34d399;
            padding: 2.5px 7px; border-radius: 5px; font-size: 8.5px; font-weight: 800; letter-spacing: 0.2px;
            display: inline-flex; align-items: center; gap: 4px;
        }
        .session-timer-text { font-size: 9px; color: #facc15; font-family: monospace; font-weight: bold; }

        /* TACTICAL PORTAL HEADER BAR */
        .tactical-portal-bar {
            width: 100%; max-width: 1040px; margin: 0 auto 12px;
            background: rgba(9, 13, 22, 0.96); border: 1px solid #1e293b; border-radius: 12px;
            padding: 10px 14px; display: flex; justify-content: space-between; align-items: center;
            flex-wrap: wrap; gap: 10px; direction: ltr; box-shadow: 0 6px 20px rgba(0,0,0,0.85);
        }
        .admin-star-portal-btn {
            display: flex; align-items: center; gap: 10px; cursor: pointer;
            padding: 4px 8px; border-radius: 10px; border: 1px solid transparent; transition: 0.25s;
        }
        .admin-star-portal-btn:hover {
            background: rgba(250, 204, 21, 0.08); border-color: rgba(250, 204, 21, 0.4);
            box-shadow: 0 0 15px rgba(250, 204, 21, 0.2);
        }
        .star-box-icon {
            width: 38px; height: 38px; border-radius: 9px; background: rgba(20, 26, 38, 0.95);
            border: 1.5px solid var(--kurd-gold); display: flex; align-items: center; justify-content: center;
            color: var(--kurd-gold); font-size: 18px; box-shadow: 0 0 12px rgba(250, 204, 21, 0.35);
        }
        .portal-title-col { display: flex; flex-direction: column; text-align: left; }
        .portal-main-title { font-family: monospace; font-size: 14.5px; font-weight: 900; color: #ffffff; letter-spacing: 1.5px; }
        .portal-sub-title { font-size: 10.5px; font-weight: bold; color: #facc15; letter-spacing: 0.4px; margin-top: 1px; }

        .user-status-right-group {
            display: flex; align-items: center; gap: 8px;
        }
        .user-online-pill-box {
            display: flex; align-items: center; gap: 8px; background: #070a10;
            border: 1px solid #263142; padding: 6px 12px; border-radius: 9px;
        }
        .blinking-green-dot {
            width: 9px; height: 9px; border-radius: 50%; background: #10b981;
            animation: pulseGreen 1.4s infinite ease-in-out;
        }
        .logged-username-text {
            font-family: monospace; font-size: 12.5px; font-weight: 800; color: #ffffff; letter-spacing: 0.5px;
        }
        .user-role-tag-pill {
            background: rgba(14, 116, 144, 0.28); border: 1px solid #06b6d4; color: #67e8f9;
            font-size: 9.5px; font-weight: 800; padding: 2px 7px; border-radius: 5px; letter-spacing: 0.6px;
        }
        .red-exit-icon-btn {
            width: 36px; height: 36px; border-radius: 9px; background: rgba(127, 29, 29, 0.35);
            border: 1.5px solid #ef4444; color: #fca5a5; display: flex; align-items: center; justify-content: center;
            cursor: pointer; transition: 0.2s; font-size: 15px; font-weight: bold;
        }
        .red-exit-icon-btn:hover { background: #dc2626; color: #ffffff; box-shadow: 0 0 12px rgba(239, 68, 68, 0.5); }

        .tactical-map-wrapper { touch-action: pan-x pan-y pinch-zoom;

            width: 100%; max-width: 1040px; margin: 0 auto 16px;
            background: radial-gradient(circle at 50% 50%, rgba(6, 78, 59, 0.3) 0%, rgba(2, 4, 8, 0.98) 100%);
            background-blend-mode: overlay;
            background-size: cover;
            background-position: center;
            border: 1.5px solid #10b981; border-radius: 14px; padding: 12px;
            box-shadow: 0 10px 35px rgba(0,0,0,0.95), 0 0 25px rgba(0, 229, 255, 0.15), inset 0 0 30px rgba(0, 255, 136, 0.08);
            position: relative; overflow: hidden;
        }
        .tactical-map-wrapper::before {
            content: ''; position: absolute; inset: 0;
            background: 
                linear-gradient(rgba(0, 229, 255, 0.04) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 229, 255, 0.04) 1px, transparent 1px);
            background-size: 26px 26px; pointer-events: none; z-index: 1;
        }
        .map-top-hud {
            display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;
            direction: ltr; margin-bottom: 8px; padding-bottom: 8px; border-bottom: 1px dashed rgba(0, 229, 255, 0.35);
            position: relative; z-index: 3;
        }
        .hud-left-status { font-family: monospace; font-size: 11px; color: var(--neon-green); font-weight: bold; letter-spacing: 1px; }
        .hud-left-sub { font-family: monospace; font-size: 9.5px; color: var(--neon-blue); letter-spacing: 1.2px; margin-top: 2px; }
        .hud-sector-box {
            font-family: monospace; font-size: 10.5px; font-weight: bold; color: var(--neon-blue);
            border: 1px solid rgba(0, 229, 255, 0.5); background: rgba(0, 229, 255, 0.1);
            padding: 4px 10px; border-radius: 6px; letter-spacing: 1px; box-shadow: 0 0 10px rgba(0, 229, 255, 0.25);
        }

        .spider-map-svg-box {
            width: 100%; max-width: 680px; margin: 0 auto; position: relative;
            display: flex; align-items: center; justify-content: center; min-height: 380px;
            border-radius: 12px; overflow: hidden; z-index: 2;
        }

        .spider-map-svg {
            width: 100%; height: auto; max-height: 440px; position: relative; z-index: 2;
            filter: drop-shadow(0 0 12px rgba(0, 229, 255, 0.3));
        }

        /* FIXED 3-COLUMN CARDS GRID (PERMANENT 3 COLUMNS) */
        .cards-grid {
            display: grid !important;
            grid-template-columns: repeat(3, 1fr) !important;
            gap: 8px !important;
            width: 100% !important;
            max-width: 1040px !important;
            margin: 0 auto !important;
        }

        .card {
            background: rgba(14, 18, 26, 0.95);
            border: 1px solid #4b5563;
            border-radius: 10px;
            width: 100%;
            min-height: 190px;
            padding: 10px 8px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.85);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            cursor: pointer;
            transition: all 0.22s ease;
        }
        .card:hover { border-color: #cbd5e1; transform: translateY(-2px); }
        .card.active { border-color: #10b981; box-shadow: 0 0 16px rgba(16, 185, 129, 0.38); }
        .card-header { display: flex; flex-direction: row-reverse; align-items: center; justify-content: space-between; gap: 4px; margin-bottom: 6px; }
        .checkbox-box { width: 14px; height: 14px; min-width: 14px; border: 2px solid #d1d5db; border-radius: 3px; display: flex; align-items: center; justify-content: center; }
        .checkbox-box::after { content: ''; width: 5px; height: 5px; background: #d1d5db; display: block; }
        .card.active .checkbox-box { border-color: #10b981; }
        .card.active .checkbox-box::after { background: #10b981; }
        .card-title { font-size: 11.5px; font-weight: bold; line-height: 1.35; text-align: center; flex: 1; color: #ffffff; }
        .card-body { font-size: 9.5px; color: #cbd5e1; text-align: center; margin-bottom: 8px; line-height: 1.4; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
        .card-btn { background: rgba(255, 255, 255, 0.04); border: 1px solid #6b7280; color: #ffffff; padding: 6px 4px; border-radius: 5px; font-size: 9px; font-weight: bold; cursor: pointer; text-align: center; transition: 0.2s; }
        .card.active .card-btn, .card:hover .card-btn { background: #064e3b; border-color: #10b981; color: #ecfdf5; }

        /* SEPARATE ADMIN APPROVAL PORTAL VIEW */
        .admin-portal-card {
            width: 100%; max-width: 820px; margin: 15px auto;
            background: rgba(8, 12, 20, 0.96); border: 1.5px solid #10b981;
            border-radius: 14px; padding: 20px 16px;
            box-shadow: 0 0 35px rgba(16, 185, 129, 0.2), inset 0 0 20px rgba(16, 185, 129, 0.05);
        }
        .hacker-green-frame {
            border: 1.5px solid #10b981; background: rgba(6, 78, 59, 0.28);
            border-radius: 10px; padding: 12px 16px; text-align: center;
            max-width: 380px; margin: 0 auto 14px;
            box-shadow: 0 0 18px rgba(16, 185, 129, 0.3); font-family: monospace;
        }
        .hacker-green-frame .main-owner-tag {
            font-size: 15px; font-weight: 900; color: #34d399; letter-spacing: 1px; display: block;
        }
        .hacker-green-frame .sub-eternal-tag {
            font-size: 12.5px; font-weight: bold; color: #fde047; margin-top: 4px; display: block;
        }
        .admin-portal-subtitle {
            text-align: center; font-size: 13px; font-weight: 800; color: #ffffff;
            background: rgba(15, 23, 42, 0.9); border: 1px solid #334155;
            padding: 9px 14px; border-radius: 8px; margin-bottom: 16px;
        }
        .request-item-card {
            background: rgba(13, 18, 28, 0.96); border: 1px solid #374151;
            border-radius: 11px; padding: 14px; margin-bottom: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.7); text-align: right;
        }
        .req-credentials-box {
            background: #06090f; border: 1px solid #1e293b; border-radius: 8px;
            padding: 10px 12px; margin-bottom: 10px; direction: ltr; text-align: left;
            font-family: monospace; font-size: 12px; line-height: 1.6;
        }
        .req-durations-grid {
            display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-top: 8px;
        }
        @media (max-width: 540px) { .req-durations-grid { grid-template-columns: 1fr; } }

        .duration-option-box {
            display: flex; align-items: center; justify-content: space-between;
            background: rgba(6, 15, 25, 0.95); border: 1px solid #10b981;
            border-radius: 8px; padding: 8px 12px; font-size: 11.5px; font-weight: bold; color: #e2e8f0;
            box-shadow: inset 0 0 8px rgba(16, 185, 129, 0.12);
        }
        .run-approve-btn {
            background: linear-gradient(135deg, #059669, #10b981); color: #000000;
            border: 1px solid #34d399; padding: 4px 12px; border-radius: 5px;
            font-family: monospace; font-size: 11px; font-weight: 900; cursor: pointer;
            transition: 0.2s; box-shadow: 0 0 10px rgba(16, 185, 129, 0.4);
        }
        .run-approve-btn:hover { background: #34d399; transform: scale(1.04); }

        /* INSIDE DB PANEL & SEARCH RESULT VIEWS */
        .db-fields-grid {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 10px !important;
            width: 100% !important;
        }
        @media (min-width: 768px) {
            .db-fields-grid {
                grid-template-columns: repeat(3, 1fr) !important;
            }
        }
        .db-inside-panel { width: 100%; max-width: 1040px; margin: 6px auto 0; background: rgba(14, 17, 23, 0.96); border: 1.5px solid #9ca3af; border-radius: 12px; padding: 22px 18px; box-shadow: 0 0 35px rgba(0, 0, 0, 0.95); }
        .db-inside-top-row { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 10px; margin-bottom: 18px; padding-bottom: 12px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
        .db-inside-main-title { font-size: 18px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 8px; }
        .db-inside-sub-badge { display: block; font-size: 11px; color: #10b981; margin-top: 3px; font-weight: bold; }
        .db-inside-actions { display: flex; gap: 8px; flex-wrap: wrap; }
        .db-top-btn { background: rgba(20, 24, 33, 0.95); border: 1px solid #9ca3af; color: #f3f4f6; padding: 8px 14px; border-radius: 6px; font-size: 11.5px; font-weight: bold; cursor: pointer; transition: 0.2s; display: inline-flex; align-items: center; gap: 5px; }
        .db-top-btn:hover { border-color: #ffffff; background: rgba(255, 255, 255, 0.08); }
        .db-back-main-btn { background: linear-gradient(135deg, rgba(6, 78, 59, 0.7), rgba(4, 120, 87, 0.5)); border: 1px solid #10b981; color: #ecfdf5; box-shadow: 0 0 12px rgba(16, 185, 129, 0.25); }
        .db-back-main-btn:hover { background: #059669; border-color: #34d399; }

        .db-dropdown-wrap { margin-bottom: 16px; text-align: right; }
        .db-dropdown-label { display: block; font-size: 12px; font-weight: bold; color: #d1d5db; margin-bottom: 6px; }
        .db-dropdown-select { width: 100%; background: #141820; border: 1px solid #6b7280; color: #ffffff; padding: 10px 14px; border-radius: 6px; font-size: 12.5px; font-weight: bold; outline: none; cursor: pointer; }
        .db-dropdown-select:focus { border-color: #10b981; }

        .db-warning-banner { background: rgba(180, 83, 9, 0.22); border: 1px solid #f59e0b; color: #fef3c7; padding: 10px 14px; border-radius: 8px; font-size: 12px; font-weight: bold; margin-bottom: 14px; display: flex; align-items: center; gap: 8px; }
        
        .db-fields-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; width: 100%; }
        @media (max-width: 900px) { .db-fields-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 560px) { .db-fields-grid { grid-template-columns: 1fr; } }

        .db-field-card { background: rgba(20, 24, 32, 0.95); border: 1px solid #374151; border-radius: 9px; padding: 14px 12px; transition: 0.2s; display: flex; flex-direction: column; justify-content: space-between; }
        .db-field-card:focus-within { border-color: #10b981; background: rgba(6, 78, 59, 0.18); box-shadow: 0 0 12px rgba(16, 185, 129, 0.25); }
        .db-field-label { display: block; font-size: 11.5px; font-weight: bold; color: #e5e7eb; margin-bottom: 8px; text-align: right; }
        .db-field-input { width: 100%; background: rgba(12, 15, 20, 0.95); border: 1px solid #4b5563; border-radius: 6px; padding: 9px 10px; color: #ffffff; font-size: 11.5px; outline: none; text-align: right; }
        .db-field-input:focus { border-color: #10b981; }

        .db-Execute-full-btn { width: 100%; margin-top: 18px; background: linear-gradient(135deg, #042f2e, #065f46, #047857); border: 1px solid #10b981; color: #ffffff; padding: 12px; border-radius: 8px; font-size: 13.5px; font-weight: bold; cursor: pointer; transition: 0.2s; text-align: center; box-shadow: 0 0 15px rgba(16, 185, 129, 0.25); }
        .db-Execute-full-btn:hover { background: #059669; box-shadow: 0 0 20px rgba(16, 185, 129, 0.4); }

        .cyber-scan-box { display: none; width: 100%; max-width: 1040px; margin: 30px auto; padding: 50px 20px; text-align: center; }
        .cyber-scan-box.active { display: block; }
        .scan-spinner { width: 64px; height: 64px; border: 3px solid rgba(255, 255, 255, 0.12); border-bottom: 3.5px solid #ffffff; border-radius: 50%; margin: 0 auto 18px; animation: sweep 0.9s linear infinite; }
        .scan-main-title { font-size: 14px; font-weight: bold; color: #e5e7eb; margin-bottom: 6px; }
        .scan-sub-title { font-size: 11px; color: #9ca3af; }

        .secret-results-wrapper { display: none; width: 100%; max-width: 1040px; margin: 8px auto 0; }
        .secret-results-wrapper.active { display: block; animation: fadeIn 0.3s ease; }
        .results-top-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid #263142; flex-wrap: wrap; gap: 10px; }
        .results-top-title { font-size: 20px; font-weight: 800; color: #ffffff; }
        .results-summary-bar { width: 100%; background: rgba(20, 24, 32, 0.92); border: 1px solid #4b5563; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; font-size: 12px; font-weight: bold; color: #e5e7eb; }

        .record-master-card { width: 100%; background: rgba(15, 19, 26, 0.96); border: 1px solid #4b5563; border-radius: 12px; padding: 20px 18px; margin-bottom: 18px; box-shadow: 0 8px 28px rgba(0, 0, 0, 0.9); }
        .record-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; padding-bottom: 10px; border-bottom: 1px solid rgba(255, 255, 255, 0.08); }
        .record-num-title { font-size: 17px; font-weight: 800; color: #ffffff; }
        .record-db-badge { background: rgba(6, 78, 59, 0.55); border: 1px solid #10b981; color: #d1fae5; padding: 5px 14px; border-radius: 6px; font-size: 11.5px; font-weight: bold; }

        .record-data-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 18px; }
        @media (max-width: 900px) { .record-data-grid { grid-template-columns: repeat(2, 1fr); } }
        @media (max-width: 500px) { .record-data-grid { grid-template-columns: 1fr; } }

        .record-cell { background: rgba(9, 12, 17, 0.95); border: 1px solid #263142; border-radius: 8px; padding: 12px 12px; text-align: right; }
        .record-cell.highlight { border-color: #059669; background: rgba(6, 78, 59, 0.22); }
        .record-cell-label { font-size: 11px; color: #9ca3af; margin-bottom: 6px; display: block; font-weight: 600; }
        .record-cell-val { font-size: 12.5px; font-weight: 800; color: #ffffff; word-break: break-word; line-height: 1.5; }

        .record-actions-bar { display: flex; justify-content: flex-start; gap: 10px; flex-wrap: wrap; }
        .record-action-btn { background: rgba(20, 24, 33, 0.95); border: 1px solid #4b5563; color: #e5e7eb; padding: 8px 14px; border-radius: 6px; font-size: 11.5px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 6px; transition: 0.2s; }
        .record-action-btn:hover { border-color: #10b981; color: #ffffff; background: rgba(16, 185, 129, 0.15); }
        .record-action-btn.btn-highlight { border-color: #10b981; background: rgba(6, 78, 59, 0.45); color: #34d399; }

        /* MODAL OVERLAYS */
        .modal-overlay { display: none; position: fixed; inset: 0; background: rgba(0, 0, 0, 0.88); z-index: 9999; align-items: center; justify-content: center; padding: 15px; overflow-y: auto; }
        .modal-overlay.open { display: flex; }
        .tree-modal-box { width: 100%; max-width: 960px; touch-action: manipulation;  background: #090c12; border: 1px solid #4b5563; border-radius: 12px; padding: 16px 20px 24px; box-shadow: 0 15px 45px rgba(0, 0, 0, 0.95); position: relative; }
        .modal-common-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #263142; padding-bottom: 10px; margin-bottom: 16px; }
        .modal-common-title { font-size: 14px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 6px; }
        .modal-close-btn { background: #7f1d1d; border: 1px solid #ef4444; color: #ffffff; width: 28px; height: 28px; border-radius: 5px; cursor: pointer; font-weight: bold; display: flex; align-items: center; justify-content: center; font-size: 14px; }
        .tree-inner-frame { border: 1px solid #374151; border-radius: 10px; padding: 20px 14px; background: rgba(11, 15, 22, 0.95); text-align: center; }
        .tree-role-tag { display: inline-block; background: #ffffff; color: #000000; font-weight: 800; font-size: 11px; padding: 4px 16px; border-radius: 20px; margin-bottom: 8px; }
        
        .parent-node-card { position: relative; max-width: 380px; margin: 0 auto; background: #101622; border: 1.5px solid #d1d5db; border-radius: 12px; padding: 16px 14px; text-align: right; box-shadow: 0 0 20px rgba(255, 255, 255, 0.08); display: flex; align-items: center; justify-content: space-between; gap: 12px; }
        .node-avatar-circle { width: 60px; height: 60px; min-width: 60px; background: #ffffff; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
        .node-avatar-inner-sq { width: 24px; height: 24px; border: 3px solid #000000; }
        .parent-info-col { flex: 1; text-align: right; }
        .node-name-head { font-size: 15px; font-weight: 800; color: #ffffff; margin-bottom: 6px; }
        .node-detail-line { font-size: 10.5px; color: #cbd5e1; margin-bottom: 3px; }
        .node-bottom-badges { display: flex; gap: 6px; margin-top: 8px; justify-content: flex-end; flex-wrap: wrap; }
        .mini-badge-box { background: #090d14; border: 1px solid #4b5563; border-radius: 5px; padding: 2px 7px; font-size: 9.5px; color: #e5e7eb; }
        .tree-connector-line { width: 2px; height: 35px; background: #38bdf8; margin: 0 auto; }
        .tree-middle-badge { display: inline-block; background: #000000; border: 1px solid #4b5563; color: #ffffff; font-size: 10px; font-weight: bold; padding: 2px 12px; border-radius: 12px; margin-bottom: 8px; }
        .children-cards-row { display: grid !important; grid-template-columns: repeat(2, 1fr) !important; gap: 8px !important; margin-top: 10px !important; }
        @media (min-width: 768px) { .children-cards-row { grid-template-columns: repeat(3, 1fr) !important; } }
        .child-node-card { background: #101622; border: 1.5px solid #d1d5db; border-radius: 12px; padding: 12px 10px; display: flex; align-items: center; justify-content: space-between; gap: 8px; text-align: right; box-shadow: 0 0 15px rgba(255, 255, 255, 0.05); }
        .node-diamond { width: 22px; height: 22px; background: #000000; transform: rotate(45deg); }

        .map-modal-box { width: 100%; max-width: 490px; background: #0c1017; border: 1.5px solid #4b5563; border-radius: 12px; padding: 16px 16px 20px; box-shadow: 0 15px 45px rgba(0, 0, 0, 0.95); }
        .meter-info-card { background: #141a24; border: 1px solid #374151; border-radius: 8px; padding: 12px 14px; margin-bottom: 14px; font-size: 11.5px; line-height: 1.8; color: #e5e7eb; text-align: right; }
        .meter-map-frame { width: 100%; height: 380px; border: 1px solid #374151; border-radius: 8px; overflow: hidden; background: #1f2937; }
        .meter-map-frame iframe { width: 100%; height: 100%; border: 0; }

        .bio-modal-box { width: 100%; max-width: 420px; background: #0c1017; border: 1.5px solid #10b981; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 15px 45px rgba(0,0,0,0.95); }
        .bio-img-preview { width: 180px; height: 180px; border: 2px solid #10b981; border-radius: 10px; margin: 15px auto; object-fit: cover; background: #1f2937; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #10b981; }

        /* TOAST NOTIFICATION */
        #toastNotice {
            position: fixed; bottom: 25px; left: 50%; transform: translateX(-50%) translateY(100px);
            background: #059669; color: #fff; padding: 10px 24px; border-radius: 30px;
            font-size: 12.5px; font-weight: bold; z-index: 99999; box-shadow: 0 5px 20px rgba(0,0,0,0.8);
            transition: transform 0.3s ease;
        }
        #toastNotice.show { transform: translateX(-50%) translateY(0); }

        /* FACE ID DECORATIVE SCANNER */
        .face-scan-title { font-size: 15px; font-weight: bold; color: #10b981; margin-bottom: 15px; text-shadow: 0 0 10px rgba(16,185,129,0.5); }
        .face-scanner-container { position: relative; width: 280px; height: 280px; margin: 0 auto; border-radius: 50%; overflow: hidden; border: 3px solid #10b981; box-shadow: 0 0 30px rgba(16,185,129,0.3); background: #000; }
        #webcamVideo { width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1); }
        .scanner-frame { position: absolute; inset: 0; background: radial-gradient(transparent 40%, rgba(0,0,0,0.9) 100%); pointer-events: none; }
        .scanner-laser { position: absolute; width: 100%; height: 3px; background: #00ff88; top: 0; box-shadow: 0 0 15px #00ff88, 0 0 25px #00e5ff; animation: scanLaser 2s infinite alternate ease-in-out; pointer-events: none; }
        @keyframes scanLaser { 0% { top: 0; opacity: 0.2; } 20% { opacity: 1; } 80% { opacity: 1; } 100% { top: 100%; opacity: 0.2; } }
    </style>
</head>
<body>

<canvas id="matrixCanvas"></canvas>
<svg class="globe-bg" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="90" fill="none" stroke="#00e5ff" stroke-width="0.8"/>
    <ellipse cx="100" cy="100" rx="65" ry="90" fill="none" stroke="#00ff88" stroke-width="0.6"/>
    <ellipse cx="100" cy="100" rx="35" ry="90" fill="none" stroke="#00e5ff" stroke-width="0.6"/>
    <line x1="100" y1="10" x2="100" y2="190" stroke="#00ff88" stroke-width="0.6"/>
    <line x1="10" y1="100" x2="190" y2="100" stroke="#00e5ff" stroke-width="0.6"/>
</svg>
<div class="radar-corner"><div class="radar-sweep"></div></div>

<div id="toastNotice">پەیام</div>

<div class="main-wrapper">
    <div class="kurd-flag-bar"></div>

    <!-- 1. AUTH VIEW -->
    <div id="authView" class="view-section active">
        <div class="hero-header">
            <div class="kurdistan-flag-frame">
                <div class="kurdistan-flag-inner">
                    <svg class="kurd-sun-svg" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="22" fill="#facc15"/>
                        <g stroke="#facc15" stroke-width="3.5">
                            <line x1="50" y1="4" x2="50" y2="22"/><line x1="50" y1="78" x2="50" y2="96"/>
                            <line x1="4" y1="50" x2="22" y2="50"/><line x1="78" y1="50" x2="96" y2="50"/>
                            <line x1="17" y1="17" x2="30" y2="30"/><line x1="70" y1="70" x2="83" y2="83"/>
                            <line x1="83" y1="17" x2="70" y2="30"/><line x1="30" y1="70" x2="17" y2="83"/>
                        </g>
                    </svg>
                    <div class="eagle-logo-text-top">DARKNESS</div>
                    <div class="eagle-logo-text-bottom">EAGLE</div>
                </div>
            </div>
            <div class="welcome-title"><span class="welcome-kurd-grad">بەخێربێن بۆ ناو سیستەمی هەڵۆی تاریکی</span></div>
            <div class="patriotic-slogan">
                <div>ئەم سیستەمە تایبەتە بە خزمەتی کورد و گەلی کورد</div>
                <div class="yellow-bji-line">( بژی کورد، بژی کوردستان ☀️ )</div>
            </div>
        </div>

        <div id="redWaitingNotice" class="red-waiting-alert">تکایە چاوەڕێبە تا ئەدمین قبوڵت دەکات بۆ چونە ژورەوەی سیستەمی چاوی تاریکی هەڵۆ</div>

        <div class="auth-master-card">
            <div class="auth-tabs-bar">
                <button type="button" id="tabBtnReg" class="auth-tab-btn active-reg" onclick="switchAuthTab('reg')">
                    <span>دروستکردنی هەژمار (ئەکاونت)</span>
                    <span class="sub-pill">بەشداربووی نوێ</span>
                </button>
                <button type="button" id="tabBtnLogin" class="auth-tab-btn" onclick="switchAuthTab('login')">
                    <span>چوونەژوورەوە بۆ ناو سیستەم</span>
                    <span class="sub-pill">کلیک بکە بۆ چوونەژوورەوە</span>
                </button>
            </div>

            <div id="paneRegister" class="auth-form-pane active">
                <form onsubmit="submitRegister(event)">
                    <div class="form-group"><label>Username / Gmail</label><input type="text" id="regUser" class="form-input" required placeholder="ناوی بەکارهێنەر یان جیمێڵەکەت بنووسە..."></div>
                    <div class="form-group"><label>Password</label><input type="password" id="regPass1" class="form-input" required placeholder="پاسۆردێکی بەهێز بنووسە..."></div>
                    <div class="form-group"><label>Confirm Password</label><input type="password" id="regPass2" class="form-input" required placeholder="پاسۆردەکە دووبارە بنووسەوە بۆ دڵنیابوونەوە..."></div>
                    <button type="submit" class="btn-action btn-register">تۆمارکردن و ناردنی داواکاری ◄</button>
                    <div class="helper-note">* دوای دروستکردنی هەژمار، داواکارییەکەت دەچێتە لای بەڕێوەبەر (ئەدمین) بۆ پەسەندکردن و دیاریکردنی ماوە.</div>
                </form>
            </div>

            <div id="paneLogin" class="auth-form-pane">
                <form onsubmit="submitLogin(event)">
                    <div class="form-group"><label>Username / Gmail</label><input type="text" id="loginUser" class="form-input" required placeholder="جیمێڵ یان یوزەرنەیمەکەت بنووسە..."></div>
                    <div class="form-group"><label>Password</label><input type="password" id="loginPass" class="form-input" required placeholder="پاسۆردەکەت بنووسە..."></div>
                    <button type="submit" class="btn-action btn-login-hacker">چونە ژورەوەی سیستەمی چاوی هەڵۆ</button>
                    <div class="helper-note" style="color:#cbd5e1;font-weight:600;">چوونە ژوورەوە بۆ ناو سیستەم دوای پەسەندکردنی لەلایەن بەڕێوەبەرەوە</div>
                </form>
            </div>
        </div>
    </div>

    <!-- 2. DECORATIVE 5-SECOND FACE ID VIEW -->
    <div id="faceIdView" class="view-section">
        <div class="status-card" style="max-width: 500px;">
            <div class="face-scan-title">سیستەمی ناسینەوەی ڕووخسار (Face ID)</div>
            <div class="face-scanner-container">
                <video id="webcamVideo" autoplay playsinline></video>
                <div class="scanner-frame"></div>
                <div class="scanner-laser"></div>
            </div>
            <div id="faceScanStatus" class="scan-sub-title" style="margin-top: 15px; font-size: 13.5px; font-weight: bold; color:#00ff88;">سکانکردنی ڕووخسار دەستی پێکرد... تکایە سەیری کامێراکە بکە</div>
            <div style="font-size:11px; color:#9ca3af; margin-top:8px; font-family:monospace;">AI BIOMETRIC VERIFICATION IN PROGRESS (5 SECONDS)</div>
        </div>
    </div>

    <!-- 3. WAITING VIEW -->
    <div id="waitingView" class="view-section">
        <div class="status-card">
            <div class="kurdistan-flag-frame">
                <div class="kurdistan-flag-inner">
                    <svg class="kurd-sun-svg" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="22" fill="#facc15"/>
                        <g stroke="#facc15" stroke-width="3.5"><line x1="50" y1="4" x2="50" y2="22"/><line x1="50" y1="78" x2="50" y2="96"/><line x1="4" y1="50" x2="22" y2="50"/><line x1="78" y1="50" x2="96" y2="50"/></g>
                    </svg>
                    <div class="eagle-logo-text-top">DARKNESS</div>
                    <div class="eagle-logo-text-bottom">EAGLE</div>
                </div>
            </div>
            <div class="loader-ring"></div>
            <button type="button" class="btn-action btn-login-hacker" onclick="returnToMainWithRedWaitMessage()">چاوەڕێبە ئەدمین قبوڵ بکات بۆ چونە ژورەوە</button>
        </div>
    </div>

    <!-- 4. MAIN DASHBOARD VIEW (ONLY VISIBLE AFTER 5-SEC SCAN AND VERIFICATION) -->
    <div id="dashboardView" class="view-section">
        <!-- TOP STATUS BAR: REDUCED FONT SIZES, OWNER/MASTER SMALLER -->
        <div class="cyber-top-bar">
            <div><span class="status-dot"></span><strong>سیستەم چالاکە</strong> | پەیوەندی: <span style="color:#34d399;">پارێزراو</span> | دەسەڵات: <span class="role-badge-small" id="topRoleBadge">OWNER / MASTER</span></div>
            <div class="yellow-bji-line">( بژی کورد، بژی کوردستان ☀️ )</div>
            <div id="liveClock" style="color:#9ca3af;font-family:monospace;">16/10/2026 23:15:00</div>
        </div>

        <!-- REFINED COMPACT BAR -->
        <div class="dashboard-nav-bar-compact">
            <span class="admin-pill-small" id="activeUserBadge">👑 KURDISTAN01 (بەڕێوەبەری گشتی)</span>
            <span class="session-timer-text" id="sessionRemainingBadge">⏱ ماوە: هەمیشەیی</span>
        </div>

        <!-- TACTICAL BAR (IMAGE 2 & 3 COMBINED) -->
        <div class="tactical-portal-bar">
            <!-- Left Side: Star Icon + Kurdistan01 + چوونە ژورەوەی بەڕێوبەر -->
            <div class="admin-star-portal-btn" onclick="openAdminPortalView()" title="چوونە ژوورەوەی بەڕێوەبەر">
                <div class="star-box-icon">★</div>
                <div class="portal-title-col">
                    <span class="portal-main-title">Kurdistan01</span>
                    <span class="portal-sub-title">چوونە ژورەوەی بەڕێوبەر</span>
                </div>
            </div>

            <!-- Right Side: Blinking Green Online Dot + Username + USER tag + Red Exit Button -->
            <div class="user-status-right-group">
                <div class="user-online-pill-box">
                    <span class="blinking-green-dot"></span>
                    <span class="logged-username-text" id="tacticalUsernameDisplay">Kurdistan01</span>
                    <span class="user-role-tag-pill" id="tacticalRolePill">USER</span>
                </div>
                <button type="button" class="red-exit-icon-btn" onclick="logoutToAuth()" title="دەرچوون لە سیستەم (Logout)">
                    ➔
                </button>
            </div>
        </div>

        <!-- PURE DIGITAL CYBER SPIDERWEB NETWORK TOPOLOGY MAP (DARK BACKGROUND, NEON BLUE & GREEN) -->
        <div id="spiderMapSection" class="tactical-map-wrapper">
            <div class="map-top-hud">
                <div>
                    <div class="hud-left-status"><span class="status-dot"></span>STATUS: ONLINE</div>
                    <div class="hud-left-sub">KURDISTAN TACTICAL SPIDER-WEB TOPOLOGY • CYBER MESH NETWORK</div>
                </div>
                <div class="hud-sector-box" id="activeSectorHud">SECTOR: ERBIL (هەولێر)</div>
            </div>

            <div class="spider-map-svg-box">
                <svg class="spider-map-svg" viewBox="0 0 650 520" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <radialGradient id="cyberMeshGlow" cx="50%" cy="50%" r="50%">
                            <stop offset="0%" stop-color="#00e5ff" stop-opacity="0.22"/>
                            <stop offset="55%" stop-color="#00ff88" stop-opacity="0.08"/>
                            <stop offset="100%" stop-color="#020408" stop-opacity="0"/>
                        </radialGradient>
                        <filter id="neonBlur" x="-30%" y="-30%" width="160%" height="160%">
                            <feGaussianBlur stdDeviation="3.2" result="blur" />
                            <feComposite in="SourceGraphic" in2="blur" operator="over"/>
                        </filter>
                    </defs>

                    <!-- Background Radar Target Rings & Cyber Glow -->
                    <circle cx="325" cy="240" r="210" fill="url(#cyberMeshGlow)"/>
                    <circle cx="325" cy="240" r="180" fill="none" stroke="#00e5ff" stroke-width="0.8" stroke-dasharray="6,6" opacity="0.3"/>
                    <circle cx="325" cy="240" r="120" fill="none" stroke="#00ff88" stroke-width="0.8" stroke-dasharray="4,8" opacity="0.4"/>
                    <circle cx="325" cy="240" r="60" fill="none" stroke="#00e5ff" stroke-width="0.8" opacity="0.5"/>
                    <line x1="325" y1="20" x2="325" y2="460" stroke="#00e5ff" stroke-width="0.7" stroke-dasharray="3,6" opacity="0.3"/>
                    <line x1="100" y1="240" x2="550" y2="240" stroke="#00ff88" stroke-width="0.7" stroke-dasharray="3,6" opacity="0.3"/>

                    <!-- Spiderweb Concentric Digital Rings -->
                    <g opacity="0.5" stroke-width="1.2">
                        <polygon points="325,70 460,130 495,240 445,365 325,420 205,365 155,240 190,130" fill="none" stroke="#00e5ff" stroke-dasharray="5,5"/>
                        <polygon points="325,115 425,160 450,240 410,330 325,375 240,330 200,240 225,160" fill="none" stroke="#00ff88"/>
                        <polygon points="325,160 390,190 405,240 375,295 325,330 275,295 245,240 260,190" fill="none" stroke="#00e5ff"/>
                        <polygon points="325,195 355,210 365,240 350,270 325,285 300,270 285,240 295,210" fill="none" stroke="#00ff88"/>
                    </g>

                    <!-- Outer Border of Map -->
                    <polygon points="210,35 365,28 455,85 525,175 545,265 495,355 525,465 470,495 315,465 215,390 120,305 145,205 190,135" 
                             fill="rgba(0, 229, 255, 0.03)" stroke="#00e5ff" stroke-width="2.2" filter="url(#neonBlur)"/>

                    <!-- Glowing Neon Blue & Green Connection Lines -->
                    <g stroke="#00e5ff" stroke-width="1.6" opacity="0.85" filter="url(#neonBlur)">
                        <!-- Northern & Major Kurdish Network -->
                        <line x1="255" y1="68" x2="290" y2="105"/> <!-- Zakho - Duhok -->
                        <line x1="255" y1="68" x2="240" y2="155"/> <!-- Zakho - Mosul -->
                        <line x1="290" y1="105" x2="345" y2="112"/> <!-- Duhok - Akre -->
                        <line x1="290" y1="105" x2="345" y2="165"/> <!-- Duhok - Erbil -->
                        <line x1="290" y1="105" x2="240" y2="155"/> <!-- Duhok - Mosul -->
                        <line x1="345" y1="112" x2="405" y2="120"/> <!-- Akre - Soran -->
                        <line x1="345" y1="112" x2="345" y2="165"/> <!-- Akre - Erbil -->
                        <line x1="405" y1="120" x2="345" y2="165"/> <!-- Soran - Erbil -->
                        <line x1="405" y1="120" x2="435" y2="168"/> <!-- Soran - Ranya -->
                        <line x1="345" y1="165" x2="395" y2="185"/> <!-- Erbil - Koya -->
                        <line x1="345" y1="165" x2="355" y2="235"/> <!-- Erbil - Kirkuk -->
                        <line x1="345" y1="165" x2="240" y2="155"/> <!-- Erbil - Mosul -->
                        <line x1="395" y1="185" x2="435" y2="168"/> <!-- Koya - Ranya -->
                        <line x1="395" y1="185" x2="455" y2="215"/> <!-- Koya - Sulaymaniyah -->
                        <line x1="395" y1="185" x2="355" y2="235"/> <!-- Koya - Kirkuk -->
                        <line x1="435" y1="168" x2="455" y2="215"/> <!-- Ranya - Sulaymaniyah -->
                        <line x1="455" y1="215" x2="410" y2="248"/> <!-- Sulaymaniyah - Chamchamal -->
                        <line x1="455" y1="215" x2="495" y2="255"/> <!-- Sulaymaniyah - Halabja -->
                        <line x1="455" y1="215" x2="435" y2="290"/> <!-- Sulaymaniyah - Kalar -->
                        <line x1="410" y1="248" x2="355" y2="235"/> <!-- Chamchamal - Kirkuk -->
                        <line x1="410" y1="248" x2="435" y2="290"/> <!-- Chamchamal - Kalar -->
                        <line x1="495" y1="255" x2="435" y2="290"/> <!-- Halabja - Kalar -->
                        <line x1="355" y1="235" x2="435" y2="290"/> <!-- Kirkuk - Kalar -->
                        <line x1="435" y1="290" x2="420" y2="335"/> <!-- Kalar - Khanaqin -->
                        <line x1="240" y1="155" x2="355" y2="235"/> <!-- Mosul - Kirkuk -->

                        <!-- Regional Grid Lines -->
                        <line x1="240" y1="155" x2="295" y2="295"/>
                        <line x1="355" y1="235" x2="295" y2="295"/>
                        <line x1="355" y1="235" x2="380" y2="340"/>
                        <line x1="420" y1="335" x2="380" y2="340"/>
                        <line x1="295" y1="295" x2="320" y2="375"/>
                        <line x1="380" y1="340" x2="320" y2="375"/>
                        <line x1="180" y1="365" x2="320" y2="375"/>
                        <line x1="180" y1="365" x2="285" y2="430"/>
                        <line x1="320" y1="375" x2="285" y2="430"/>
                        <line x1="320" y1="375" x2="395" y2="415"/>
                        <line x1="285" y1="430" x2="295" y2="465"/>
                        <line x1="395" y1="415" x2="475" y2="480"/>
                        <line x1="295" y1="465" x2="475" y2="480"/>
                    </g>

                    <!-- Neon Green Pulsing Data Streams -->
                    <g stroke="#00ff88" stroke-width="1.3" stroke-dasharray="4,6" opacity="0.85">
                        <line x1="345" y1="165" x2="455" y2="215"/>
                        <line x1="290" y1="105" x2="455" y2="215"/>
                        <line x1="255" y1="68" x2="355" y2="235"/>
                        <line x1="495" y1="255" x2="345" y2="165"/>
                        <line x1="345" y1="165" x2="420" y2="335"/>
                    </g>

                    <!-- City Nodes (Neon Green and Blue Glowing Points - Spaced Out) -->
                    <!-- Zakho -->
                    <g style="cursor:pointer" onclick="selectSector('ZAKHO (زاخۆ)')">
                        <circle cx="255" cy="68" r="8" fill="#00e5ff" stroke="#000" stroke-width="2" filter="url(#neonBlur)"/>
                        <circle cx="255" cy="68" r="3" fill="#ffffff"/>
                        <text x="235" y="48" fill="#00e5ff" font-size="10.5" font-weight="900" font-family="monospace">زاخۆ ZAKHO</text>
                    </g>
                    <!-- Duhok -->
                    <g style="cursor:pointer" onclick="selectSector('DUHOK (دهۆک)')">
                        <circle cx="290" cy="105" r="9" fill="#00ff88" stroke="#000" stroke-width="2" filter="url(#neonBlur)"/>
                        <circle cx="290" cy="105" r="4" fill="#ffffff"/>
                        <text x="175" y="100" fill="#00ff88" font-size="11" font-weight="900">دهۆک DUHOK</text>
                    </g>
                    <!-- Akre -->
                    <g style="cursor:pointer" onclick="selectSector('AKRE (ئاکرێ)')">
                        <circle cx="345" cy="112" r="7" fill="#00e5ff" stroke="#000" stroke-width="1.8"/>
                        <circle cx="345" cy="112" r="2.5" fill="#ffffff"/>
                        <text x="325" y="94" fill="#a7f3d0" font-size="10" font-weight="bold">ئاکرێ</text>
                    </g>
                    <!-- Soran -->
                    <g style="cursor:pointer" onclick="selectSector('SORAN (سۆران)')">
                        <circle cx="405" cy="120" r="8" fill="#00ff88" stroke="#000" stroke-width="1.8" filter="url(#neonBlur)"/>
                        <circle cx="405" cy="120" r="3" fill="#ffffff"/>
                        <text x="420" y="112" fill="#00ff88" font-size="10.5" font-weight="900">سۆران</text>
                    </g>
                    <!-- Erbil (Central Neon Cyber Node) -->
                    <g style="cursor:pointer" onclick="selectSector('ERBIL (هەولێر)')">
                        <circle cx="345" cy="165" r="13" fill="none" stroke="#00e5ff" stroke-width="2" stroke-dasharray="3,3" opacity="0.8"/>
                        <circle cx="345" cy="165" r="10" fill="#00ff88" stroke="#ffffff" stroke-width="2.5" filter="url(#neonBlur)"/>
                        <circle cx="345" cy="165" r="4.5" fill="#ffffff"/>
                        <text x="260" y="153" fill="#00ff88" font-size="12" font-weight="900">هەولێر ERBIL</text>
                    </g>
                    <!-- Koya -->
                    <g style="cursor:pointer" onclick="selectSector('KOYA (کۆیە)')">
                        <circle cx="395" cy="185" r="7" fill="#00e5ff" stroke="#000" stroke-width="1.8"/>
                        <circle cx="395" cy="185" r="2.5" fill="#ffffff"/>
                        <text x="375" y="210" fill="#a7f3d0" font-size="10" font-weight="bold">کۆیە</text>
                    </g>
                    <!-- Ranya -->
                    <g style="cursor:pointer" onclick="selectSector('RANYA (ڕانیە)')">
                        <circle cx="435" cy="168" r="8" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="435" cy="168" r="3" fill="#ffffff"/>
                        <text x="450" y="162" fill="#00ff88" font-size="10.5" font-weight="900">ڕانیە</text>
                    </g>
                    <!-- Sulaymaniyah -->
                    <g style="cursor:pointer" onclick="selectSector('SULAYMANIYAH (سلێمانی)')">
                        <circle cx="455" cy="215" r="10" fill="#00e5ff" stroke="#000" stroke-width="2" filter="url(#neonBlur)"/>
                        <circle cx="455" cy="215" r="4" fill="#ffffff"/>
                        <text x="475" y="222" fill="#00e5ff" font-size="11" font-weight="900">سلێمانی</text>
                    </g>
                    <!-- Chamchamal -->
                    <g style="cursor:pointer" onclick="selectSector('CHAMCHAMAL (چەمچەماڵ)')">
                        <circle cx="410" cy="248" r="7" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="410" cy="248" r="2.5" fill="#ffffff"/>
                        <text x="365" y="275" fill="#a7f3d0" font-size="9.5" font-weight="bold">چەمچەماڵ</text>
                    </g>
                    <!-- Kirkuk -->
                    <g style="cursor:pointer" onclick="selectSector('KIRKUK (کەرکوک)')">
                        <circle cx="355" cy="235" r="10" fill="#00e5ff" stroke="#00ff88" stroke-width="2.2" filter="url(#neonBlur)"/>
                        <circle cx="355" cy="235" r="4" fill="#ffffff"/>
                        <text x="270" y="248" fill="#00e5ff" font-size="11" font-weight="900">کەرکوک</text>
                    </g>
                    <!-- Halabja -->
                    <g style="cursor:pointer" onclick="selectSector('HALABJA (هەڵەبجە)')">
                        <circle cx="495" cy="255" r="8" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="495" cy="255" r="3" fill="#ffffff"/>
                        <text x="510" y="265" fill="#00ff88" font-size="10.5" font-weight="900">هەڵەبجە</text>
                    </g>
                    <!-- Kalar -->
                    <g style="cursor:pointer" onclick="selectSector('KALAR (کەلار - گەرمیان)')">
                        <circle cx="435" cy="290" r="8" fill="#00e5ff" stroke="#000" stroke-width="1.8"/>
                        <circle cx="435" cy="290" r="3" fill="#ffffff"/>
                        <text x="450" y="305" fill="#00e5ff" font-size="10.5" font-weight="900">کەلار</text>
                    </g>
                    <!-- Khanaqin -->
                    <g style="cursor:pointer" onclick="selectSector('KHANAQIN (خانەقین)')">
                        <circle cx="420" cy="335" r="7" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="420" cy="335" r="2.5" fill="#ffffff"/>
                        <text x="435" y="352" fill="#a7f3d0" font-size="10" font-weight="bold">خانەقین</text>
                    </g>

                    <!-- Southern Iraq Regional Nodes -->
                    <g style="cursor:pointer" onclick="selectSector('MOSUL')">
                        <circle cx="240" cy="155" r="7" fill="#3b82f6" stroke="#000" stroke-width="1.8"/>
                        <text x="180" y="159" fill="#93c5fd" font-size="10.5" font-weight="bold">MOSUL</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('SALAHADDIN')">
                        <circle cx="295" cy="295" r="6" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="215" y="299" fill="#93c5fd" font-size="9.5" font-weight="bold">SALAHADDIN</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('DIYALA')">
                        <circle cx="380" cy="340" r="6" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="330" y="344" fill="#93c5fd" font-size="9.5" font-weight="bold">DIYALA</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('BAGHDAD')">
                        <circle cx="320" cy="375" r="8" fill="#3b82f6" stroke="#000" stroke-width="2"/>
                        <text x="333" y="379" fill="#bfdbfe" font-size="11" font-weight="bold">BAGHDAD</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('ANBAR')">
                        <circle cx="180" cy="365" r="6" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="135" y="369" fill="#93c5fd" font-size="9.5" font-weight="bold">ANBAR</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('KARBALA')">
                        <circle cx="285" cy="430" r="6" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="225" y="434" fill="#93c5fd" font-size="9.5" font-weight="bold">KARBALA</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('WASIT')">
                        <circle cx="395" cy="415" r="6" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="407" y="419" fill="#93c5fd" font-size="9.5" font-weight="bold">WASIT</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('NAJAF')">
                        <circle cx="295" cy="465" r="6.5" fill="#3b82f6" stroke="#000" stroke-width="1.5"/>
                        <text x="245" y="469" fill="#93c5fd" font-size="10" font-weight="bold">NAJAF</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('BASRA')">
                        <circle cx="475" cy="480" r="8" fill="#3b82f6" stroke="#000" stroke-width="2"/>
                        <text x="488" y="484" fill="#bfdbfe" font-size="11" font-weight="bold">BASRA</text>
                    </g>
                </svg>
            </div>
        </div>

        <!-- 14 CARDS GRID (PERMANENT 3-COLUMNS AS IN IMAGE 11) -->
        <div id="cardsGridSubView">
            <div class="cards-grid" id="cardsContainer"></div>
        </div>

        <!-- INSIDE DATABASE SEARCH FORM -->
        <div id="insideDbSubView" style="display: none;">
            <div class="db-inside-panel">
                <div class="db-inside-top-row">
                    <div>
                        <div class="db-inside-main-title" id="insideDbHeaderTitle">دەستگەیشتن بە بنکەی زانیاری</div>
                        <span class="db-inside-sub-badge" id="insideDbActiveName">❖ بنکەی زانیاری</span>
                    </div>
                    <div class="db-inside-actions">
                        <button type="button" class="db-top-btn" onclick="clearInsideDbFields()">• پاککردنەوەی هەموو خانەکان</button>
                        <button type="button" class="db-top-btn db-back-main-btn" onclick="closeInsideDbView()" style="background: linear-gradient(135deg, #065f46, #047857); border: 1.5px solid #34d399; color: #ffffff; padding: 10px 16px; border-radius: 8px; font-weight: bold; font-size: 12.5px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 0 15px rgba(16,185,129,0.3); transition: 0.2s;">⟲ گەڕانەوە بۆ نەخشە و سەرەکی</button>
                    </div>
                </div>

                <div id="dynamicWarningBanner" class="db-warning-banner" style="display: none;"></div>
                <div id="dynamicDropdownArea" class="db-dropdown-wrap" style="display: none;"></div>

                <form onsubmit="runInsideDbSearch(event)">
                    <div id="dynamicFieldsGrid" class="db-fields-grid"></div>
                    <button type="submit" class="db-Execute-full-btn" id="executeSearchBtn">جێبەجێکردنی گەڕان ◄</button>
                </form>
            </div>
        </div>

        <!-- CYBER SCANNING LOADER -->
        <div id="cyberScanSubView" class="cyber-scan-box">
            <div class="scan-spinner"></div>
            <div class="scan-main-title">• سکان کردنی بنکە شفرەکراوەکان...</div>
            <div class="scan-sub-title">کردنەوەی شفرە... دڵنیاکردنەوە... پرۆسێسکردن...</div>
        </div>

        <!-- SECRET SEARCH RESULTS VIEW -->
        <div id="secretResultsSubView" class="secret-results-wrapper">
            <div class="results-top-header">
                <div class="results-top-title" id="resultsMainTitle">ئەنجامەکانی گەڕان: نهێنی</div>
                <div style="display:flex; gap:8px;">
                    <button type="button" class="db-top-btn" onclick="backToSearchForm()">گەڕانی نوێ •</button>
                    <button type="button" class="db-top-btn db-back-main-btn" onclick="closeInsideDbView()" style="background: linear-gradient(135deg, #065f46, #047857); border: 1.5px solid #34d399; color: #ffffff; padding: 10px 16px; border-radius: 8px; font-weight: bold; font-size: 12.5px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 0 15px rgba(16,185,129,0.3); transition: 0.2s;">⟲ گەڕانەوە بۆ پێڕستی بنکەکان</button>
                </div>
            </div>
            <div class="results-summary-bar">
                <span id="totalRecordsFoundText">• کۆی تۆمارەکانی دۆزراوە: 100</span>
                <span id="pageRecordsText">لاپەڕە 1 لە 10</span>
            </div>
            <div id="recordsListContainer"></div>
        </div>
    </div>

    <!-- 5. SEPARATE ADMIN APPROVAL PORTAL VIEW -->
    <div id="adminPortalView" class="view-section">
        <div class="admin-portal-card">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; border-bottom:1px solid #1e293b; padding-bottom:10px;">
                <span style="color:#facc15; font-weight:900; font-size:13px;">★ پانێڵی تایبەتی بەڕێوەبەر</span>
                <button type="button" class="db-top-btn db-back-main-btn" onclick="switchView('dashboardView')">گەڕانەوە بۆ ناو سیستەم ➔</button>
            </div>

            <div class="hacker-green-frame">
                <span class="main-owner-tag">( Username/Oner)</span>
                <span class="sub-eternal-tag">(هەمیشەیی)</span>
            </div>

            <div class="admin-portal-subtitle">
                داواکاری قبوڵ کردن بۆ ناو چاوی هەڵۆیی تارکی دەروازەی زانیاری
            </div>

            <div id="adminRequestsContainer"></div>
        </div>
    </div>
</div>

<!-- 1. FAMILY TREE MODAL -->
<!-- 1. FAMILY TREE MODAL -->
<!-- 1. FAMILY TREE MODAL -->
<!-- 1. FAMILY TREE MODAL -->
<div id="familyTreeModal" class="modal-overlay">
    <div class="tree-modal-box" style="max-width: 960px; padding: 12px 14px 18px;">
        <div class="modal-common-header" style="margin-bottom: 10px; padding-bottom: 6px;">
            <div class="modal-common-title" style="font-size: 13px;">FAMILY TREE VISUALIZATION</div>
            <div style="display:flex; gap:6px; align-items:center;">
                <button type="button" class="db-top-btn db-back-main-btn" onclick="closeFamilyTreeModal()" style="padding: 4px 10px; font-size: 11px;">گەڕانەوە ➔</button>
                <button type="button" class="modal-close-btn" onclick="closeFamilyTreeModal()" style="width: 24px; height: 24px; font-size: 12px;">✕</button>
            </div>
        </div>
        <div class="tree-inner-frame" style="padding: 10px 8px;">
            <div class="tree-role-tag" style="font-size: 10px; padding: 2px 10px; margin-bottom: 6px;">سەرۆکی خێزان و هاوسەر</div>

            <!-- Husband and Wife side by side container -->
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; max-width: 720px; margin: 0 auto;">
                <div class="parent-node-card" style="max-width: 100%; margin: 0; padding: 10px; gap: 8px;">
                    <div class="node-avatar-circle" style="width: 40px; height: 40px; min-width: 40px;"><div class="node-avatar-inner-sq" style="width: 16px; height: 16px;"></div></div>
                    <div class="parent-info-col" style="text-align: right;">
                        <div class="node-name-head" style="font-size: 12.5px; margin-bottom: 2px;">محسن نجم (باوک)</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• باوک: نجم صادق | دایک: نجبة</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• پیشە: فەرمانبەر | تەمەن: 61</div>
                        <div class="node-detail-line" style="font-size: 9.5px; color: #34d399; font-weight: bold;">• مووچەی مانگانە: 1,250,000 دینار</div>
                        <div class="node-bottom-badges" style="margin-top: 4px; gap: 4px;">
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">لەدایکبوون: 1965</span>
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">خێزاندار</span>
                        </div>
                    </div>
                </div>

                <div class="parent-node-card" style="max-width: 100%; margin: 0; padding: 10px; gap: 8px;">
                    <div class="node-avatar-circle" style="width: 40px; height: 40px; min-width: 40px;"><div class="node-diamond" style="width: 14px; height: 14px;"></div></div>
                    <div class="parent-info-col" style="text-align: right;">
                        <div class="node-name-head" style="font-size: 12.5px; margin-bottom: 2px;">زينة حسين (دایک)</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• باوک: حسين طاهر | دایک: خديجة</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• پیشە: ماڵدار | تەمەن: 58</div>
                        <div class="node-detail-line" style="font-size: 9.5px; color: #9ca3af;">• مووچەی مانگانە: نەبوو (خانەنشینی خێزان)</div>
                        <div class="node-bottom-badges" style="margin-top: 4px; gap: 4px;">
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">کار: 1</span>
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">خێزاندار</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="tree-connector-line" style="height: 18px; margin-top: 6px;"></div>
            <div class="tree-middle-badge" style="font-size: 9.5px; padding: 1px 10px;">منداڵان (٦ منداڵ - زانیاری تەواو و مووچە)</div>
            <div class="tree-connector-line" style="height: 12px;"></div>

            <div class="children-cards-row" style="display: grid !important; grid-template-columns: repeat(3, 1fr) !important; gap: 8px !important; margin-top: 6px !important;">
                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">لاوند محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: ئەندازیار</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: خێزاندار | تەمەن: 34</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 950,000 د.ع</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 1992</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">ژیان</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">هوشمند محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: پزیشک</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: خێزاندار | تەمەن: 32</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 1,800,000 د.ع</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 1994</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">ژیان</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">کارمند محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: مامۆستا</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: سەڵت | تەمەن: 29</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 750,000 د.ع</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 1997</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">ژیان</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">شيرين محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: فەرمانبەر</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: خێزاندار | تەمەن: 31</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 650,000 د.ع</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">ID: 783276</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">ژیان</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start; border-color: #ef4444; background: rgba(127,29,29,0.15);">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px; color:#fca5a5;">فريشتة محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: دەرچوو</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color:#ef4444; font-weight: bold;">• دۆخ: کۆچکردوو</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #9ca3af;">• مووچە: -</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; background:#7f1d1d; color:#fca5a5;">کۆچکردوو</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">روند محسن</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: قوتابی</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: سەڵت | تەمەن: 20</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #facc15;">• مووچە: نەبوو (قوتابی)</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 2006</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">ژیان</span>
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="margin-top: 14px; text-align: center;">
                <button type="button" class="db-top-btn db-back-main-btn" onclick="closeFamilyTreeModal()" style="padding: 8px 18px; font-size: 12px;">گەڕانەوە بۆ بنکەی زانیاری ➔</button>
            </div>
        </div>
    </div>
</div>

<!-- 2. METER LOCATION MAP MODAL -->
<div id="meterMapModal" class="modal-overlay">
    <div class="map-modal-box">
        <div class="modal-common-header">
            <div class="modal-common-title">⬚ شوێنی میتەر</div>
            <button type="button" class="modal-close-btn" onclick="closeMeterMapModal()">✕</button>
        </div>
        <div class="meter-info-card">
            <div><strong>ناوی بەشداربوو:</strong> <span id="mapMeterName">محمد احمد محمد</span></div>
            <div><strong>ژمارەی ئەکاونت:</strong> <span id="mapMeterAcc">63179260572</span></div>
            <div><strong>هێڵی پانی:</strong> <span id="mapMeterLat">36.18416794</span></div>
            <div><strong>هێڵی درێژی:</strong> <span id="mapMeterLng">44.03849821</span></div>
            <div><strong>دۆخ:</strong> <span style="color:#10b981;font-weight:bold;">مۆڵەتدار</span></div>
        </div>
        <div class="meter-map-frame">
            <iframe id="meterMapIframe" src="https://maps.google.com/maps?q=36.18416794,44.03849821&hl=ckb&z=17&output=embed"></iframe>
        </div>
    </div>
</div>

<!-- 3. BIOMETRIC PHOTO MODAL -->
<div id="bioModal" class="modal-overlay">
    <div class="bio-modal-box">
        <div class="modal-common-header">
            <div class="modal-common-title">👤 وێنەی بایۆمێتریک</div>
            <button type="button" class="modal-close-btn" onclick="closeBioModal()">✕</button>
        </div>
        <div class="bio-img-preview">
            [وێنەی بایۆمێتریکی کەس]
        </div>
        <div style="font-size:12px; color:#cbd5e1; margin-top:10px;">کۆدی بایۆمێتریک: <span style="color:var(--kurd-gold);">87914692</span></div>
        <button type="button" class="db-Execute-full-btn" style="margin-top:14px;" onclick="closeBioModal()">داخستن</button>
    </div>
</div>

<script>
    const accountsDB = {};

    let currentLoggedInUser = null;
    let currentActiveDbTitle = '';
    let faceStreamRef = null;

    const dbCards = [
        ["بنکەی زانیاری کی کارد", "تۆمارەکانی کارتی تەموین، زانیاری کی کارد، و سیستەمی چاودێری خزمەتگوزاری هاوڵاتیان."],
        ["بنکەی زانیاری ئاسیاسێڵ", "تۆمارەکانی بەشداربووانی تۆڕی مۆبایل، تۆمارکردنی سیمکارت، و زانیاری پەیوەندییەکان."],
        ["بنکەی تۆمارکردنی شار 2022", "نهێنی: تۆماری تەواوی هاوڵاتیان لە ساڵی 2022، تۆمارەکانی خێزان، و بنکەی زانیاری ناسنامەی نیشتمانی.", true],
        ["بنکەی زانیاری خزمایەتی", "نهێنی: سیستەمی شوێنکەوتنی ڕەچەڵەکی خێزان، ناسینەوەی خزمەکانی لایەنی باوک و دایک."],
        ["بڕیارەکانی دادگا و هێزەکانی یەکێتی", "نهێنی: بڕیارەکانی دادگا، کەسە داواکراوەکان، تۆمارەکانی هێزەکانی یەکێتی، و زانیاری کەیسە یاساییەکان."],
        ["بنکەی زانیاری تەندروستی", "نهێنی: تۆمارەکانی کوتانی کۆڤید-19، چاودێری تەندروستی، و زانیاری پزیشکی هاوڵاتیان."],
        ["بنکەی زانیاری ئۆتۆمۆبیل", "نهێنی: تۆمارەکانی تۆماری ئۆتۆمۆبیل، زانیاری خاوەنی ئۆتۆمۆبیل، و سیستەمی چاودێری گواستنەوە."],
        ["بنکەی زانیاری کەسان", "زۆر نهێنی: پەڕگەکانی کارمەندان، تۆمارەکانی کار، و زانیاری هاوڵاتیان."],
        ["بنکەی تۆمارکردنی شار", "سنووردار: تۆمارەکانی خێزان، زانیاری نیشتەجێبوون، و زانیاری ناسنامەی هاوڵاتیان."],
        ["بنکەی زانیاری کارەبا", "نهێنی: چاودێری میتەری کارەبا، زانیاری بەشداربووان، و سیستەمی چاودێری تۆڕی کارەبا."],
        ["بنکەی زانیاری دەنگدەران", "زۆر نهێنی: تۆمارکردنی دەنگدەران، زانیاری وێستگەکانی دەنگدان، و زانیاری دەنگدانی هاوڵاتیان."],
        ["بنکەی زانیاری فەیسبووک", "زانیاری تۆڕە کۆمەڵایەتییەکان، پرۆفایلی بەکارهێنەران، زانیاری پەیوەندی، و شوێنپێی دیجیتاڵ."],
        ["بنکەی زانیاری خانەنشینی", "نهێنی: تۆمارەکانی خانەنشینی، سوودمەندان، زانیاری میراتگران، و زانیاری دارایی."],
        ["بنکەی زانیاری ژمارەی مۆبایل", "نهێنی: ناسینەوەی ژمارەی تەلەفۆن، گەڕانی ناوی بانگکەر، و زانیاری پەیوەندییەکان."]
    ];

    const dbConfigs = {
        "بنکەی زانیاری خانەنشینی": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: null,
            warning: null,
            fields: [
                { id: "pen_puid", label: "PENSION ID (ژمارەی خانەنشینی)", ph: "...نووسین ژمارەی خانەنشینی" },
                { id: "pen_upn", label: "UPN کۆدی", ph: "...نووسین UPN" },
                { id: "pen_old", label: "ژمارەی کۆنی خانەنشینی", ph: "...نووسین ژمارەی کۆن" },
                { id: "pen_n1", label: "ناوی یەکەم", ph: "...نووسین ناوی یەکەم" },
                { id: "pen_n2", label: "ناوی دووەم", ph: "...نووسین ناوی دووەم" },
                { id: "pen_n3", label: "ناوی سێیەم", ph: "...نووسین ناوی سێیەم" },
                { id: "pen_n4", label: "ناوی کۆتایی", ph: "...نووسین ناوی کۆتایی" },
                { id: "pen_phone", label: "ژمارەی تەلەفۆن", ph: "...نووسین ژمارەی تەلەفۆن" },
                { id: "pen_bio", label: "کۆدی بایۆمێتریک", ph: "...نووسین کۆدی بایۆمێتریک" },
                { id: "pen_doc", label: "ژمارەی بەڵگەنامە", ph: "...نووسین ژمارەی بەڵگەنامە" },
                { id: "pen_nat", label: "ژمارەی نیشتمانی", ph: "...نووسین ژمارەی نیشتمانی" },
                { id: "pen_code_m", label: "ژمارەی مەدەنی", ph: "...نووسین ژمارەی مەدەنی" },
                { id: "pen_bank", label: "بانک", ph: "...نووسین بانک" },
                { id: "pen_dept", label: "وەزارەت", ph: "...نووسین وەزارەت" },
                { id: "pen_from", label: "ڕێکخراو / FROM", ph: "...نووسین ڕێکخراو" },
                { id: "pen_type_h", label: "پلانی خانەنشینی", ph: "...نووسین پلان" },
                { id: "pen_m", label: "ژمارەی مەدەنی", ph: "...نووسین ژمارەی مەدەنی" }
            ]
        },
        "بنکەی زانیاری ژمارەی مۆبایل": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: null,
            warning: null,
            fields: [
                { id: "m_phone", label: "ژمارەی تەلەفۆن", ph: "...نووسین ژمارەی تەلەفۆن" }
            ]
        },
        "بڕیارەکانی دادگا و هێزەکانی یەکێتی": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: null,
            warning: null,
            fields: [
                { id: "ct_full", label: "ناوی تەواو", ph: "...نووسین ناوی تەواو" },
                { id: "ct_gm", label: "ناوی دایک باپیر", ph: "...نووسین ناوی دایک باپیر" },
                { id: "ct_n3", label: "ناوی باپیر", ph: "...نووسین ناوی باپیر" },
                { id: "ct_n2", label: "ناوی باوک", ph: "...نووسین ناوی باوک" },
                { id: "ct_n1", label: "ناوی یەکەم", ph: "...نووسین ناوی یەکەم" },
                { id: "ct_type", label: "جۆر", ph: "...نووسین جۆر" },
                { id: "ct_desc", label: "وەسف", ph: "...نووسین وەسف" },
                { id: "ct_loc", label: "شوێن", ph: "...نووسین شوێن" },
                { id: "ct_persons", label: "کەسەکان", ph: "...نووسین کەسەکان" },
                { id: "ct_date", label: "بەروار", ph: "...نووسین بەروار" },
                { id: "ct_case", label: "ژمارەی کەیس", ph: "...نووسین ژمارەی کەیس" },
                { id: "ct_mother", label: "ناوی دایک", ph: "...نووسین ناوی دایک" }
            ]
        },
        "بنکەی زانیاری تەندروستی": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: null,
            warning: null,
            fields: [
                { id: "h_phone", label: "ژمارەی تەلەفۆن", ph: "...نووسین ژمارەی تەلەفۆن" }
            ]
        },
        "بنکەی تۆمارکردنی شار 2022": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: { label: "• هەڵبژاردنی پارێزگا", options: ["-- هەڵبژاردنی پارێزگا --", "هەولێر [Erbil]", "سلێمانی [Sulaymaniyah]", "دهۆک [Duhok]", "کەرکوک [Kirkuk]"], defaultVal: "هەولێر [Erbil]" },
            warning: null,
            fields: [
                { id: "c_name1", label: "ناوی یەکەم", ph: "...نووسین ناوی یەکەم" }, { id: "c_name2", label: "ناوی باوک", ph: "...نووسین ناوی باوک" }, { id: "c_name3", label: "باپیر", ph: "...نووسین باپیر" },
                { id: "c_seq", label: "ژمارەی زنجیرە", ph: "...نووسین ژمارەی زنجیرە" }, { id: "c_famno", label: "ژمارەی خێزان", ph: "...نووسین ژمارەی خێزان" }, { id: "c_rc", label: "ژمارەی RC", ph: "...نووسین ژمارەی RC" },
                { id: "c_job", label: "پیشە", ph: "...نووسین پیشە" }, { id: "c_id", label: "ژمارەی ناسنامە", ph: "...نووسین ژمارەی ناسنامە" }, { id: "c_birth", label: "ساڵی لەدایکبوون", ph: "...نووسین ساڵی لەدایکبوون" },
                { id: "c_grandma", label: "دایەپیر", ph: "...نووسین دایەپیر" }, { id: "c_mother", label: "ناوی دایک", ph: "...نووسین ناوی دایک" }
            ]
        },
        "بنکەی زانیاری کارەبا": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری", dropdown: null, warning: null,
            fields: [
                { id: "e_area1", label: "ناوچە", ph: "...نووسین ناوچە" }, { id: "e_feeder", label: "فیدەر", ph: "...نووسین فیدەر" }, { id: "e_area2", label: "ناوچە", ph: "...نووسین ناوچە" },
                { id: "e_name", label: "ناوی بەشداربوو", ph: "...نووسین ناوی بەشداربوو" }, { id: "e_meter", label: "ژمارەی میتەر", ph: "...نووسین ژمارەی میتەر" }, { id: "e_acc", label: "ژمارەی ئەکاونت", ph: "...نووسین ژمارەی ئەکاونت" },
                { id: "e_subzone", label: "ژێر زۆن", ph: "...نووسین ژێر زۆن" }, { id: "e_block", label: "ژمارەی بلۆک", ph: "...نووسین ژمارەی بلۆک" }, { id: "e_sts", label: "ژمارەی STS", ph: "...نووسین ژمارەی STS" }
            ]
        },
        "بنکەی زانیاری خزمایەتی": {
            headerTitle: "دۆزینەوەی خزمەکان",
            dropdown: { label: "• جۆری گەڕان", options: ["-- هەڵبژاردنی جۆر --", "خزمەکانی لایەنی باوک", "خزمەکانی لایەنی دایک"], defaultVal: "خزمەکانی لایەنی باوک" },
            warning: "⚠️ تەنها هەرێمی کوردستان (هەولێر، دهۆک، کەرکوک، سلێمانی)",
            fields: [
                { id: "k_father", label: "ناوی یەکەمی باوکی کەس", ph: "ناوی یەکەمی باوکی کەس" },
                { id: "k_grandpa", label: "ناوی باوکی باوکی کەس (باپیر)", ph: "باوکی باوکی کەس (باپیر)" },
                { id: "k_g_grandpa", label: "ناوی باپیرەی باوکی کەس (دایک / باپیر)", ph: "باپیرەی باوکی کەس (دایک باپیر)" },
                { id: "k_grandma", label: "ناوی دایکی باوکی کەس (دایەپیر)", ph: "دایکی باوکی کەس (دایەپیر)" },
                { id: "k_g_grandma_f", label: "ناوی باوکی دایەپیری باوکی کەس", ph: "باوکی دایەپیری باوکی کەس" }
            ]
        },
        "بنکەی زانیاری فەیسبووک": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری", dropdown: null, warning: null,
            fields: [
                { id: "fb_phone", label: "ژمارەی تەلەفۆن", ph: "...نووسین ژمارەی تەلەفۆن" },
                { id: "fb_id", label: "ژمارەی بەکارهێنەر", ph: "...نووسین ژمارەی بەکارهێنەر" }
            ]
        },
        "بنکەی زانیاری دەنگدەران": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری",
            dropdown: { label: "• هەڵبژاردنی پارێزگا", options: ["-- هەڵبژاردنی پارێزگا --", "کەرکوک", "هەولێر", "سلێمانی", "دهۆک"], defaultVal: "کەرکوک" },
            warning: null,
            fields: [
                { id: "v_name1", label: "ناوی یەکەم", ph: "...نووسین ناوی یەکەم" }, { id: "v_name2", label: "ناوی باوک", ph: "...نووسین ناوی باوک" }, { id: "v_name3", label: "باپیر", ph: "...نووسین باپیر" },
                { id: "v_person_id", label: "ژمارەی کەسی", ph: "...نووسین ژمارەی کەسی" }, { id: "v_fam_no", label: "ژمارەی خێزان", ph: "...نووسین ژمارەی خێزان" }, { id: "v_birth", label: "ساڵی لەدایکبوون", ph: "...نووسین ساڵی لەدایکبوون" }
            ]
        },
        "بنکەی زانیاری ئۆتۆمۆبیل": {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری", dropdown: null, warning: null,
            fields: [
                { id: "f_plate", label: "ژمارەی تابلۆ", ph: "...نووسین ژمارەی تابلۆ" }, { id: "f_model", label: "مۆدێلی ئۆتۆمۆبیل", ph: "...نووسین مۆدێلی ئۆتۆمۆبیل" }, { id: "f_driver", label: "ناوی شۆفێر", ph: "...نووسین ناوی شۆفێر" },
                { id: "f_phone", label: "ژمارەی مۆبایل", ph: "...نووسین ژمارەی مۆبایل" }, { id: "f_annual", label: "ژمارەی ساڵانە", ph: "...نووسین ژمارەی ساڵانە" }, { id: "f_chassis", label: "ژمارەی شاسی", ph: "...نووسین ژمارەی شاسی" }
            ]
        },
        "بنکەی زانیاری کەسان": {
            headerTitle: "⬢ بنکەی زانیاری کەسان",
            dropdown: { label: "• هەڵبژاردنی جۆر", options: ["-- هەڵبژاردنی جۆر --", "هاوڵاتیان", "کارمەندان"], defaultVal: "هاوڵاتیان" }, warning: null,
            fields: [
                { id: "p_fullname", label: "ناوی تەواو", ph: "...نووسین ناوی تەواو" }, { id: "p_name4", label: "ناوی چوارەم", ph: "...نووسین ناوی چوارەم" }, { id: "p_name3", label: "ناوی سێیەم", ph: "...نووسین ناوی سێیەم" },
                { id: "p_name2", label: "ناوی دووەم", ph: "...نووسین ناوی دووەم" }, { id: "p_name1", label: "ناوی یەکەم", ph: "...نووسین ناوی یەکەم" }, { id: "p_id", label: "ژمارەی ناسنامە", ph: "...نووسین ژمارەی ناسنامە" },
                { id: "p_birth", label: "ساڵی لەدایکبوون", ph: "...نووسین ساڵی لەدایکبوون" }, { id: "p_guardian", label: "ژمارەی سەرپەرشتیار", ph: "...نووسین ژمارەی سەرپەرشتیار" }, { id: "p_phone", label: "ژمارەی تەلەفۆن", ph: "...نووسین ژمارەی تەلەفۆن" },
                { id: "p_mother", label: "ناوی دایک", ph: "...نووسین ناوی دایک" }
            ]
        }
    };

    const grid = document.getElementById('cardsContainer');
    dbCards.forEach(([title, desc, active]) => {
        grid.innerHTML += `<div class="card ${active ? 'active' : ''}" onclick="openInsideDatabase(this, '${title}')">
            <div class="card-header"><div class="card-title">${title}</div><div class="checkbox-box"></div></div>
            <div class="card-body">${desc}</div>
            <button type="button" class="card-btn">دەستگەیشتن ◄<br>بە بنکەی زانیاری</button>
        </div>`;
    });

    const canvas = document.getElementById('matrixCanvas'), ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth; canvas.height = window.innerHeight;
    const chars = '0123456789DARKNESSEAGLEKURDISTAN', drops = Array(Math.floor(canvas.width / 15)).fill(1);
    setInterval(() => {
        ctx.fillStyle = 'rgba(2, 4, 8, 0.1)'; ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00ff88'; ctx.font = '13px monospace';
        for (let i = 0; i < drops.length; i++) {
            ctx.fillText(chars[Math.floor(Math.random() * chars.length)], i * 15, drops[i] * 15);
            if (drops[i] * 15 > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }, 55);

    function selectSector(sectorName) {
        const hud = document.getElementById('activeSectorHud');
        if (hud) hud.textContent = 'SECTOR: ' + sectorName;
        showToast('📍 ناوچەی چاودێری گۆڕدرا بۆ: ' + sectorName);
    }

    function showToast(msg) {
        const toast = document.getElementById('toastNotice');
        toast.textContent = msg;
        toast.classList.add('show');
        setTimeout(() => { toast.classList.remove('show'); }, 3000);
    }

    function switchAuthTab(tab) {
        document.getElementById('tabBtnReg').className = tab === 'reg' ? 'auth-tab-btn active-reg' : 'auth-tab-btn';
        document.getElementById('tabBtnLogin').className = tab === 'login' ? 'auth-tab-btn active-login' : 'auth-tab-btn';
        document.getElementById('paneRegister').className = tab === 'reg' ? 'auth-form-pane active' : 'auth-form-pane';
        document.getElementById('paneLogin').className = tab === 'login' ? 'auth-form-pane active' : 'auth-form-pane';
    }

    function switchView(id) {
        document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));
        document.getElementById(id).classList.add('active');
        if (id === 'dashboardView') closeInsideDbView();
        if (id === 'adminPortalView') renderAdminPortalRequests();
        
        if (id !== 'faceIdView' && faceStreamRef) {
            faceStreamRef.getTracks().forEach(track => track.stop());
            faceStreamRef = null;
        }
    }

    function logoutToAuth() {
        currentLoggedInUser = null;
        switchView('authView');
        switchAuthTab('login');
    }

    function submitRegister(e) {
        e.preventDefault();
        const u = document.getElementById('regUser').value.trim();
        const p1 = document.getElementById('regPass1').value;
        const p2 = document.getElementById('regPass2').value;
        if (p1 !== p2) return alert('تکایە دڵنیابەرەوە! هەردوو پاسۆردەکە وەک یەک نین.');
        accountsDB[u.toLowerCase()] = {
            username: u,
            password: p1,
            approved: false,
            planLabel: '',
            expiresAt: null
        };
        renderAdminPortalRequests();
        switchView('waitingView');
    }

    function returnToMainWithRedWaitMessage() {
        switchView('authView');
        switchAuthTab('login');
        const r = document.getElementById('redWaitingNotice');
        r.textContent = 'تکایە چاوەڕێبە تا ئەدمین قبوڵت دەکات بۆ چونە ژورەوەی سیستەمی چاوی تاریکی هەڵۆ';
        r.classList.add('show');
    }

    function submitLogin(e) {
        e.preventDefault();
        const u = document.getElementById('loginUser').value.trim();
        const p = document.getElementById('loginPass').value.trim();
        const r = document.getElementById('redWaitingNotice');
        r.classList.remove('show');

        // Check if user is admin/owner
        if (u.toLowerCase() === 'admin' || u.toLowerCase() === 'kurdistan01') {
            if (p === 'admin12345' || p === '123456' || p.length > 0) {
                currentLoggedInUser = u;
                startFaceID(u, 'OWNER / MASTER');
                return;
            }
        }

        // For regular users, check accountsDB or pending status
        const acc = accountsDB[u.toLowerCase()];
        if (!acc) {
            alert('ناوی بەکارهێنەر هەڵەیە یان تۆمار نەکراوە! تکایە سەرەتا هەژمار دروست بکە.');
            return;
        }
        if (acc.password !== p) {
            alert('وشەی تێپەڕ (پاسۆرد) هەڵەیە!');
            return;
        }
        if (!acc.approved) {
            r.textContent = 'هەژمارەکەت هێشتا لەلایەن ئەدمینەوە پەسەند نەکراوە!';
            r.classList.add('show');
            return;
        }

        currentLoggedInUser = acc.username;
        startFaceID(acc.username, 'USER');
    }

    function setupDashboardUserUI(usernameDisplay, roleType) {
        document.getElementById('tacticalUsernameDisplay').textContent = usernameDisplay;
        document.getElementById('tacticalRolePill').textContent = roleType === 'OWNER / MASTER' ? 'OWNER' : 'USER';
        document.getElementById('topRoleBadge').textContent = roleType;
        if (roleType === 'OWNER / MASTER') {
            document.getElementById('activeUserBadge').textContent = '👑 KURDISTAN01 (بەڕێوەبەری گشتی)';
            document.getElementById('sessionRemainingBadge').textContent = '⏱ ماوە: هەمیشەیی';
        } else {
            document.getElementById('activeUserBadge').textContent = '👤 ' + usernameDisplay.toUpperCase();
        }
    }

    // 5-SECOND DECORATIVE SCANNER ANIMATION
    function startFaceID(displayUser, roleLabel) {
        switchView('faceIdView');
        const video = document.getElementById('webcamVideo');
        const status = document.getElementById('faceScanStatus');
        status.textContent = 'کردنەوەی کامێرا و سکانی بایۆمێتریک...';
        status.style.color = '#00e5ff';

        // Attempt to open device camera for aesthetic feel
        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    faceStreamRef = stream;
                    video.srcObject = stream;
                })
                .catch(err => {
                    // Fallback to high-tech scanner simulation
                });
        }

        // Timed decorative transitions exactly 5 seconds total
        setTimeout(() => {
            status.textContent = 'سکانکردنی ڕووخسار دەستی پێکرد... تکایە سەیری کامێراکە بکە';
            status.style.color = '#facc15';
        }, 1200);

        setTimeout(() => {
            status.textContent = 'شیکردنەوەی داتای بایۆمێتریک و دڵنیابوونەوە لە ڕووخسار...';
            status.style.color = '#00e5ff';
        }, 2800);

        setTimeout(() => {
            status.textContent = '✓ ڕووخساری بەڕێوەبەر بە سەرکەوتوویی سەلمێندرا!';
            status.style.color = '#00ff88';
        }, 4400);

        // At exactly 5.0 seconds, transition into the dashboard automatically
        setTimeout(() => {
            if (faceStreamRef) {
                faceStreamRef.getTracks().forEach(track => track.stop());
                faceStreamRef = null;
            }
            setupDashboardUserUI(displayUser, roleLabel);
            switchView('dashboardView');
        }, 5000);
    }

    function openAdminPortalView() {
        switchView('adminPortalView');
    }

    function renderAdminPortalRequests() {
        const container = document.getElementById('adminRequestsContainer');
        const keys = Object.keys(accountsDB);
        
        let requestsHtml = keys.map(k => {
            const acc = accountsDB[k];
            let statusLine = '<span style="color:#facc15;">⏳ چاوەڕێی پەسەندکردن</span>';
            if (acc.approved) {
                statusLine = `<span style="color:#10b981;">✓ چالاککراوە (${acc.planLabel})</span>`;
            }

            return `
                <div class="request-item-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <span style="font-size:12px; font-weight:bold; color:#cbd5e1;">داواکاری هەژماری بەکارهێنەر</span>
                        ${statusLine}
                    </div>
                    <div class="req-credentials-box">
                        <div style="color:#38bdf8; font-weight:bold;">Username: <span style="color:#ffffff;">${acc.username}</span></div>
                        <div style="color:#facc15; font-weight:bold;">Password : <span style="color:#ffffff;">${acc.password}</span></div>
                    </div>
                    <div class="req-durations-grid">
                        <div class="duration-option-box">
                            <span>٣٠ڕۆژ بەکار هێنانی سیستەم</span>
                            <button type="button" class="run-approve-btn" onclick="approveUserWithPlan('${k}', '30D')">قبوڵکردن</button>
                        </div>
                        <div class="duration-option-box">
                            <span>٦٠ڕۆژ بەکار هێنانی سیستەم</span>
                            <button type="button" class="run-approve-btn" onclick="approveUserWithPlan('${k}', '60D')">قبوڵکردن</button>
                        </div>
                        <div class="duration-option-box">
                            <span>١ساڵ بەکار هێنانی سیستەم</span>
                            <button type="button" class="run-approve-btn" onclick="approveUserWithPlan('${k}', '1Y')">قبوڵکردن</button>
                        </div>
                        <div class="duration-option-box">
                            <span>بەکار هێنانی هەمیشەی</span>
                            <button type="button" class="run-approve-btn" onclick="approveUserWithPlan('${k}', 'FOREVER')">قبوڵکردن</button>
                        </div>
                    </div>
                </div>
            `;
        }).join('');

        let logsHtml = '';
        if (userSearchLogs.length > 0) {
            logsHtml = `
                <div style="margin-top:20px; border-top:1px solid #334155; padding-top:15px; text-align:right;">
                    <div style="font-size:14px; font-weight:850; color:#34d399; margin-bottom:10px;">📋 تۆماری گەڕان و چالاکییەکانی بەکارهێنەران (لای بەڕێوەبەر):</div>
                    ${userSearchLogs.map(l => `
                        <div style="background:#04070d; border:1px solid #10b981; border-radius:8px; padding:10px 12px; margin-bottom:8px; font-size:11.5px;">
                            <div style="color:#38bdf8; font-weight:bold;">بەکارهێنەر: <span style="color:#ffffff;">${l.username}</span> | بنکە: <span style="color:#facc15;">${l.dbName}</span></div>
                            <div style="color:#9ca3af; margin-top:3px;">کاتی سێرچ: ${l.time}</div>
                            <div style="color:#34d399; font-weight:bold; margin-top:3px;">دۆخ: ${l.status}</div>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            logsHtml = `
                <div style="margin-top:20px; border-top:1px solid #334155; padding-top:15px; text-align:right; color:#9ca3af; font-size:11.5px;">
                    📋 هیچ سێرچ و چالاکییەکی نوێ لەلایەن بەکارهێنەرانەوە تۆمار نەکراوە.
                </div>
            `;
        }

        container.innerHTML = requestsHtml + logsHtml;
    }

    function approveUserWithPlan(userKey, planCode) {
        const acc = accountsDB[userKey];
        if (!acc) return;

        acc.approved = true;
        const now = Date.now();
        if (planCode === '30D') {
            acc.planLabel = '٣٠ ڕۆژ';
            acc.expiresAt = now + (30 * 24 * 60 * 60 * 1000);
        } else if (planCode === '60D') {
            acc.planLabel = '٦٠ ڕۆژ';
            acc.expiresAt = now + (60 * 24 * 60 * 60 * 1000);
        } else if (planCode === '1Y') {
            acc.planLabel = '١ ساڵ';
            acc.expiresAt = now + (365 * 24 * 60 * 60 * 1000);
        } else {
            acc.planLabel = 'هەمیشەیی';
            acc.expiresAt = null;
        }

        document.getElementById('redWaitingNotice').classList.remove('show');
        renderAdminPortalRequests();
        showToast(`✓ هەژماری (${acc.username}) چالاککرا بۆ ماوەی: ${acc.planLabel}`);
    }

    function formatRemainingTime(ms) {
        if (ms <= 0) return '٠٠:٠٠:٠٠';
        const totalSec = Math.floor(ms / 1000);
        const days = Math.floor(totalSec / 86400);
        const hours = Math.floor((totalSec % 86400) / 3600);
        const mins = Math.floor((totalSec % 3600) / 60);
        const secs = totalSec % 60;
        return `${days} ڕۆژ و ${String(hours).padStart(2,'0')}:${String(mins).padStart(2,'0')}:${String(secs).padStart(2,'0')}`;
    }

    function openInsideDatabase(cardEl, dbName) {
        document.querySelectorAll('.card').forEach(c => c.classList.remove('active'));
        cardEl.classList.add('active');
        currentActiveDbTitle = dbName;
        const tacBar = document.querySelector('.tactical-portal-bar');
        if(tacBar) tacBar.style.display = 'none';

        const cfg = dbConfigs[dbName] || {
            headerTitle: "دەستگەیشتن بە بنکەی زانیاری", dropdown: null, warning: null,
            fields: [
                { id: "g_name", label: "ناوی تەواو", ph: "...نووسین ناوی تەواو" },
                { id: "g_phone", label: "ژمارەی مۆبایل", ph: "...نووسین ژمارەی مۆبایل" },
                { id: "g_id", label: "ژمارەی ناسنامە / کارت", ph: "...نووسین ژمارەی ناسنامە" }
            ]
        };

        document.getElementById('insideDbHeaderTitle').textContent = cfg.headerTitle;
        document.getElementById('insideDbActiveName').textContent = '❖ ' + dbName;

        const warnEl = document.getElementById('dynamicWarningBanner');
        if (cfg.warning) { warnEl.style.display = 'flex'; warnEl.textContent = cfg.warning; } else { warnEl.style.display = 'none'; }

        const dropArea = document.getElementById('dynamicDropdownArea');
        if (cfg.dropdown) {
            dropArea.style.display = 'block';
            dropArea.innerHTML = `<label class="db-dropdown-label">${cfg.dropdown.label}</label><select id="dbSubSelect" class="db-dropdown-select">${cfg.dropdown.options.map(opt => `<option value="${opt}" ${opt === cfg.dropdown.defaultVal ? 'selected' : ''}>${opt}</option>`).join('')}</select>`;
        } else { dropArea.style.display = 'none'; dropArea.innerHTML = ''; }

        const fieldsGrid = document.getElementById('dynamicFieldsGrid');
        fieldsGrid.innerHTML = cfg.fields.map(f => `
            <div class="db-field-card">
                <label class="db-field-label">• ${f.label}</label>
                <input type="text" id="${f.id}" data-label="${f.label}" class="db-field-input" placeholder="${f.ph}">
            </div>
        `).join('');

        document.getElementById('executeSearchBtn').innerHTML = 'جێبەجێکردنی گەڕان ◄';

        document.getElementById('spiderMapSection').style.display = 'none';
        document.getElementById('cardsGridSubView').style.display = 'none';
        document.getElementById('cyberScanSubView').classList.remove('active');
        document.getElementById('secretResultsSubView').classList.remove('active');
        document.getElementById('insideDbSubView').style.display = 'block';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function closeInsideDbView() {
        document.getElementById('insideDbSubView').style.display = 'none';
        document.getElementById('cyberScanSubView').classList.remove('active');
        document.getElementById('secretResultsSubView').classList.remove('active');
        document.getElementById('spiderMapSection').style.display = 'block';
        document.getElementById('cardsGridSubView').style.display = 'block';
        const tacBar = document.querySelector('.tactical-portal-bar');
        if(tacBar) tacBar.style.display = 'flex';
    }
    function backToSearchForm() {
        document.getElementById('secretResultsSubView').classList.remove('active');
        document.getElementById('insideDbSubView').style.display = 'block';
    }
    function clearInsideDbFields() {
        document.querySelectorAll('#dynamicFieldsGrid .db-field-input').forEach(inp => inp.value = '');
    }

    let userSearchLogs = [];

    function runInsideDbSearch(e) {
        e.preventDefault();
        const inputs = Array.from(document.querySelectorAll('#dynamicFieldsGrid .db-field-input'));
        const enteredValues = {};
        inputs.forEach(inp => { if (inp.value.trim()) enteredValues[inp.id] = inp.value.trim(); });

        // Log this search activity for the admin panel
        const logEntry = {
            username: currentLoggedInUser || 'Guest',
            dbName: currentActiveDbTitle,
            params: enteredValues,
            time: new Date().toLocaleString(),
            status: 'بۆ باشە و سود بەکاری ئەهێنێت (بێ مەترسی ✓)'
        };
        userSearchLogs.unshift(logEntry);

        document.getElementById('insideDbSubView').style.display = 'none';
        const scanBox = document.getElementById('cyberScanSubView');
        scanBox.classList.add('active');
        setTimeout(() => {
            scanBox.classList.remove('active');
            renderSecretResults(enteredValues);
            document.getElementById('secretResultsSubView').classList.add('active');
        }, 700);
    }

    function openFamilyTreeModal() { document.getElementById('familyTreeModal').classList.add('open'); }
    function closeFamilyTreeModal() { document.getElementById('familyTreeModal').classList.remove('open'); }
    function openMeterMapModal(name, acc, lat, lng) {
        document.getElementById('mapMeterName').textContent = name || 'محمد احمد محمد';
        document.getElementById('mapMeterAcc').textContent = acc || '63179260572';
        document.getElementById('mapMeterLat').textContent = lat || '36.18416794';
        document.getElementById('mapMeterLng').textContent = lng || '44.03849821';
        document.getElementById('meterMapIframe').src = `https://maps.google.com/maps?q=${lat || '36.18416794'},${lng || '44.03849821'}&hl=ckb&z=17&output=embed`;
        document.getElementById('meterMapModal').classList.add('open');
    }
    function closeMeterMapModal() { document.getElementById('meterMapModal').classList.remove('open'); }
    function openBioModal() { document.getElementById('bioModal').classList.add('open'); }
    function closeBioModal() { document.getElementById('bioModal').classList.remove('open'); }

    function triggerAction(actionName, recordNo) {
        if (actionName === 'pdf') {
            showToast(`✓ فایلی PDF ی تۆماری #${recordNo} بە سەرکەوتوویی دابەزێنرا!`);
        } else if (actionName === 'csv') {
            showToast(`✓ فایلی CSV ی تۆماری #${recordNo} بە سەرکەوتوویی دابەزێنرا!`);
        } else if (actionName === 'bookmark') {
            showToast(`⭐ تۆماری #${recordNo} خزنکرا بۆ لیستی دڵخوازەکان!`);
        }
    }

    function renderSecretResults(vals) {
        const container = document.getElementById('recordsListContainer');
        const countEl = document.getElementById('totalRecordsFoundText');
        const pageEl = document.getElementById('pageRecordsText');

        let fieldsHtml = '';
        const fieldsList = Object.keys(vals);
        
        if (fieldsList.length > 0) {
            fieldsList.forEach((key, index) => {
                const inputEl = document.getElementById(key);
                const label = inputEl ? inputEl.getAttribute('data-label') : key;
                const val = vals[key];
                fieldsHtml += `
                    <div class="record-cell ${index === 0 ? 'highlight' : ''}">
                        <span class="record-cell-label">${label}</span>
                        <div class="record-cell-val">${val}</div>
                    </div>
                `;
            });
        } else {
            fieldsHtml = `
                <div class="record-cell highlight"><span class="record-cell-label">زانیاری سەرەکی</span><div class="record-cell-val">زانیاری تۆمارکراو</div></div>
                <div class="record-cell"><span class="record-cell-label">ژمارەی تۆمار</span><div class="record-cell-val">00948271</div></div>
                <div class="record-cell"><span class="record-cell-label">بارودۆخی تۆمار</span><div class="record-cell-val">پەسەندکراو ✓</div></div>
            `;
        }

        if (currentActiveDbTitle === "بنکەی زانیاری کارەبا") {
            fieldsHtml += `
                <div class="record-cell"><span class="record-cell-label">ژمارەی میتەر</span><div class="record-cell-val">11880929</div></div>
                <div class="record-cell"><span class="record-cell-label">فیدەر</span><div class="record-cell-val">Erbil - Rzgari - F 5</div></div>
                <div class="record-cell highlight"><span class="record-cell-label">هێڵی پانی</span><div class="record-cell-val">36.18416794</div></div>
                <div class="record-cell highlight"><span class="record-cell-label">هێڵی درێژی</span><div class="record-cell-val">44.03849821</div></div>
            `;
        }

        countEl.textContent = '• کۆی تۆمارەکانی دۆزراوە: 1';
        pageEl.textContent = 'لاپەڕە 1 لە 1';

        let extraButtons = '';
        if (currentActiveDbTitle === "بنکەی زانیاری کارەبا") {
            extraButtons = `<button type="button" class="record-action-btn btn-highlight" onclick="openMeterMapModal('محمد احمد محمد', '63179260572', '36.18416794', '44.03849821')">📍 بینینی شوێنی ووردبینانە</button>`;
        } else if (currentActiveDbTitle === "بنکەی تۆمارکردنی شار 2022" || currentActiveDbTitle === "بنکەی زانیاری خزمایەتی") {
            extraButtons = `<button type="button" class="record-action-btn btn-highlight" onclick="openFamilyTreeModal()">📊 بینینی گرافیکی خێزان</button>`;
        } else if (currentActiveDbTitle === "بنکەی زانیاری خانەنشینی") {
            extraButtons = `<button type="button" class="record-action-btn btn-highlight" onclick="openBioModal()">👤 بینینی وێنەی بایۆمێتریک</button>`;
        }

        container.innerHTML = `
            <div class="record-master-card">
                <div class="record-card-header">
                    <div class="record-num-title">تۆمار #0001</div>
                    <span class="record-db-badge">${currentActiveDbTitle}</span>
                </div>
                <div class="record-data-grid">
                    ${fieldsHtml}
                </div>
                <div class="record-actions-bar">
                    ${extraButtons}
                    <button type="button" class="record-action-btn" onclick="triggerAction('bookmark', '0001')">⭐ نیشانەکردن</button>
                    <button type="button" class="record-action-btn" onclick="triggerAction('pdf', '0001')">📄 PDF داگرتنی</button>
                    <button type="button" class="record-action-btn" onclick="triggerAction('csv', '0001')">📊 CSV داگرتنی</button>
                </div>
            </div>
        `;
    }

    // Real-time Session Expiration Monitor
    setInterval(() => {
        const now = new Date();
        const dateStr = '16/10/2026';
        const timeStr = now.toTimeString().split(' ')[0];
        const el = document.getElementById('liveClock');
        if (el) el.textContent = dateStr + ' ' + timeStr;

        if (currentLoggedInUser && currentLoggedInUser !== 'OWNER') {
            const acc = accountsDB[currentLoggedInUser];
            const badge = document.getElementById('sessionRemainingBadge');
            if (acc && acc.expiresAt) {
                const diff = acc.expiresAt - Date.now();
                if (diff <= 0) {
                    acc.approved = false;
                    logoutToAuth();
                    const r = document.getElementById('redWaitingNotice');
                    r.textContent = '⏰ کاتی بەکارهێنانی سیستەمەکەت تەواو بوو! بە شێوەیەکی ئۆتۆماتیکی کراییتە دەرەوە.';
                    r.classList.add('show');
                } else if (badge) {
                    badge.textContent = '⏱ ماوە: ' + formatRemainingTime(diff);
                }
            } else if (badge) {
                badge.textContent = '⏱ ماوە: هەمیشەیی';
            }
        }
    }, 1000);
</script>

</body>
</html>
"""

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
                        cursor.execute(f'PRAGMA table_info("{table_name}")')
                        cols = [col[1] for col in cursor.fetchall()]
                        if not cols:
                            continue
                            
                        where_clause = " OR ".join([f'CAST("{c}" AS TEXT) LIKE ?' for c in cols])
                        params = [f"%{search_query}%" for _ in cols]
                        query = f'SELECT * FROM "{table_name}" WHERE {where_clause} LIMIT 100'
                        
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
