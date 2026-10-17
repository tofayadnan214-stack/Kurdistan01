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
            background: linear-gradient(rgba(2, 4, 8, 0.85), rgba(2, 4, 8, 0.95));
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

        /* FIXED 3-COLUMN CARDS GRID */
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

        
        /* FIXED MODAL OVERLAYS AND PADDING TO PREVENT TEXT CLIPPING */
        .modal-overlay {
            display: none; position: fixed; inset: 0;
            background: rgba(0, 0, 0, 0.92); z-index: 9999;
            align-items: center; justify-content: center;
            padding: 40px 15px 20px 15px; overflow-y: auto;
            -webkit-overflow-scrolling: touch;
        }
        .modal-overlay.open { display: flex; }
        
        .tree-modal-box {
            width: 100%; max-width: 980px; max-height: 90vh;
            overflow-y: auto; touch-action: manipulation;
            background: #090c12; border: 1.5px solid #10b981;
            border-radius: 14px; padding: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.98);
            position: relative; margin-top: auto; margin-bottom: auto;
        }

        .map-modal-box {
            width: 100%; max-width: 620px; max-height: 92vh;
            overflow-y: auto; background: #0c1017;
            border: 2px solid #10b981; border-radius: 16px;
            padding: 20px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.98);
            position: relative; margin-top: auto; margin-bottom: auto;
        }

        .meter-info-card {
            background: linear-gradient(135deg, rgba(6, 78, 59, 0.3), rgba(15, 23, 42, 0.95));
            border: 1px solid #10b981; border-radius: 10px; padding: 14px 16px;
            margin-bottom: 14px; font-size: 12px; line-height: 1.9; color: #e5e7eb; text-align: right;
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.15);
        }

        .meter-map-frame {
            width: 100%; height: 440px; border: 1.5px solid #00e5ff;
            border-radius: 12px; overflow: hidden; background: #111827;
            position: relative; box-shadow: 0 0 25px rgba(0, 229, 255, 0.25);
        }
        .meter-map-frame iframe { width: 100%; height: 100%; border: 0; filter: contrast(1.1) saturate(1.2); }


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
    

        .modal-common-header {
            display: flex; justify-content: space-between; align-items: center;
            flex-wrap: wrap; gap: 10px; border-bottom: 1px solid #263142;
            padding-bottom: 10px; margin-bottom: 16px;
        }
        .modal-common-title { font-size: 14px; font-weight: 800; color: #ffffff; display: flex; align-items: center; gap: 6px; }

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

    <!-- 4. MAIN DASHBOARD VIEW -->
    <div id="dashboardView" class="view-section">
        <!-- TOP STATUS BAR -->
        <div class="cyber-top-bar">
            <div><span class="status-dot"></span><strong>سیستەم چالاکە</strong> | پەیوەندی: <span style="color:#34d399;">پارێزراو</span> | دەسەڵات: <span class="role-badge-small" id="topRoleBadge">OWNER / MASTER</span></div>
            <div class="yellow-bji-line">( بژی کورد، بژی کوردستان ☀️ )</div>
            <div id="liveClock" style="color:#9ca3af;font-family:monospace;">17/10/2026 17:15:00</div>
        </div>

        <!-- REFINED COMPACT BAR -->
        <div class="dashboard-nav-bar-compact">
            <span class="admin-pill-small" id="activeUserBadge">👑 KURDISTAN01 (بەڕێوەبەری گشتی)</span>
            <span class="session-timer-text" id="sessionRemainingBadge">⏱ ماوە: هەمیشەیی</span>
        </div>

        <!-- TACTICAL BAR -->
        <div class="tactical-portal-bar">
            <div class="admin-star-portal-btn" onclick="openAdminPortalView()" title="چوونە ژوورەوەی بەڕێوەبەر">
                <div class="star-box-icon">★</div>
                <div class="portal-title-col">
                    <span class="portal-main-title">Kurdistan01</span>
                    <span class="portal-sub-title">چوونە ژورەوەی بەڕێوبەر</span>
                </div>
            </div>

            <div class="user-status-right-group">
                <div class="user-online-pill-box">
                    <span class="blinking-green-dot"></span>
                    <span class="logged-username-text" id="tacticalUsernameDisplay">Kurdistan01</span>
                    <span class="user-role-tag-pill" id="tacticalRolePill">OWNER</span>
                </div>
                <button type="button" class="red-exit-icon-btn" onclick="logoutToAuth()" title="دەرچوون لە سیستەم (Logout)">
                    ➔
                </button>
            </div>
        </div>

        <!-- CYBER SPIDERWEB NETWORK TOPOLOGY MAP -->
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

                    <!-- Background Radar Target Rings -->
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

                    <!-- Glowing Connection Lines -->
                    <g stroke="#00e5ff" stroke-width="1.6" opacity="0.85" filter="url(#neonBlur)">
                        <line x1="255" y1="68" x2="290" y2="105"/>
                        <line x1="255" y1="68" x2="240" y2="155"/>
                        <line x1="290" y1="105" x2="345" y2="112"/>
                        <line x1="290" y1="105" x2="345" y2="165"/>
                        <line x1="290" y1="105" x2="240" y2="155"/>
                        <line x1="345" y1="112" x2="405" y2="120"/>
                        <line x1="345" y1="112" x2="345" y2="165"/>
                        <line x1="405" y1="120" x2="345" y2="165"/>
                        <line x1="405" y1="120" x2="435" y2="168"/>
                        <line x1="345" y1="165" x2="395" y2="185"/>
                        <line x1="345" y1="165" x2="355" y2="235"/>
                        <line x1="345" y1="165" x2="240" y2="155"/>
                        <line x1="395" y1="185" x2="435" y2="168"/>
                        <line x1="395" y1="185" x2="455" y2="215"/>
                        <line x1="395" y1="185" x2="355" y2="235"/>
                        <line x1="435" y1="168" x2="455" y2="215"/>
                        <line x1="455" y1="215" x2="410" y2="248"/>
                        <line x1="455" y1="215" x2="495" y2="255"/>
                        <line x1="455" y1="215" x2="435" y2="290"/>
                        <line x1="410" y1="248" x2="355" y2="235"/>
                        <line x1="410" y1="248" x2="435" y2="290"/>
                        <line x1="495" y1="255" x2="435" y2="290"/>
                        <line x1="355" y1="235" x2="435" y2="290"/>
                        <line x1="435" y1="290" x2="420" y2="335"/>
                        <line x1="240" y1="155" x2="355" y2="235"/>
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

                    <!-- City Nodes -->
                    <g style="cursor:pointer" onclick="selectSector('ZAKHO (زاخۆ)')">
                        <circle cx="255" cy="68" r="8" fill="#00e5ff" stroke="#000" stroke-width="2" filter="url(#neonBlur)"/>
                        <circle cx="255" cy="68" r="3" fill="#ffffff"/>
                        <text x="235" y="48" fill="#00e5ff" font-size="10.5" font-weight="900" font-family="monospace">زاخۆ ZAKHO</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('DUHOK (دهۆک)')">
                        <circle cx="290" cy="105" r="9" fill="#00ff88" stroke="#000" stroke-width="2" filter="url(#neonBlur)"/>
                        <circle cx="290" cy="105" r="4" fill="#ffffff"/>
                        <text x="175" y="100" fill="#00ff88" font-size="11" font-weight="900">دهۆک DUHOK</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('AKRE (ئاکرێ)')">
                        <circle cx="345" cy="112" r="7" fill="#00e5ff" stroke="#000" stroke-width="1.8"/>
                        <circle cx="345" cy="112" r="2.5" fill="#ffffff"/>
                        <text x="325" y="94" fill="#a7f3d0" font-size="10" font-weight="bold">ئاکرێ</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('SORAN (سۆران)')">
                        <circle cx="405" cy="120" r="8" fill="#00ff88" stroke="#000" stroke-width="1.8" filter="url(#neonBlur)"/>
                        <circle cx="405" cy="120" r="3" fill="#ffffff"/>
                        <text x="420" y="112" fill="#00ff88" font-size="10.5" font-weight="900">سۆران</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('ERBIL (هەولێر)')">
                        <circle cx="345" cy="165" r="13" fill="none" stroke="#00e5ff" stroke-width="2" stroke-dasharray="3,3" opacity="0.8"/>
                        <circle cx="345" cy="165" r="10" fill="#00ff88" stroke="#ffffff" stroke-width="2.5" filter="url(#neonBlur)"/>
                        <circle cx="345" cy="165" r="4.5" fill="#ffffff"/>
                        <text x="260" y="153" fill="#00ff88" font-size="12" font-weight="900">هەولێر ERBIL</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('KOYA (کۆیە)')">
                        <circle cx="395" cy="185" r="7" fill="#00e5ff" stroke="#000" stroke-width="1.8"/>
                        <circle cx="395" cy="185" r="2.5" fill="#ffffff"/>
                        <text x="375" y="210" fill="#a7f3d0" font-size="10" font-weight="bold">کۆیە</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('RANYA (ڕانیە)')">
                        <circle cx="435" cy="168" r="8" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="435" cy="168" r="3" fill="#ffffff"/>
                        <text x="450" y="162" fill="#00ff88" font-size="10.5" font-weight="900">ڕانیە</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('SULAYMANIYAH (سلێمانی)')">
                        <circle cx="455" cy="215" r="10" fill="#00e5ff" stroke="#000" stroke-width="2" filter="url(#neonBlur)"/>
                        <circle cx="455" cy="215" r="4" fill="#ffffff"/>
                        <text x="475" y="222" fill="#00e5ff" font-size="11" font-weight="900">سلێمانی</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('CHAMCHAMAL (چەمچەماڵ)')">
                        <circle cx="410" cy="248" r="7" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="410" cy="248" r="2.5" fill="#ffffff"/>
                        <text x="365" y="275" fill="#a7f3d0" font-size="9.5" font-weight="bold">چەمچەماڵ</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('KIRKUK (کەرکوک)')">
                        <circle cx="355" cy="235" r="10" fill="#00e5ff" stroke="#00ff88" stroke-width="2.2" filter="url(#neonBlur)"/>
                        <circle cx="355" cy="235" r="4" fill="#ffffff"/>
                        <text x="270" y="248" fill="#00e5ff" font-size="11" font-weight="900">کەرکوک</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('HALABJA (هەڵەبجە)')">
                        <circle cx="495" cy="255" r="8" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="495" cy="255" r="3" fill="#ffffff"/>
                        <text x="510" y="265" fill="#00ff88" font-size="10.5" font-weight="900">هەڵەبجە</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('KALAR (کەلار - گەرمیان)')">
                        <circle cx="435" cy="290" r="8" fill="#00e5ff" stroke="#000" stroke-width="1.8"/>
                        <circle cx="435" cy="290" r="3" fill="#ffffff"/>
                        <text x="450" y="305" fill="#00e5ff" font-size="10.5" font-weight="900">کەلار</text>
                    </g>
                    <g style="cursor:pointer" onclick="selectSector('KHANAQIN (خانەقین)')">
                        <circle cx="420" cy="335" r="7" fill="#00ff88" stroke="#000" stroke-width="1.8"/>
                        <circle cx="420" cy="335" r="2.5" fill="#ffffff"/>
                        <text x="435" y="352" fill="#a7f3d0" font-size="10" font-weight="bold">خانەقین</text>
                    </g>
                    <!-- Regional Iraqi Nodes -->
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
<div id="familyTreeModal" class="modal-overlay">
    <div class="tree-modal-box" style="max-width: 960px; padding: 12px 14px 18px;">
        <div class="modal-common-header" style="margin-bottom: 10px; padding-bottom: 6px;">
            <div class="modal-common-title" style="font-size: 13px;">فایلی زانیاری خێزان و بنەماڵە</div>
            <div style="display:flex; gap:6px; align-items:center;">
                <button type="button" class="db-top-btn db-back-main-btn" onclick="closeFamilyTreeModal()" style="padding: 4px 10px; font-size: 11px;">گەڕانەوە ➔</button>
                <button type="button" class="modal-close-btn" onclick="closeFamilyTreeModal()" style="width: 24px; height: 24px; font-size: 12px;">✕</button>
            </div>
        </div>
        <div class="tree-inner-frame" style="padding: 10px 8px;">
            <div class="tree-role-tag" style="font-size: 10px; padding: 2px 10px; margin-bottom: 6px;">فایلی زانیاری تەواوی خێزان و بنەماڵە</div>

            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; max-width: 720px; margin: 0 auto;">
                <div class="parent-node-card" style="max-width: 100%; margin: 0; padding: 10px; gap: 8px;">
                    <div class="node-avatar-circle" style="width: 40px; height: 40px; min-width: 40px;"><div class="node-avatar-inner-sq" style="width: 16px; height: 16px;"></div></div>
                    <div class="parent-info-col" style="text-align: right;">
                        <div class="node-name-head" id="modalFatherName" style="font-size: 12.5px; margin-bottom: 2px;">محسن نجم (باوک - سەرۆکی خێزان)</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• باوک: نجم صادق | دایک: نجبة</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• پیشە: فەرمانبەر | تەمەن: 61 | گرووپی خوێن: O+</div>
                        <div class="node-detail-line" style="font-size: 9.5px; color: #34d399; font-weight: bold;">• مووچەی مانگانە: 1,250,000 دینار</div>
                        <div class="node-detail-line" style="font-size: 9.5px; color: #38bdf8;">• ناونیشان: هەولێر - بەختیاری - کۆڵانی 14</div>
                        <div class="node-bottom-badges" style="margin-top: 4px; gap: 4px;">
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">لەدایک: 1965</span>
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">ناسنامە: 1965482910</span>
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">خێزاندار</span>
                        </div>
                    </div>
                </div>

                <div class="parent-node-card" style="max-width: 100%; margin: 0; padding: 10px; gap: 8px;">
                    <div class="node-avatar-circle" style="width: 40px; height: 40px; min-width: 40px;"><div class="node-diamond" style="width: 14px; height: 14px;"></div></div>
                    <div class="parent-info-col" style="text-align: right;">
                        <div class="node-name-head" id="modalMotherName" style="font-size: 12.5px; margin-bottom: 2px;">زينة حسين (دایک - هاوسەر)</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• باوک: حسين طاهر | دایک: خديجة</div>
                        <div class="node-detail-line" style="font-size: 9.5px; margin-bottom: 1px;">• پیشە: ماڵدار | تەمەن: 58 | گرووپی خوێن: A+</div>
                        <div class="node-detail-line" style="font-size: 9.5px; color: #9ca3af;">• مووچەی مانگانە: نەبوو (خانەنشینی خێزان)</div>
                        <div class="node-detail-line" style="font-size: 9.5px; color: #38bdf8;">• ناونیشان: هەولێر - بەختیاری</div>
                        <div class="node-bottom-badges" style="margin-top: 4px; gap: 4px;">
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">لەدایک: 1968</span>
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">ناسنامە: 1968591024</span>
                            <span class="mini-badge-box" style="font-size: 8.5px; padding: 1px 5px;">خێزاندار</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="tree-connector-line" style="height: 18px; margin-top: 6px;"></div>
            <div class="tree-middle-badge" style="font-size: 9.5px; padding: 1px 10px;">منداڵان (٦ منداڵ - زانیاری تەواو، پیشە، مووچە و باری ژیان)</div>
            <div class="tree-connector-line" style="height: 12px;"></div>

            <div class="children-cards-row" style="display: grid !important; grid-template-columns: repeat(3, 1fr) !important; gap: 8px !important; margin-top: 6px !important;">
                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">لاوند محسن (کوڕ)</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: ئەندازیاری شارستانی</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: خێزاندار | تەمەن: 34</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 950,000 د.ع</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #38bdf8;">• تەلەفۆن: 0750 412 8931</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 1992</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">لە ژیاندا</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">هوشمند محسن (کوڕ)</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: پزیشکی گشتی</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: خێزاندار | تەمەن: 32</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 1,800,000 د.ع</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #38bdf8;">• تەلەفۆن: 0770 195 4420</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 1994</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">لە ژیاندا</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">کارمند محسن (کوڕ)</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: مامۆستای ئامادەیی</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: سەڵت | تەمەن: 29</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 750,000 د.ع</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #38bdf8;">• تەلەفۆن: 0751 883 2019</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 1997</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">لە ژیاندا</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start;">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">شيرين محسن (کچ)</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: فەرمانبەری حکومی</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: خێزاندار | تەمەن: 31</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #34d399; font-weight: bold;">• مووچە: 650,000 د.ع</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #38bdf8;">• تەلەفۆن: 0771 902 3314</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 1995</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">لە ژیاندا</span>
                        </div>
                    </div>
                </div>

                <div class="child-node-card" style="padding: 8px; gap: 6px; min-height: 130px; align-items: flex-start; border-color: #ef4444; background: rgba(127,29,29,0.15);">
                    <div class="node-avatar-circle" style="width: 34px; height: 34px; min-width: 34px;"><div class="node-diamond" style="width: 12px; height: 12px;"></div></div>
                    <div class="parent-info-col" style="text-align: right; flex: 1;">
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px; color:#fca5a5;">فريشتة محسن (کچ)</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: دەرچووی زانکۆ</div>
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
                        <div class="node-name-head" style="font-size: 11.5px; margin-bottom: 2px;">روند محسن (کچ)</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• پیشە: قوتابی زانکۆ</div>
                        <div class="node-detail-line" style="font-size: 8.5px;">• دۆخ: سەڵت | تەمەن: 20</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #facc15;">• مووچە: نەبوو (قوتابی)</div>
                        <div class="node-detail-line" style="font-size: 8.5px; color: #38bdf8;">• تەلەفۆن: 0750 714 6205</div>
                        <div class="node-bottom-badges" style="margin-top: 3px; gap: 3px;">
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px;">لەدایک: 2006</span>
                            <span class="mini-badge-box" style="font-size: 7.5px; padding: 1px 4px; color:#34d399;">لە ژیاندا</span>
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
            dropdown: { label: "• هەڵبژاردنی پارێزگا", options: ["-- هەڵبژاردنی پارێزگا --", "هەولێر (Erbil)", "سلێمانی (Sulaymaniyah)", "دهۆک (Duhok)", "کەرکوک (Kirkuk)", "هەڵەبجە (Halabja)", "بەغدا (Baghdad)", "بەسرە (Basrah)", "نینووا / مووسڵ (Nineveh)", "ئەنبار (Anbar)", "دیالە (Diyala)", "سەلاحەدین (Salahaddin)", "بابل (Babylon)", "کەربەلا (Karbala)", "نەجەف (Najaf)", "واسیت (Wasit)", "مەیسان (Maysan)", "ذی قار (Dhi Qar)", "موسەنا (Muthanna)", "قادسیە (Qadisiyah)", "گەرمیان و راپەڕین (Garmian)"], defaultVal: "هەولێر [Erbil]" },
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

    function cleanInput(str) {
        if (!str) return '';
        let s = str.replace(/[​-‍‎‏‪-‮﻿]/g, '').trim();
        const ar = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
        const fa = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
        for (let i = 0; i < 10; i++) {
            s = s.split(ar[i]).join(i.toString()).split(fa[i]).join(i.toString());
        }
        return s;
    }

    function submitRegister(e) {
        e.preventDefault();
        const u = cleanInput(document.getElementById('regUser').value);
        const p1 = cleanInput(document.getElementById('regPass1').value);
        const p2 = cleanInput(document.getElementById('regPass2').value);
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

        const adminUser = "Kurdistan01#001_##0101";
        const adminPass = "Oner_admin_01_King_001";

        if (!u || !p) {
            if (r) {
                r.textContent = 'تکایە هەردوو خانەی ناوی بەکارهێنەر و وشەی نهێنی پڕبکەرەوە!';
                r.classList.add('show');
            }
            return;
        }

        // Strict Admin Check
        if (u === adminUser && p === adminPass) {
            currentLoggedInUser = 'Kurdistan01';
            startFaceID('Kurdistan01', 'OWNER / MASTER');
            return;
        }

        // Check registered accounts database
        const acc = accountsDB[u.toLowerCase()];
        if (acc) {
            if (acc.password !== p) {
                if (r) {
                    r.textContent = 'وشەی نهێنی (پاسۆرد) هەڵەیە! تکایە دووبارە هەوڵ بدە.';
                    r.classList.add('show');
                }
                return;
            }
            if (!acc.approved) {
                if (r) {
                    r.textContent = 'تکایە چاوەڕێبە تا ئەدمین قبوڵت دەکات بۆ چونە ژورەوەی سیستەمی چاوی تاریکی هەڵۆ';
                    r.classList.add('show');
                }
                return;
            }
            currentLoggedInUser = acc.username;
            startFaceID(acc.username, 'USER (' + acc.planLabel + ')');
            return;
        }

        // If not found or incorrect
        if (r) {
            r.textContent = 'ناوی بەکارهێنەر یان وشەی نهێنی هەڵەیە! ڕێگەت پێنادرێت بچیتە ژوورەوە.';
            r.classList.add('show');
        }
    }

    function setupDashboardUserUI(usernameDisplay, roleType) {
        document.getElementById('tacticalUsernameDisplay').textContent = usernameDisplay;
        document.getElementById('tacticalRolePill').textContent = roleType.startsWith('OWNER') ? 'OWNER' : 'USER';
        document.getElementById('topRoleBadge').textContent = roleType;
        if (roleType.startsWith('OWNER')) {
            document.getElementById('activeUserBadge').textContent = '👑 KURDISTAN01 (بەڕێوەبەری گشتی)';
            document.getElementById('sessionRemainingBadge').textContent = '⏱ ماوە: هەمیشەیی';
        } else {
            document.getElementById('activeUserBadge').textContent = '👤 ' + usernameDisplay.toUpperCase();
        }
    }

    function startFaceID(displayUser, roleLabel) {
        switchView('faceIdView');
        const video = document.getElementById('webcamVideo');
        const status = document.getElementById('faceScanStatus');
        status.textContent = 'کردنەوەی کامێرا و سکانی بایۆمێتریک...';
        status.style.color = '#00e5ff';

        if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
            navigator.mediaDevices.getUserMedia({ video: true })
                .then(stream => {
                    faceStreamRef = stream;
                    video.srcObject = stream;
                })
                .catch(err => {});
        }

        setTimeout(() => {
            status.textContent = 'سکانکردنی ڕووخسار دەستی پێکرد... تکایە سەیری کامێراکە بکە';
            status.style.color = '#facc15';
        }, 1200);

        setTimeout(() => {
            status.textContent = 'شیکردنەوەی داتای بایۆمێتریک و دڵنیابوونەوە لە ڕووخسار...';
            status.style.color = '#00e5ff';
        }, 2800);

        setTimeout(() => {
            status.textContent = '✓ ناسنامە و مۆڵەت بە سەرکەوتوویی سەلمێندرا!';
            status.style.color = '#00ff88';
        }, 4400);

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

        let logsHtml = userSearchLogs.length > 0 ? `
            <div style="margin-top:20px; border-top:1px solid #334155; padding-top:15px; text-align:right;">
                <div style="font-size:14px; font-weight:850; color:#34d399; margin-bottom:10px;">📋 تۆماری گەڕان و چالاکییەکانی بەکارهێنەران:</div>
                ${userSearchLogs.map(l => `
                    <div style="background:#04070d; border:1px solid #10b981; border-radius:8px; padding:10px 12px; margin-bottom:8px; font-size:11.5px;">
                        <div style="color:#38bdf8; font-weight:bold;">بەکارهێنەر: <span style="color:#ffffff;">${l.username}</span> | بنکە: <span style="color:#facc15;">${l.dbName}</span></div>
                        <div style="color:#9ca3af; margin-top:3px;">کاتی سێرچ: ${l.time}</div>
                    </div>
                `).join('')}
            </div>
        ` : '';

        container.innerHTML = (requestsHtml || '<div style="color:#9ca3af; text-align:center; padding:15px;">هیچ داواکارییەکی نوێ نییە.</div>') + logsHtml;
    }

    function approveUserWithPlan(userKey, planCode) {
        const acc = accountsDB[userKey];
        if (!acc) return;
        acc.approved = true;
        acc.planLabel = planCode === '30D' ? '٣٠ ڕۆژ' : (planCode === '60D' ? '٦٠ ڕۆژ' : (planCode === '1Y' ? '١ ساڵ' : 'هەمیشەیی'));
        renderAdminPortalRequests();
        showToast(`✓ هەژماری (${acc.username}) چالاککرا!`);
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
            dropArea.innerHTML = `<label class="db-dropdown-label">${cfg.dropdown.label}</label><select id="dbSubSelect" class="db-dropdown-select">${cfg.dropdown.options.map(opt => `<option value="${opt}">${opt}</option>`).join('')}</select>`;
        } else { dropArea.style.display = 'none'; dropArea.innerHTML = ''; }

        const fieldsGrid = document.getElementById('dynamicFieldsGrid');
        fieldsGrid.innerHTML = cfg.fields.map(f => `
            <div class="db-field-card">
                <label class="db-field-label">• ${f.label}</label>
                <input type="text" id="${f.id}" data-label="${f.label}" class="db-field-input" placeholder="${f.ph}">
            </div>
        `).join('');

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

        userSearchLogs.unshift({
            username: currentLoggedInUser || 'Guest',
            dbName: currentActiveDbTitle,
            time: new Date().toLocaleString()
        });

        document.getElementById('insideDbSubView').style.display = 'none';
        const scanBox = document.getElementById('cyberScanSubView');
        scanBox.classList.add('active');
        setTimeout(() => {
            scanBox.classList.remove('active');
            renderSecretResults(enteredValues);
            document.getElementById('secretResultsSubView').classList.add('active');
        }, 700);
    }

    function openFamilyTreeModal(personName, fatherName, motherName) {
        if (personName) {
            document.getElementById('modalFatherName').textContent = `${personName} (${fatherName || 'باوک'})`;
            document.getElementById('modalMotherName').textContent = `${motherName || 'دایک'} (هاوسەر)`;
        }
        document.getElementById('familyTreeModal').classList.add('open');
    }
    function closeFamilyTreeModal() { document.getElementById('familyTreeModal').classList.remove('open'); }
    function openMeterMapModal(name, acc, lat, lng) {
        document.getElementById('mapMeterName').textContent = name || 'محمد احمد محمد';
        document.getElementById('mapMeterAcc').textContent = acc || '63179260572';
        document.getElementById('mapMeterLat').textContent = lat || '36.18416794';
        document.getElementById('mapMeterLng').textContent = lng || '44.03849821';
        
        // Dynamic landmark description based on coordinates
        const landmarks = [
            'هەولێر - نزیک پارکی سامێ - کۆڵانی 14',
            'سلێمانی - نزیک سەرچنار - شەقامی سەرەکی',
            'دهۆک - نزیک باژێر سەنتەر - بازاڕی کۆن',
            'کەرکوک - گەڕەکی شۆڕش - نزیک مزگەوت'
        ];
        const landmark = landmarks[Math.floor(Math.random() * landmarks.length)];
        
        // Add IP & Landmark details inside meter-info-card if element exists
        const infoCard = document.querySelector('.meter-info-card');
        if (infoCard) {
            infoCard.innerHTML = `
                <div><strong>ناوی بەشداربوو:</strong> <span id="mapMeterName">${name || 'محمد احمد محمد'}</span></div>
                <div><strong>ژمارەی ئەکاونت:</strong> <span id="mapMeterAcc">${acc || '63179260572'}</span></div>
                <div><strong>هێڵی پانی (Lat):</strong> <span id="mapMeterLat">${lat || '36.18416794'}</span></div>
                <div><strong>هێڵی درێژی (Lng):</strong> <span id="mapMeterLng">${lng || '44.03849821'}</span></div>
                <div><strong>🌐 ناونیشانی IP ی ماڵەوە:</strong> <span style="color:#fde047; font-family:monospace;">185.87.131.45 (Korek 4G)</span></div>
                <div><strong>📍 دەقیقی ماڵەکە (نزیک لە):</strong> <span style="color:#34d399;">${landmark}</span></div>
                <div><strong>دۆخ:</strong> <span style="color:#10b981;font-weight:bold;">مۆڵەتدار و جێگیرکراو ✓</span></div>
            `;
        }

        document.getElementById('meterMapIframe').src = `https://maps.google.com/maps?q=${lat || '36.18416794'},${lng || '44.03849821'}&hl=ckb&z=17&output=embed`;
        document.getElementById('meterMapModal').classList.add('open');
    }
    function closeMeterMapModal() { document.getElementById('meterMapModal').classList.remove('open'); }
    function openBioModal() { document.getElementById('bioModal').classList.add('open'); }
    function closeBioModal() { document.getElementById('bioModal').classList.remove('open'); }

    function triggerAction(actionName, recordNo) {
        if (actionName === 'pdf') showToast(`✓ فایلی PDF ی تۆماری #${recordNo} دابەزێنرا!`);
        else if (actionName === 'csv') showToast(`✓ فایلی CSV ی تۆماری #${recordNo} دابەزێنرا!`);
        else if (actionName === 'bookmark') showToast(`⭐ تۆماری #${recordNo} خزنکرا بۆ دڵخوازەکان!`);
    }

    function renderSecretResults(vals) {
        const container = document.getElementById('recordsListContainer');
        const countEl = document.getElementById('totalRecordsFoundText');
        const pageEl = document.getElementById('pageRecordsText');

        let qFirst = (vals['c_name1'] || vals['p_name1'] || vals['pen_n1'] || vals['v_name1'] || vals['ct_n1'] || vals['p_name1'] || '').trim();
        let qFather = (vals['c_name2'] || vals['p_name2'] || vals['pen_n2'] || vals['v_name2'] || vals['ct_n2'] || vals['k_father'] || '').trim();
        let qGrandpa = (vals['c_name3'] || vals['p_name3'] || vals['pen_n3'] || vals['v_name3'] || vals['ct_n3'] || vals['k_grandpa'] || '').trim();
        let qFull = (vals['p_fullname'] || vals['ct_full'] || vals['e_name'] || vals['g_name'] || vals['f_driver'] || '').trim();
        let qPhone = (vals['pen_phone'] || vals['m_phone'] || vals['h_phone'] || vals['fb_phone'] || vals['f_phone'] || vals['p_phone'] || vals['g_phone'] || '').trim();
        let qPlate = (vals['f_plate'] || '').trim();
        let qMeter = (vals['e_meter'] || vals['e_acc'] || '').trim();
        let qBirth = (vals['c_birth'] || vals['p_birth'] || vals['v_birth'] || '').trim();
        let qMother = (vals['c_mother'] || vals['p_mother'] || vals['ct_mother'] || vals['p_mother'] || '').trim();
        let qId = (vals['c_id'] || vals['p_id'] || vals['v_person_id'] || vals['pen_nat'] || vals['g_id'] || '').trim();

        if (qFull && !qFirst) {
            const parts = qFull.split(/\s+/);
            qFirst = parts[0] || '';
            if (parts[1]) qFather = parts[1];
            if (parts[2]) qGrandpa = parts[2];
        }

        const defFirst = qFirst || 'محمد';
        const defFather = qFather || 'احمد';
        const defGrandpa = qGrandpa || 'محمد';

        const clanNames = ['عەلی', 'کەریم', 'حسێن', 'ساڵح', 'قادر', 'رەشید', 'مستەفا', 'عەبدوڵڵا', 'تەها', 'فەتاح', 'خالید', 'عوسمان'];
        const mothersList = ['فاتمە مەحمود', 'ئامینە عەلی', 'خەدیجە تاهیر', 'نەجیبە حسێن', 'زەینەب رەشید', 'پەروین کەریم', 'سوعاد ساڵح', 'بەهزاد رەحمان', 'گەلاوێژ ئەحمەد', 'عائیشە قادر', 'شەرمین عوسمان', 'شیرین مەولود'];
        const grandmasList = ['گەلاوێژ', 'مەنیجە', 'رەعنا', 'مینا', 'تەوار', 'خاوەر', 'عائیشە', 'حەلیمە', 'فەهیمە', 'بەسیێ', 'نەرمین', 'خانزاد'];
        const yearsList = [1978, 1982, 1985, 1988, 1991, 1994, 1996, 1999, 2001, 1974, 1980, 1993];
        const jobsList = ['فەرمانبەری دەوڵەت', 'کاسب / بازرگان', 'مامۆستا', 'ئەندازیاری شارستانی', 'پزیشکی گشتی', 'ئەفسەری پێشمەرگە', 'پارێزەر', 'ژمێریار', 'کارمەندی کەرتی تایبەت', 'مامۆستای زانکۆ', 'شۆفێری تاکسی', 'کارمەندی تەندروستی'];
        const maritalList = ['خێزاندار', 'خێزاندار', 'سەڵت', 'خێزاندار', 'سەڵت', 'خێزاندار', 'خێزاندار', 'سەڵت', 'خێزاندار', 'خێزاندار', 'سەڵت', 'خێزاندار'];
        const citiesList = ['هەولێر (Erbil)', 'سلێمانی (Sulaymaniyah)', 'دهۆک (Duhok)', 'کەرکوک (Kirkuk)', 'هەڵەبجە (Halabja)', 'بەغدا (Baghdad)', 'بەسرە (Basrah)', 'نینووا / مووسڵ (Nineveh)', 'ئەنبار (Anbar)', 'دیالە (Diyala)', 'سەلاحەدین (Salahaddin)', 'بابل (Babylon)', 'کەربەلا (Karbala)', 'نجەف (Najaf)', 'واسیت (Wasit)', 'مەیسان (Maysan)', 'ذی قار (Dhi Qar)', 'موسەنا (Muthanna)', 'قادسیە (Qadisiyah)', 'گەرمیان و راپەڕین (Garmian)'];
        const neighborhoodsList = [
            'بەختیاری - کۆڵانی 14', 'سەرچنار - گەڕەکی شۆڕش', 'ماسیکێ - شەقامی زانکۆ', 'ڕەحیماوا - نزیک بازاڕ',
            'کانی ئاسکان - کۆڵانی 8', 'شەهیدان - شەقامی سەرەکی', 'ئاشتی - گەڕەکی 104', 'شۆڕش - کۆڵانی 21',
            'مامۆستایان - کۆڵانی 5', 'ئازادی - نزیک قوتابخانە', 'برایەتی - شەقامی گشتی', 'نەورۆز - کۆڵانی 12'
        ];
        const phoneList = ['0750 412 8931', '0770 195 4420', '0751 883 2019', '0771 902 3314', '0750 714 6205', '0770 821 7739', '0751 409 1182', '0772 315 9064', '0750 994 2271', '0770 551 8820', '0751 229 6610', '0771 440 8593'];

        const numRecords = 10;
        countEl.textContent = `• کۆی تۆمارەکانی دۆزراوە: ${numRecords} ناو (تۆمار)`;
        pageEl.textContent = `لاپەڕە 1 لە 1`;

        let cardsHtml = '';
        const db = currentActiveDbTitle;

        
        
        for (let i = 0; i < numRecords; i++) {
            const recNum = String(i + 1).padStart(4, '0');
            const firstName = defFirst;
            const fatherName = defFather;
            const grandpaName = defGrandpa;
            const forthName = clanNames[i % clanNames.length];
            const motherName = qMother || mothersList[i % mothersList.length];
            const grandmaName = grandmasList[i % grandmasList.length];
            
            // Consistent birth year and matching exact date & age
            const validYears = [1995, 1998, 2000, 2002, 1992, 1988, 2004, 1997, 1990, 2001];
            const birthYear = qBirth ? parseInt(qBirth) : validYears[i % validYears.length];
            const exactDob = `0${(i % 9) + 1}/0${(i % 4) + 1}/${birthYear}`;
            const ageCalc = 2026 - birthYear;

            const job = jobsList[i % jobsList.length];
            const marital = maritalList[i % maritalList.length];
            const city = citiesList[i % citiesList.length];
            const neighborhood = neighborhoodsList[i % neighborhoodsList.length];
            const phone = qPhone ? (i === 0 ? qPhone : phoneList[i % phoneList.length]) : phoneList[i % phoneList.length];
            const natId = qId ? (i === 0 ? qId : `19${String(birthYear).slice(-2)}${482910 + i * 37}`) : `19${String(birthYear).slice(-2)}${482910 + i * 37}`;
            const familyNo = `5${29104 + i * 83}`;
            const seqNo = (i + 1).toString();
            const rcNo = `6${19200 + i * 14} / 09`;

            const ipAddress = `185.${80 + (i * 7)}.${120 + (i * 11)}.${44 + i}`;
            const isps = ['Korek Telecom 4G', 'Asiacell 4G LTE', 'Fastlink 5G', 'Newroz Telecom FTTH'];
            const isp = isps[i % isps.length];
            const latVal = (36.184167 + (i * 0.0035)).toFixed(6);
            const lngVal = (44.038498 + (i * 0.0028)).toFixed(6);

            let fieldsHtml = `
                <div class="record-cell highlight"><span class="record-cell-label">ناوی یەکەم / تەواو</span><div class="record-cell-val">${firstName} ${fatherName} ${grandpaName} ${forthName}</div></div>
                <div class="record-cell"><span class="record-cell-label">ناوی باوک و باپیر</span><div class="record-cell-val">${fatherName} ${grandpaName}</div></div>
                <div class="record-cell"><span class="record-cell-label">ناوی دایک و دایەپیر</span><div class="record-cell-val">${motherName} (${grandmaName})</div></div>
                <div class="record-cell"><span class="record-cell-label">📅 بەرواری لەدایکبوون و تەمەن</span><div class="record-cell-val" style="color:#fde047;">${exactDob} (تەمەن: ${ageCalc} ساڵ)</div></div>
                <div class="record-cell"><span class="record-cell-label">پیشە و کار</span><div class="record-cell-val">${job}</div></div>
                <div class="record-cell"><span class="record-cell-label">باری خێزانداری</span><div class="record-cell-val">${marital}</div></div>
                <div class="record-cell"><span class="record-cell-label">ژمارەی ناسنامە (کارت)</span><div class="record-cell-val">${natId}</div></div>
                <div class="record-cell"><span class="record-cell-label">ژمارەی خێزان و زنجیرە</span><div class="record-cell-val">${familyNo} - زنجیرە ${seqNo}</div></div>
                <div class="record-cell"><span class="record-cell-label">ژمارەی تەلەفۆن</span><div class="record-cell-val" style="color:#38bdf8;">${phone}</div></div>
                <div class="record-cell"><span class="record-cell-label">پارێزگا و ناونیشان</span><div class="record-cell-val">${city} - ${neighborhood}</div></div>
                <div class="record-cell highlight"><span class="record-cell-label">🌐 ناونیشانی IP ی ماڵەوە</span><div class="record-cell-val" style="color:#fde047; font-family:monospace;">${ipAddress} (${isp})</div></div>
                <div class="record-cell highlight"><span class="record-cell-label">📍 دەقیقی GPS (پانی و درێژی)</span><div class="record-cell-val" style="color:#34d399; font-family:monospace;">${latVal}, ${lngVal}</div></div>
            `;

            let extraButtons = `
                <button type="button" class="record-action-btn btn-highlight" onclick="openMeterMapModal('${firstName} ${fatherName}', '63179260572', '${latVal}', '${lngVal}')">🗺️ بینینی دەقیقی ماڵەکەی لەسەر نەخشە (GPS)</button>
                <button type="button" class="record-action-btn" onclick="openFamilyTreeModal('${firstName} ${fatherName} ${grandpaName}', '${fatherName}', '${motherName}')">📊 خێزان و منداڵەکان</button>
            `;

            let mapEmbedHtml = `
                <div style="margin-top: 14px; border: 1.5px solid #10b981; border-radius: 10px; overflow: hidden; background: #0c1017; box-shadow: 0 0 20px rgba(16,185,129,0.2);">
                    <div style="background: rgba(6, 78, 59, 0.4); padding: 6px 12px; font-size: 11px; font-weight: bold; color: #34d399; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #10b981;">
                        <span>📍 نەخشەی ڕاستەقینەی ماڵی کەسەکە (GPS Location)</span>
                        <span style="font-family: monospace; color: #00e5ff;">${latVal}, ${lngVal}</span>
                    </div>
                    <div style="width: 100%; height: 260px;">
                        <iframe width="100%" height="100%" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://maps.google.com/maps?q=${latVal},${lngVal}&hl=ckb&z=16&output=embed"></iframe>
                    </div>
                </div>
            `;

            cardsHtml += `
                <div class="record-master-card">
                    <div class="record-card-header">
                        <div class="record-num-title">تۆمار #${recNum}</div>
                        <span class="record-db-badge">${db}</span>
                    </div>
                    <div class="record-data-grid">
                        ${fieldsHtml}
                    </div>
                    ${mapEmbedHtml}
                    <div class="record-actions-bar" style="margin-top: 14px;">
                        ${extraButtons}
                        <button type="button" class="record-action-btn" onclick="triggerAction('bookmark', '${recNum}')">⭐ نیشانەکردن</button>
                        <button type="button" class="record-action-btn" onclick="triggerAction('pdf', '${recNum}')">📄 PDF داگرتنی</button>
                        <button type="button" class="record-action-btn" onclick="triggerAction('csv', '${recNum}')">📊 CSV داگرتنی</button>
                    </div>
                </div>
            `;
        }

        container.innerHTML = cardsHtml;
    }

</script>

</body>
</html>
