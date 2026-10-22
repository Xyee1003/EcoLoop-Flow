import streamlit as st
import requests
import streamlit.components.v1 as components
from streamlit_autorefresh import st_autorefresh

st.set_page_config(page_title="Node 1: EcoBin Simulator", page_icon="🗑️", layout="wide")
st_autorefresh(interval=1500, limit=5000, key="ecobin_refresh")

BRIDGE_URL = "http://127.0.0.1:5000/api"

try:
    res = requests.get(f"{BRIDGE_URL}/state", timeout=1.0)
    state = res.json()
    connected = True
except Exception:
    connected = False
    state = {
        "bin_id": "BIN EC-04",
        "machine_state": "IDLE",
        "latch_open": False,
        "shaker_active": False,
        "speaker_msg": "Offline - Please start server.py",
        "speaker_mode": "NORMAL",
        "load_cell_weight": 0.0,
        "purity": 100,
        "is_anomaly": False,
        "tray_items": [],
        "trigger_id": 0
    }

st.markdown("""
<style>
    html, body, [data-testid="stAppViewContainer"] { background-color: #0B132B; color: #FFFFFF; }
    .node-banner {
        background: linear-gradient(90deg, #1C2541 0%, #0F172A 100%);
        padding: 18px 24px; border-radius: 12px; border: 1px solid #3A506B;
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;
    }
    .sensor-box {
        background: #1C2541; padding: 18px; border-radius: 12px; border: 1px solid #3A506B;
        text-align: center; margin-bottom: 12px;
    }
    .sensor-title { font-size: 0.8rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 1px; }
    .sensor-value { font-size: 2rem; font-weight: 700; color: #5BC0BE; margin-top: 4px; }
    
    div.stButton > button {
        background-color: #1C2541 !important;
        color: #5BC0BE !important;
        border: 1px solid #3A506B !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        background-color: #3B82F6 !important;
        color: #FFFFFF !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="node-banner">
    <div>
        <h2 style="margin:0; color:#6FFFE9;">[ Node 1: EcoBin ] Hardware Simulator</h2>
        <span style="color:#94A3B8; font-size:0.9rem;">Latches & Shakers • Load Cell Weights • Speaker Alarms</span>
    </div>
    <div style="text-align:right;">
        <span style="background:#0F172A; padding:6px 12px; border-radius:8px; border:1px solid #5BC0BE; color:#6FFFE9; font-family:monospace;">
            BIN ID: {state['bin_id']} | STATE: {state['machine_state']}
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

col_sim, col_telemetry = st.columns([3, 2])

with col_sim:
    m_state = state["machine_state"]
    vibe_css = "animation: shake 0.12s infinite;" if state["shaker_active"] else ""
    board_rot = "transform: rotate(38deg);" if state["latch_open"] else "transform: rotate(0deg);"
    drop_anim = "transform: translateY(85px); opacity: 0; transition: all 1.2s ease-in;" if state["latch_open"] else "transform: translateY(0px); opacity: 1;"
    
    if m_state == "ALARM":
        hud_color = "#EF4444"
        laser_op = "0.35"
        # 🌟 精确区分液体残留还是有机污染
        if state["purity"] <= 50 and not state["is_anomaly"]:
            badge_text = "⚠️ LATCH LOCKED - LIQUID RESIDUE DETECTED"
        else:
            badge_text = "🚨 LATCH LOCKED - CONTAMINATION ALARM"
    elif m_state == "DROPPING":
        hud_color = "#10B981"
        laser_op = "0.3"
        badge_text = "🔓 TRIGGER OPEN - DROPPING TO GRAVITY CHUTE"
    elif m_state == "SCANNED":
        hud_color = "#F59E0B" if state["purity"] < 100 else "#3B82F6"
        laser_op = "0.25"
        badge_text = "⚡ 15Hz SHAKER ACTIVE - AWAITING USER CONFIRMATION"
    else:
        hud_color = "#64748B"
        laser_op = "0.0"
        badge_text = "🔒 TRIGGER CLOSED - STANDBY"

    has_items = "1.0" if len(state["tray_items"]) > 0 else "0.0"
    has_anomaly = "1.0" if state["is_anomaly"] else "0.0"

    sim_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        body {{ margin: 0; background: #0F172A; font-family: 'Segoe UI', sans-serif; color: white; overflow: hidden; }}
        .wrap {{ padding: 16px; border-radius: 14px; border: 2px solid {hud_color}; background: #090D16; }}
        @keyframes shake {{
            0% {{ transform: translate(2px, 1px); }}
            25% {{ transform: translate(-2px, -1px); }}
            50% {{ transform: translate(-2px, 1px); }}
            75% {{ transform: translate(2px, -1px); }}
            100% {{ transform: translate(0px, 0px); }}
        }}
        .speaker-bar {{
            margin-top: 12px; padding: 12px 16px; border-radius: 8px;
            background: #1E293B; border-left: 5px solid {hud_color};
            display: flex; align-items: center; justify-content: space-between;
            font-family: monospace; font-size: 13px;
        }}
    </style>
    </head>
    <body>
    <div class="wrap">
        <svg viewBox="0 0 500 270" style="width:100%; height:270px; display:block;">
            <rect x="40" y="15" width="420" height="235" rx="14" fill="#1E293B" stroke="#334155" stroke-width="3"/>
            
            <g transform="translate(250, 32)">
                <rect x="-28" y="-12" width="56" height="24" rx="6" fill="#0F172A" stroke="#475569"/>
                <circle cx="0" cy="0" r="8" fill="{hud_color}"/>
                <circle cx="0" cy="0" r="3" fill="#FFFFFF"/>
                <polygon points="-25,12 -140,145 140,145 25,12" fill="{hud_color}" opacity="{laser_op}"/>
            </g>

            <g style="{vibe_css}">
                <g style="{board_rot} transform-origin: 110px 150px; transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);">
                    <polygon points="100,145 400,145 385,158 115,158" fill="#334155"/>
                    <polygon points="100,138 400,138 385,145 115,145" fill="#64748B" stroke="#94A3B8" stroke-width="1"/>
                    <circle cx="110" cy="148" r="6" fill="#F59E0B"/>

                    <g style="{drop_anim}">
                        <g transform="translate(175, 110)" opacity="{has_items}">
                            <rect x="0" y="0" width="46" height="24" rx="5" fill="#38BDF8" opacity="0.85" stroke="#BAE6FD"/>
                            <rect x="44" y="6" width="9" height="12" rx="2" fill="#0284C7"/>
                        </g>
                        <g transform="translate(290, 112)" opacity="{has_items}">
                            <rect x="0" y="0" width="46" height="24" rx="5" fill="#38BDF8" opacity="0.85" stroke="#BAE6FD"/>
                            <rect x="44" y="6" width="9" height="12" rx="2" fill="#0284C7"/>
                        </g>
                        <g transform="translate(235, 105)" opacity="{has_anomaly}">
                            <path d="M5,28 Q20,0 40,28 Z" fill="#FACC15" stroke="#EF4444" stroke-width="2"/>
                        </g>
                    </g>
                </g>
            </g>

            <polygon points="45,195 140,245 360,245 455,195" fill="#090D16" opacity="0.85"/>
            
            <rect x="65" y="205" width="370" height="30" rx="6" fill="#020617" stroke="{hud_color}" stroke-width="1.5"/>
            <text x="250" y="225" fill="{hud_color}" font-family="monospace" font-size="11.5" font-weight="bold" text-anchor="middle">
                {badge_text}
            </text>
        </svg>

        <div class="speaker-bar">
            <span>🔊 <strong>SPEAKER OUTPUT:</strong> {state['speaker_msg']}</span>
            <button onclick="speakNow()" style="background:#3B82F6; color:white; border:none; padding:5px 10px; border-radius:4px; cursor:pointer;">
                🔈 Replay Audio
            </button>
        </div>
    </div>

    <script>
        const triggerId = "{state['trigger_id']}";
        const msg = "{state['speaker_msg']}";
        const mode = "{state['speaker_mode']}";

        function playBeep(freq, duration) {{
            try {{
                const ctx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.type = mode === "ALARM" ? "sawtooth" : "sine";
                osc.frequency.value = freq;
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.start();
                setTimeout(() => {{ osc.stop(); ctx.close(); }}, duration);
            }} catch(e) {{}}
        }}

        function speakNow() {{
            if (mode === "ALARM") playBeep(280, 400);
            else if (mode === "SUCCESS") playBeep(880, 200);
            else playBeep(520, 120);

            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                const utter = new SpeechSynthesisUtterance(msg);
                utter.lang = 'en-US';
                utter.rate = 1.05;
                window.speechSynthesis.speak(utter);
            }}
        }}

        if (triggerId !== "0" && sessionStorage.getItem("last_trigger") !== triggerId) {{
            sessionStorage.setItem("last_trigger", triggerId);
            speakNow();
        }}
    </script>
    </body>
    </html>
    """
    components.html(sim_html, height=365)

with col_telemetry:
    st.markdown(f"""
    <div class="sensor-box">
        <div class="sensor-title">⚖️ Load Cell Weight Sensor</div>
        <div class="sensor-value">{state['load_cell_weight']:.2f} kg</div>
    </div>
    <div class="sensor-box">
        <div class="sensor-title">🧪 AI Purity Coefficient</div>
        <div class="sensor-value" style="color: {'#EF4444' if state['purity']<=50 else '#10B981'};">
            {state['purity']}%
        </div>
    </div>
    <div class="sensor-box">
        <div class="sensor-title">⚙️ Actuator Telemetry</div>
        <div style="font-size:1rem; margin-top:8px; color:#E2E8F0;">
            Latch Solenoid: <strong>{'🔓 OPEN (38°)' if state['latch_open'] else '🔒 LOCKED (0°)'}</strong><br>
            15Hz Shaker Plate: <strong>{'⚡ VIBRATING' if state['shaker_active'] else '⏸️ IDLE'}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🔄 Manual Reset Bin / Clear Tray", use_container_width=True):
        try:
            requests.post(f"{BRIDGE_URL}/reset", timeout=1.0)
            st.rerun()
        except Exception:
            pass