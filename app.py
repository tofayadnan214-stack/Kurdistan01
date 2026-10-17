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
            const rawU = document.getElementById('loginUser').value;
            const rawP = document.getElementById('loginPass').value;
            const u = cleanInput(rawU);
            const p = cleanInput(rawP);
            const r = document.getElementById('redWaitingNotice');
            if (r) r.classList.remove('show');

            const targetUser = "Kurdistan01#001_##0101";
            const targetPass = "Kurdistan01#001_##0101";

            if (!u || !p) {
                if (r) {
                    r.textContent = 'تکایە هەردوو خانەی ناوی بەکارهێنەر و وشەی نهێنی پڕبکەرەوە!';
                    r.classList.add('show');
                }
                return;
            }

            if (u === targetUser && p === targetPass) {
                currentLoggedInUser = 'Kurdistan01';
                startFaceID('Kurdistan01', 'OWNER / MASTER');
                return;
            }

            if (r) {
                r.textContent = 'ناوی بەکارهێنەر یان وشەی نهێنی هەڵەیە! تکایە دووبارە هەوڵ بدە.';
                r.classList.add('show');
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
