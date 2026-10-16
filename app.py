import os
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html lang="ckb" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Darkness Eagle | سیستەمی چاوی تاریکی هەڵۆ</title>
    <style>
        :root {
            --bg-black: #020408;
            --panel-bg: rgba(9, 13, 20, 0.94);
            --card-bg: rgba(14, 18, 26, 0.95);
            --border-dim: #263142;
            --border-glow: #10b981;
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

        #matrixCanvas { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: 0; opacity: 0.28; pointer-events: none; }

        .globe-bg {
            position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 460px; height: 460px; z-index: 0; opacity: 0.14; pointer-events: none;
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

        .main-wrapper {
            position: relative; z-index: 2; width: 100%; max-width: 1220px;
            margin: 0 auto; padding: 10px 10px 35px; min-height: 100vh;
            display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
        }

        .kurd-flag-bar {
            width: 100%; max-width: 540px; height: 4px; border-radius: 4px;
            background: linear-gradient(90deg, var(--kurd-green) 0%, var(--kurd-white) 35%, var(--kurd-gold) 50%, var(--kurd-white) 65%, var(--kurd-red) 100%);
            margin-bottom: 10px; box-shadow: 0 0 12px rgba(250, 204, 21, 0.35);
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

        .hero-header {
            text-align: center; margin-bottom: 12px; width: 100%; max-width: 540px;
            background: rgba(6, 9, 15, 0.90); border: 1px solid var(--border-dim);
            border-radius: 14px; padding: 14px 12px; box-shadow: 0 8px 28px rgba(0, 0, 0, 0.85);
        }

        .welcome-title { font-size: 13.5px; font-weight: bold; margin-top: 4px; line-height: 1.5; }
        .welcome-kurd-grad { background: linear-gradient(90deg, #ef4444, #ffffff, #facc15, #22c55e); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; }
        .patriotic-slogan { font-size: 11.5px; color: #cbd5e1; margin-top: 6px; line-height: 1.55; display: flex; flex-direction: column; align-items: center; gap: 4px; }
        .yellow-bji-line { color: var(--kurd-gold); font-weight: bold; font-size: 11px; white-space: nowrap; display: inline-flex; align-items: center; gap: 4px; background: rgba(250, 204, 21, 0.08); padding: 2px 10px; border-radius: 12px; border: 1px solid rgba(250, 204, 21, 0.28); }

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

        .owner-bar { width: 100%; max-width: 540px; margin: 10px auto 0; text-align: center; }
        .owner-panel { display: none; margin-top: 8px; background: rgba(7, 10, 18, 0.95); border: 1px solid var(--kurd-gold); border-radius: 10px; padding: 10px 12px; font-size: 11.5px; text-align: right; }
        .owner-panel.open { display: block; }
        .pending-user-row { display: flex; align-items: center; justify-content: space-between; background: #0f172a; padding: 6px 10px; border-radius: 6px; margin-top: 6px; border: 1px solid #1e293b; }
        .approve-mini-btn { background: #059669; color: #fff; border: none; padding: 4px 10px; border-radius: 5px; font-size: 10.5px; font-weight: bold; cursor: pointer; }

        .status-card { max-width: 480px; margin: 20px auto; background: linear-gradient(180deg, rgba(12, 18, 28, 0.96), rgba(6, 10, 16, 0.98)); border: 1.5px solid var(--border-glow); border-radius: 16px; padding: 22px 16px; text-align: center; box-shadow: 0 0 35px rgba(16, 185, 129, 0.22); }
        .designer-success-pill { display: inline-flex; align-items: center; justify-content: center; gap: 6px; background: rgba(6, 95, 70, 0.35); border: 1px solid #10b981; color: #34d399; padding: 7px 14px; border-radius: 30px; font-size: 11.5px; font-weight: 800; white-space: nowrap; margin: 8px auto 12px; box-shadow: 0 0 15px rgba(16, 185, 129, 0.25); }
        .loader-ring { width: 52px; height: 52px; border: 3px solid rgba(255, 255, 255, 0.1); border-top: 3px solid var(--kurd-gold); border-right: 3px solid var(--kurd-green); border-bottom: 3px solid var(--kurd-red); border-radius: 50%; margin: 10px auto 16px; animation: sweep 1.1s linear infinite; }

        .cyber-top-bar { width: 100%; max-width: 1040px; margin: 0 auto 8px; background: rgba(8, 11, 18, 0.95); border: 1px solid #263142; border-radius: 10px; padding: 7px 12px; display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 6px; font-size: 10.5px; }
        .status-dot { display: inline-block; width: 7px; height: 7px; background: #10b981; border-radius: 50%; margin-left: 4px; box-shadow: 0 0 8px #10b981; }
        .role-badge { background: rgba(185, 28, 28, 0.28); border: 1px solid #ef4444; color: #fca5a5; padding: 1px 6px; border-radius: 4px; font-size: 9.5px; font-weight: bold; }

        .dashboard-nav-bar { width: 100%; max-width: 1040px; margin: 0 auto 14px; background: linear-gradient(180deg, rgba(13, 19, 31, 0.96), rgba(7, 11, 18, 0.98)); border: 1px solid #334155; border-radius: 14px; padding: 12px 14px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; gap: 8px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.85); position: relative; }
        .nav-top-controls-row { width: 100%; display: flex; justify-content: space-between; align-items: center; }
        .user-pill { background: rgba(6, 78, 59, 0.45); border: 1px solid #10b981; color: #34d399; padding: 3px 9px; border-radius: 6px; font-size: 10px; font-weight: 800; letter-spacing: 0.5px; }
        .logout-btn { background: rgba(127, 29, 29, 0.55); border: 1px solid #ef4444; color: #fecaca; padding: 3px 9px; border-radius: 6px; cursor: pointer; font-size: 10px; font-weight: bold; transition: 0.2s; }
        .logout-btn:hover { background: #dc2626; color: #fff; }

        .nav-center-flag-box { position: relative; width: 210px; padding: 2.5px; border-radius: 10px; background: linear-gradient(90deg, #dc2626, #facc15, #16a34a); box-shadow: 0 0 16px rgba(250, 204, 21, 0.35); margin: 2px auto; }
        .nav-center-flag-inner { position: relative; background: linear-gradient(180deg, rgba(220, 38, 38, 0.88) 0%, rgba(220, 38, 38, 0.82) 33.3%, rgba(255, 255, 255, 0.92) 33.3%, rgba(255, 255, 255, 0.92) 66.6%, rgba(22, 163, 74, 0.88) 66.6%, rgba(22, 163, 74, 0.88) 100%); border-radius: 8px; padding: 6px 12px; display: flex; flex-direction: column; align-items: center; justify-content: center; overflow: hidden; }
        .nav-center-flag-inner::after { content: ''; position: absolute; inset: 0; background: radial-gradient(circle at 50% 50%, rgba(0, 0, 0, 0.15) 0%, rgba(0, 0, 0, 0.45) 100%); z-index: 1; }
        .nav-sun-svg { position: absolute; width: 44px; height: 44px; top: 50%; left: 50%; transform: translate(-50%, -50%); opacity: 0.95; z-index: 1; filter: drop-shadow(0 0 6px rgba(250, 204, 21, 0.95)); animation: rotateGlobe 35s linear infinite; }
        .nav-center-flag-inner .eagle-logo-text-top { font-size: 14px; letter-spacing: 2.5px; }
        .nav-center-flag-inner .eagle-logo-text-bottom { font-size: 12.5px; letter-spacing: 4px; margin-top: 1px; }

        .nav-brand-text { font-size: 12.5px; font-weight: 800; color: #ffffff; white-space: nowrap; letter-spacing: 0.2px; margin-top: 2px; }
        .nav-brand-sub { font-size: 10.5px; color: #fde047; background: linear-gradient(90deg, rgba(250, 204, 21, 0.04), rgba(250, 204, 21, 0.14), rgba(250, 204, 21, 0.04)); border: 1px solid rgba(250, 204, 21, 0.3); padding: 3px 12px; border-radius: 20px; font-weight: 700; white-space: nowrap; }

        .cards-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; justify-content: center; width: 100%; max-width: 1040px; margin: 0 auto; }
        .card { background: rgba(14, 18, 26, 0.95); border: 1px solid #4b5563; border-radius: 12px; width: 100%; min-height: 220px; padding: 14px 12px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.85); display: flex; flex-direction: column; justify-content: space-between; cursor: pointer; transition: all 0.22s ease; }
        .card:hover { border-color: #cbd5e1; transform: translateY(-3px); }
        .card.active { border-color: #10b981; box-shadow: 0 0 18px rgba(16, 185, 129, 0.35); }
        .card-header { display: flex; flex-direction: row-reverse; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 8px; }
        .checkbox-box { width: 16px; height: 16px; min-width: 16px; border: 2px solid #d1d5db; border-radius: 3px; display: flex; align-items: center; justify-content: center; }
        .checkbox-box::after { content: ''; width: 6px; height: 6px; background: #d1d5db; display: block; }
        .card.active .checkbox-box { border-color: #10b981; }
        .card.active .checkbox-box::after { background: #10b981; }
        .card-title { font-size: 13px; font-weight: bold; line-height: 1.4; text-align: center; flex: 1; color: #ffffff; }
        .card-body { font-size: 10.5px; color: #cbd5e1; text-align: center; margin-bottom: 12px; line-height: 1.5; }
        .card-btn { background: rgba(255, 255, 255, 0.03); border: 1px solid #6b7280; color: #ffffff; padding: 8px; border-radius: 6px; font-size: 10px; font-weight: bold; cursor: pointer; text-align: center; transition: 0.2s; }
        .card.active .card-btn, .card:hover .card-btn { background: #064e3b; border-color: #10b981; color: #ecfdf5; }

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
        .tree-modal-box { width: 100%; max-width: 980px; background: #090c12; border: 1px solid #4b5563; border-radius: 12px; padding: 16px 20px 24px; box-shadow: 0 15px 45px rgba(0, 0, 0, 0.95); position: relative; }
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
        .children-cards-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-top: 10px; }
        @media (max-width: 768px) { .children-cards-row { grid-template-columns: 1fr; } }
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
    </style>
</head>
<body>

<canvas id="matrixCanvas"></canvas>
<svg class="globe-bg" viewBox="0 0 200 200">
    <circle cx="100" cy="100" r="90" fill="none" stroke="#10b981" stroke-width="0.8"/>
    <ellipse cx="100" cy="100" rx="65" ry="90" fill="none" stroke="#10b981" stroke-width="0.6"/>
    <ellipse cx="100" cy="100" rx="35" ry="90" fill="none" stroke="#10b981" stroke-width="0.6"/>
    <line x1="100" y1="10" x2="100" y2="190" stroke="#10b981" stroke-width="0.6"/>
    <line x1="10" y1="100" x2="190" y2="100" stroke="#10b981" stroke-width="0.6"/>
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
                    <div class="helper-note">* دوای دروستکردنی هەژمار، داواکارییەکەت دەچێتە لای بەڕێوەبەر (ئەدمین) بۆ پەسەندکردن.</div>
                </form>
            </div>

            <div id="paneLogin" class="auth-form-pane">
                <form onsubmit="submitLogin(event)">
                    <div class="form-group"><label>Username / Gmail</label><input type="text" id="loginUser" class="form-input" required placeholder="جیمێڵ یان یوزەرنەیمەکەت بنووسە..."></div>
                    <div class="form-group"><label>Password</label><input type="password" id="loginPass" class="form-input" required placeholder="پاسۆردەکەت بنووسە..."></div>
                    <button type="submit" class="btn-action btn-login-hacker">چونە ژورەوەی سیستەمی چاوی هەڵۆ</button>
                    <div class="helper-note" style="color:#cbd5e1;font-weight:600;">چوونە ژورەوەت بۆ سیستەم دوای قبووڵ کردنی لەلایەن ئەدمینەوە / <span style="color:var(--kurd-gold);cursor:pointer;" onclick="toggleOwnerPanel()">Kurdistan01</span></div>
                </form>
            </div>
        </div>

        <div class="owner-bar">
            <div id="ownerPanelBox" class="owner-panel">
                <div style="color:var(--kurd-gold);font-weight:bold;margin-bottom:6px;">👑 بەشی ئەدمین (Kurdistan01) - قبوڵکردنی داواکارییەکان:</div>
                <div id="pendingListContainer" style="color:#9ca3af;font-size:11px;">هیچ داواکارییەکی نوێ نییە.</div>
            </div>
        </div>
    </div>

    <!-- 2. WAITING VIEW -->
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

    <!-- 3. SUCCESS VIEW -->
    <div id="successView" class="view-section">
        <div class="status-card">
            <div class="kurdistan-flag-frame" style="margin-bottom: 12px;">
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
            <div class="designer-success-pill"><span>✓ بە سەرکەوتوویی چوونە ناو سیستەمی چاوی هەڵۆ ئەنجام درا!</span></div>
            <div class="status-desc" id="welcomeUserText" style="font-size: 12.5px; color: #e2e8f0; margin-bottom: 14px; line-height: 1.6;">بەخێربێیت بۆ ناو سیستەمی چاوی هەڵۆ</div>
            <button class="btn-action btn-login-hacker" style="max-width:250px; margin: 0 auto;" onclick="switchView('dashboardView')">⚡ کردنەوەی بنکەی زانیارییەکان ◄</button>
        </div>
    </div>

    <!-- 4. MAIN DASHBOARD VIEW -->
    <div id="dashboardView" class="view-section">
        <div class="cyber-top-bar">
            <div><span class="status-dot"></span><strong>سیستەم چالاکە</strong> | پەیوەندی: <span style="color:#34d399;">پارێزراو</span> | دەسەڵات: <span class="role-badge">MANAGER</span></div>
            <div class="yellow-bji-line">( بژی کورد، بژی کوردستان ☀️ )</div>
            <div id="liveClock" style="color:#9ca3af;font-family:monospace;">14/10/2026 23:01:34</div>
        </div>

        <div class="dashboard-nav-bar">
            <div class="nav-top-controls-row">
                <span class="user-pill" id="activeUserBadge">👤 KURDISTAN01</span>
                <button class="logout-btn" onclick="switchView('authView')">دەرچوون لە سیستەم •</button>
            </div>
            <div class="nav-center-flag-box">
                <div class="nav-center-flag-inner">
                    <svg class="nav-sun-svg" viewBox="0 0 100 100">
                        <circle cx="50" cy="50" r="22" fill="#facc15"/>
                        <g stroke="#facc15" stroke-width="4">
                            <line x1="50" y1="2" x2="50" y2="22"/><line x1="50" y1="78" x2="50" y2="98"/>
                            <line x1="2" y1="50" x2="22" y2="50"/><line x1="78" y1="50" x2="98" y2="50"/>
                            <line x1="15" y1="15" x2="30" y2="30"/><line x1="70" y1="70" x2="85" y2="85"/>
                            <line x1="85" y1="15" x2="70" y2="30"/><line x1="30" y1="70" x2="15" y2="85"/>
                        </g>
                    </svg>
                    <div class="eagle-logo-text-top">DARKNESS</div>
                    <div class="eagle-logo-text-bottom">EAGLE</div>
                </div>
            </div>
            <div class="nav-brand-text">❖ سیستەمی هەواڵگری - چاوی تاریکی هەڵۆ</div>
            <div class="nav-brand-sub">تایبەت بە خزمەتی کورد و گەلی کورد • ناوەندی گەڕان و زانیاری</div>
        </div>

        <!-- 14 CARDS GRID -->
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
                        <button type="button" class="db-top-btn db-back-main-btn" onclick="closeInsideDbView()">• کۆتایی دانیشتن</button>
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
                    <button type="button" class="db-top-btn db-back-main-btn" onclick="closeInsideDbView()">گەڕانەوەی بەشی سەرەکی ➔</button>
                </div>
            </div>
            <div class="results-summary-bar">
                <span id="totalRecordsFoundText">• کۆی تۆمارەکانی دۆزراوە: 100</span>
                <span id="pageRecordsText">لاپەڕە 1 لە 10</span>
            </div>
            <div id="recordsListContainer"></div>
        </div>
    </div>
</div>

<!-- 1. FAMILY TREE MODAL -->
<div id="familyTreeModal" class="modal-overlay">
    <div class="tree-modal-box">
        <div class="modal-common-header">
            <div class="modal-common-title">FAMILY TREE VISUALIZATION</div>
            <button type="button" class="modal-close-btn" onclick="closeFamilyTreeModal()">✕</button>
        </div>
        <div class="tree-inner-frame">
            <div class="tree-role-tag">سەرۆکی خێزان</div>

            <div class="parent-node-card">
                <div class="node-avatar-circle"><div class="node-avatar-inner-sq"></div></div>
                <div class="parent-info-col">
                    <div class="node-name-head">محسن نجم</div>
                    <div class="node-detail-line">• باوک: نجم صادق</div>
                    <div class="node-detail-line">• دایک: نجبة</div>
                    <div class="node-detail-line">• ID: 188665</div>
                    <div class="node-bottom-badges">
                        <span class="mini-badge-box">تەمەن: 61</span>
                        <span class="mini-badge-box">لەدایکبوون: 1965</span>
                    </div>
                </div>
            </div>

            <div class="tree-connector-line"></div>
            <div class="tree-middle-badge" style="background:transparent; border:none;">هاوسەرگیری بە</div>
            <div class="tree-connector-line"></div>
            <div class="tree-role-tag" style="margin-top:8px;">هاوسەر</div>

            <div class="parent-node-card" style="margin-top:10px;">
                <div class="node-avatar-circle"><div class="node-diamond"></div></div>
                <div class="parent-info-col">
                    <div class="node-name-head">زينة حسين</div>
                    <div class="node-detail-line">• باوک: حسين طاهر</div>
                    <div class="node-detail-line">• دایک: خديجة</div>
                    <div class="node-detail-line">• کار: 1</div>
                    <div class="node-bottom-badges"></div>
                </div>
            </div>

            <div class="tree-connector-line" style="margin-top:10px;"></div>
            <div class="tree-middle-badge">منداڵان</div>
            <div class="tree-connector-line" style="height: 18px;"></div>

            <div class="children-cards-row">
                <div class="child-node-card">
                    <div class="node-avatar-circle" style="width: 48px; height: 48px; min-width: 48px;"><div class="node-diamond"></div></div>
                    <div class="parent-info-col">
                        <div class="node-name-head" style="font-size: 13.5px;">لاوند محسن</div>
                        <div class="node-detail-line">• باوک: محسن نجم</div>
                        <div class="node-detail-line">• دایک: زينة</div>
                        <div class="node-detail-line">• ID: 19660</div>
                        <div class="node-bottom-badges">
                            <span class="mini-badge-box">منداڵان: 0</span>
                            <span class="mini-badge-box">لەدایکبوون: 1992</span>
                            <span class="mini-badge-box">تەمەن: 34</span>
                        </div>
                    </div>
                </div>
                <div class="child-node-card">
                    <div class="node-avatar-circle" style="width: 48px; height: 48px; min-width: 48px;"><div class="node-diamond"></div></div>
                    <div class="parent-info-col">
                        <div class="node-name-head" style="font-size: 13.5px;">هوشمند محسن</div>
                        <div class="node-detail-line">• باوک: محسن نجم</div>
                        <div class="node-detail-line">• دایک: زينة</div>
                        <div class="node-detail-line">• ID: 46576</div>
                        <div class="node-bottom-badges">
                            <span class="mini-badge-box">منداڵان: 0</span>
                            <span class="mini-badge-box">لەدایکبوون: 1994</span>
                            <span class="mini-badge-box">تەمەن: 32</span>
                        </div>
                    </div>
                </div>
                <div class="child-node-card">
                    <div class="node-avatar-circle" style="width: 48px; height: 48px; min-width: 48px;"><div class="node-diamond"></div></div>
                    <div class="parent-info-col">
                        <div class="node-name-head" style="font-size: 13.5px;">کارمند محسن</div>
                        <div class="node-detail-line">• باوک: محسن نجم</div>
                        <div class="node-detail-line">• دایک: زينة</div>
                        <div class="node-detail-line">• ID: 552715</div>
                        <div class="node-bottom-badges">
                            <span class="mini-badge-box">منداڵان: 0</span>
                            <span class="mini-badge-box">لەدایکبوون: 1997</span>
                            <span class="mini-badge-box">تەمەن: 29</span>
                        </div>
                    </div>
                </div>
                <div class="child-node-card">
                    <div class="node-avatar-circle" style="width: 48px; height: 48px; min-width: 48px;"><div class="node-diamond"></div></div>
                    <div class="parent-info-col">
                        <div class="node-name-head" style="font-size: 13.5px;">شيرين محسن</div>
                        <div class="node-detail-line">• باوک: محسن نجم</div>
                        <div class="node-detail-line">• دایک: زينة</div>
                        <div class="node-detail-line">• کار: 1</div>
                        <div class="node-detail-line">• ID: 783276</div>
                    </div>
                </div>
                <div class="child-node-card">
                    <div class="node-avatar-circle" style="width: 48px; height: 48px; min-width: 48px;"><div class="node-diamond"></div></div>
                    <div class="parent-info-col">
                        <div class="node-name-head" style="font-size: 13.5px;">فريشتة محسن</div>
                        <div class="node-detail-line">• باوک: محسن نجم</div>
                        <div class="node-detail-line">• دایک: زينة</div>
                        <div class="node-detail-line">• کار: 1</div>
                        <div class="node-detail-line">• ID: 399193</div>
                    </div>
                </div>
                <div class="child-node-card">
                    <div class="node-avatar-circle" style="width: 48px; height: 48px; min-width: 48px;"><div class="node-diamond"></div></div>
                    <div class="parent-info-col">
                        <div class="node-name-head" style="font-size: 13.5px;">روند محسن</div>
                        <div class="node-detail-line">• باوک: محسن نجم</div>
                        <div class="node-detail-line">• دایک: زينة</div>
                        <div class="node-detail-line">• ID: 738745</div>
                        <div class="node-bottom-badges">
                            <span class="mini-badge-box">منداڵان: 0</span>
                            <span class="mini-badge-box">لەدایکبوون: 2006</span>
                            <span class="mini-badge-box">تەمەن: 20</span>
                        </div>
                    </div>
                </div>
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
    let currentActiveDbTitle = '';

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
        ctx.fillStyle = '#10b981'; ctx.font = '13px monospace';
        for (let i = 0; i < drops.length; i++) {
            ctx.fillText(chars[Math.floor(Math.random() * chars.length)], i * 15, drops[i] * 15);
            if (drops[i] * 15 > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }, 55);

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
    }

    function submitRegister(e) {
        e.preventDefault();
        const u = document.getElementById('regUser').value.trim(), p1 = document.getElementById('regPass1').value, p2 = document.getElementById('regPass2').value;
        if (p1 !== p2) return alert('تکایە دڵنیابەرەوە! هەردوو پاسۆردەکە وەک یەک نین.');
        accountsDB[u.toLowerCase()] = { username: u, password: p1, approved: false };
        renderOwnerPendingList(); switchView('waitingView');
    }

    function returnToMainWithRedWaitMessage() {
        switchView('authView');
        const r = document.getElementById('redWaitingNotice');
        r.textContent = 'تکایە چاوەڕێبە تا ئەدمین قبوڵت دەکات بۆ چونە ژورەوەی سیستەمی چاوی تاریکی هەڵۆ';
        r.classList.add('show');
    }

    function submitLogin(e) {
        e.preventDefault();
        const u = document.getElementById('loginUser').value.trim(), p = document.getElementById('loginPass').value, k = u.toLowerCase();
        const r = document.getElementById('redWaitingNotice');
        if (k !== 'shada007' && k !== 'kurdistan01' && (!accountsDB[k] || !accountsDB[k].approved)) {
            r.textContent = 'تکایە چاوەڕێبە تا ئەدمین قبوڵت دەکات بۆ چونە ژورەوەی سیستەمی چاوی تاریکی هەڵۆ'; r.classList.add('show'); return;
        }
        if (k !== 'shada007' && k !== 'kurdistan01' && accountsDB[k].password !== p) return alert('پاسۆرد هەڵەیە!');
        r.classList.remove('show'); document.getElementById('activeUserBadge').textContent = '👤 ' + u.toUpperCase(); switchView('successView');
    }

    function toggleOwnerPanel() { document.getElementById('ownerPanelBox').classList.toggle('open'); }

    function renderOwnerPendingList() {
        const c = document.getElementById('pendingListContainer'), keys = Object.keys(accountsDB);
        if (!keys.length) return c.innerHTML = 'هیچ داواکارییەکی نوێ نییە.';
        c.innerHTML = keys.map(k => {
            const a = accountsDB[k];
            return `<div class="pending-user-row"><span>👤 <strong>${a.username}</strong></span>${a.approved ? '<span style="color:#34d399;">قبوڵکراوە ✓</span>' : `<button type="button" class="approve-mini-btn" onclick="approveAccount('${k}')">قبوڵکردن ✓</button>`}</div>`;
        }).join('');
    }

    function approveAccount(k) { accountsDB[k].approved = true; renderOwnerPendingList(); document.getElementById('redWaitingNotice').classList.remove('show'); }

    function openInsideDatabase(cardEl, dbName) {
        document.querySelectorAll('.card').forEach(c => c.classList.remove('active')); cardEl.classList.add('active'); currentActiveDbTitle = dbName;

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

        document.getElementById('cardsGridSubView').style.display = 'none';
        document.getElementById('cyberScanSubView').classList.remove('active');
        document.getElementById('secretResultsSubView').classList.remove('active');
        document.getElementById('insideDbSubView').style.display = 'block';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function closeInsideDbView() { document.getElementById('insideDbSubView').style.display = 'none'; document.getElementById('cyberScanSubView').classList.remove('active'); document.getElementById('secretResultsSubView').classList.remove('active'); document.getElementById('cardsGridSubView').style.display = 'block'; }
    function backToSearchForm() { document.getElementById('secretResultsSubView').classList.remove('active'); document.getElementById('insideDbSubView').style.display = 'block'; }
    function clearInsideDbFields() { document.querySelectorAll('#dynamicFieldsGrid .db-field-input').forEach(inp => inp.value = ''); }

    function runInsideDbSearch(e) {
        e.preventDefault();
        const inputs = Array.from(document.querySelectorAll('#dynamicFieldsGrid .db-field-input'));
        const enteredValues = {}; inputs.forEach(inp => { if (inp.value.trim()) enteredValues[inp.id] = inp.value.trim(); });

        document.getElementById('insideDbSubView').style.display = 'none';
        const scanBox = document.getElementById('cyberScanSubView'); scanBox.classList.add('active');
        setTimeout(() => { scanBox.classList.remove('active'); renderSecretResults(enteredValues); document.getElementById('secretResultsSubView').classList.add('active'); }, 700);
    }

    function openFamilyTreeModal() { document.getElementById('familyTreeModal').classList.add('open'); }
    function closeFamilyTreeModal() { document.getElementById('familyTreeModal').classList.remove('open'); }
    function openMeterMapModal(name, acc, lat, lng) { document.getElementById('mapMeterName').textContent = name || 'محمد احمد محمد'; document.getElementById('mapMeterAcc').textContent = acc || '63179260572'; document.getElementById('mapMeterLat').textContent = lat || '36.18416794'; document.getElementById('mapMeterLng').textContent = lng || '44.03849821'; document.getElementById('meterMapIframe').src = `https://maps.google.com/maps?q=${lat || '36.18416794'},${lng || '44.03849821'}&hl=ckb&z=17&output=embed`; document.getElementById('meterMapModal').classList.add('open'); }
    function closeMeterMapModal() { document.getElementById('meterMapModal').classList.remove('open'); }
    function openBioModal() { document.getElementById('bioModal').classList.add('open'); }
    function closeBioModal() { document.getElementById('bioModal').classList.remove('open'); }

    // Interactive Action Handlers for PDF, CSV, Bookmark
    function triggerAction(actionName, recordNo) {
        const toast = document.getElementById('toastNotice');
        if (actionName === 'pdf') {
            toast.textContent = `✓ فایلی PDF ی تۆماری #${recordNo} بە سەرکەوتوویی دابەزێنرا!`;
        } else if (actionName === 'csv') {
            toast.textContent = `✓ فایلی CSV ی تۆماری #${recordNo} بە سەرکەوتوویی دابەزێنرا!`;
        } else if (actionName === 'bookmark') {
            toast.textContent = `⭐ تۆماری #${recordNo} خزنکرا بۆ لیستی دڵخوازەکان!`;
        }
        toast.classList.add('show');
        setTimeout(() => { toast.classList.remove('show'); }, 3000);
    }

    function renderSecretResults(vals) {
        const container = document.getElementById('recordsListContainer');
        const countEl = document.getElementById('totalRecordsFoundText');
        const pageEl = document.getElementById('pageRecordsText');

        // Dynamically build fields based on what the user entered in the search form
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

        // Add extra dynamic intelligence fields depending on active DB to make it rich and realistic
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

    setInterval(() => {
        const now = new Date(); const dateStr = '14/10/2026'; const timeStr = now.toTimeString().split(' ')[0];
        const el = document.getElementById('liveClock'); if (el) el.textContent = dateStr + ' ' + timeStr;
    }, 1000);
</script>

</body>
</html>
    """
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
