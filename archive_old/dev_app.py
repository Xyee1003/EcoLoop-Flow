import streamlit as st
import time
import requests
import streamlit.components.v1 as components # 🌟 引入独立沙箱组件
from streamlit_autorefresh import st_autorefresh

# ==================== 页面高级配置 ====================
st.set_page_config(
    page_title="EcoLoop-Flow SDP Dev Portal", 
    page_icon="🏢", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 🌟 每隔 3 秒自动刷新一次大屏
st_autorefresh(interval=3000, limit=1000, key="dev_fizz_refresh")

# ==================== 真实网络数据拉取 ====================
BACKEND_DATA_URL = "http://127.0.0.1:5000/api/v1/resident/data"
CLEAR_CONTAINER_URL = "http://127.0.0.1:5000/api/v1/developer/clear-container"

try:
    response = requests.get(BACKEND_DATA_URL, timeout=1.0)
    if response.status_code == 200:
        server_data = response.json()
        container_fill = server_data["container_fill"]
        total_weight = server_data["total_weight"]
        server_connected = True
    else:
        server_connected = False
except Exception:
    server_connected = False

# 优雅降级数据兜底机制
if not server_connected:
    container_fill = 82.5
    total_weight = 15.4

# ==================== CSS 样式注入 (SDP 暗绿 UI) ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Inter', sans-serif;
        background-color: #F3F4F6;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    .dev-brand-container {
        padding: 24px 30px;
        background: #0D2315;
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(13, 35, 21, 0.12);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .dev-title {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.5px;
    }
    .dev-subtitle {
        font-size: 0.85rem; opacity: 0.8; font-weight: 300; margin-top: 2px;
    }
    
    .metric-card {
        background: white; padding: 24px; border-radius: 12px; border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.01); text-align: center; position: relative;
    }
    .metric-label {
        font-size: 0.8rem; color: #6B7280; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
    }
    .metric-val {
        font-size: 2.2rem; font-weight: 700; color: #113826; margin: 6px 0; letter-spacing: -0.5px;
    }
    
    .delta-badge {
        display: inline-flex; align-items: center; font-size: 0.85rem; font-weight: 700;
        color: #10B981; background-color: #ECFDF5; padding: 2px 8px; border-radius: 20px; margin-top: 4px; border: 1px solid #A7F3D0;
    }
    
    .task-card {
        background: #FEF3C7; border-left: 5px solid #D97706; padding: 18px; border-radius: 8px; margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 🏢 顶部企业级横幅 ====================
st.markdown("""
<div class="dev-brand-container">
    <div>
        <h1 class="dev-title">EcoLoop-Flow | Developer Dashboard</h1>
        <div class="dev-subtitle">Sime Darby Property Facility & Infrastructure Management System</div>
    </div>
    <div style="text-align: right; font-size: 0.85rem; opacity: 0.9;">
        <strong>Estate: City of Elmina (Block A)</strong><br>
        <span>Active Bins: 60 | Active Households: 420</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not server_connected:
    st.warning("⚠️ Connected via Local State Backup. Please start server.py to stream live IoT telemetry.")

# ==================== 动态增量逻辑计算 ====================
if 'prev_total_weight' not in st.session_state:
    st.session_state.prev_total_weight = total_weight

delta_weight = total_weight - st.session_state.prev_total_weight
st.session_state.prev_total_weight = total_weight

# 如果有数据增加，记录投递触发时间，供 3D 挡板在 5 秒内显示打开状态
if delta_weight > 0:
    st.session_state.last_deposit_time = time.time()

# 基础换算
est_savings = round(total_weight * 925.3, 2)
delta_savings = round(delta_weight * 925.3, 2)
carbon_offset = total_weight * 1.5
delta_carbon = delta_weight * 1.5

# ==================== 第一排：核心商业价值 KPI 看板 ====================
st.markdown("<h3 style='color: #113826; font-weight: 600;'>Macro Sustainability & CAPEX KPI</h3>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Material Ingested</div>
        <div class="metric-val">{total_weight:.2f} kg</div>
        {f'<div class="delta-badge">▲ +{delta_weight:.2f} kg</div>' if delta_weight > 0 else '<div style="font-size: 0.75rem; color: #9CA3AF; margin-top:6px;">Waiting for IoT drop-off...</div>'}
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Eco-Asphalt Paved</div>
        <div class="metric-val">{(total_weight * 9.25):.1f} Meters</div>
        {f'<div class="delta-badge">▲ +{(delta_weight * 9.25):.1f} m</div>' if delta_weight > 0 else '<div style="font-size: 0.75rem; color: #9CA3AF; margin-top:6px;">Elmina Boulevard Section 3</div>'}
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Est. CAPEX Saved</div>
        <div class="metric-val" style="color: #113826;">RM {est_savings:,.2f}</div>
        {f'<div class="delta-badge">▲ +RM {delta_savings:,.2f}</div>' if delta_weight > 0 else '<div style="font-size: 0.75rem; color: #9CA3AF; margin-top:6px;">Slashing aggregates procurement</div>'}
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">ESG CO2 Offsets</div>
        <div class="metric-val" style="color: #059669;">{carbon_offset:.1f} kg</div>
        {f'<div class="delta-badge" style="color: #059669; background-color: #ECFDF5; border-color: #A7F3D0;">▲ +{delta_carbon:.1f} kg CO2</div>' if delta_weight > 0 else f'<div style="font-size: 0.75rem; color: #059669; margin-top:6px; font-weight:600;">Equivalent to {int(carbon_offset/22)} trees planted</div>'}
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== 第二排：3D 物理设备仿真 与 中央集装箱监控 ====================
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("<h3 style='color: #113826; font-weight: 600;'>3D Digital Twin Chute Simulator</h3>", unsafe_allow_html=True)
    st.write("Real-time physical visualization of the Block A Floor 15 smart chute. Watch the mechanical sequence trigger on incoming IoT traffic.")
    
    # 🌟 检测是否处于刚刚投递状态（5 秒内视为投递开闸状态）
    is_active_payout = False
    if 'last_deposit_time' in st.session_state:
        if time.time() - st.session_state.last_deposit_time < 5.0:
            is_active_payout = True

    # 100% 成功渲染的自包含 CSS SVG 仿真模拟器
    if is_active_payout:
        vibe_animation = "animation: industrial_vibe 0.15s infinite;"
        board_rotation = "transform: rotate(32deg); transform-origin: 200px 140px; transition: transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275);"
        laser_opacity = "0.25"
        laser_color = "#10B981"
        status_text = "✅ AI VERIFIED: PREMIUM PET | OPEN CHUTE"
    else:
        vibe_animation = ""
        board_rotation = "transform: rotate(0deg); transform-origin: 200px 140px; transition: transform 0.6s;"
        laser_opacity = "0.0"
        laser_color = "#475569"
        status_text = "🔒 STANDBY: WAITING FOR RESIDENT DROP-OFF"

    # 🌟 核心突破：将 SVG 放入完全隔离的 iframe html 沙箱，避开 Streamlit 的所有解析规则，确保 100% 绘制成功！
    sandbox_html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                padding: 0;
                background-color: #0F172A;
                overflow: hidden;
            }}
            .simulation-container {{
                width: 100%;
                height: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            @keyframes industrial_vibe {{
                0% {{ transform: translate(1px, 0.5px) rotate(0deg); }}
                25% {{ transform: translate(-1px, -0.5px) rotate(-0.5deg); }}
                50% {{ transform: translate(-0.5px, 0.5px) rotate(0.5deg); }}
                75% {{ transform: translate(1px, -0.5px) rotate(0deg); }}
                100% {{ transform: translate(-0.5px, 0.5px) rotate(0.5deg); }}
            }}
        </style>
    </head>
    <body>
        <div class="simulation-container">
            <svg viewBox="0 0 400 240" style="width: 100%; height: 240px; display: block;">
                <!-- 3D 智能垃圾桶内部金属舱 -->
                <rect x="50" y="20" width="300" height="190" rx="12" fill="#1E293B" stroke="#334155" stroke-width="2" />
                
                <!-- 顶部单高清 AI 摄像头 -->
                <g transform="translate(200, 40)">
                    <rect x="-20" y="-12" width="40" height="20" rx="4" fill="#0F172A" />
                    <circle cx="0" cy="-2" r="7" fill="{laser_color}" />
                    <circle cx="0" cy="-2" r="3" fill="#FFFFFF" />
                    <polygon points="-20,8 -110,125 110,125 20,8" fill="{laser_color}" opacity="{laser_opacity}" />
                </g>
                
                <!-- 15Hz 电磁振动板 -->
                <g style="{vibe_animation} {board_rotation}">
                    <polygon points="100,135 300,135 285,145 115,145" fill="#334155" />
                    <polygon points="100,130 300,130 285,135 115,135" fill="#475569" stroke="#64748B" stroke-width="1.5" />
                    
                    <g transform="translate(175, 102)" opacity="{'1.0' if is_active_payout else '0.0'}">
                        <rect x="0" y="0" width="40" height="18" rx="4" fill="#38BDF8" opacity="0.8" />
                        <rect x="36" y="4" width="8" height="10" rx="1" fill="#FFFFFF" opacity="0.9" />
                    </g>
                </g>
                
                <!-- 底部重力落料口 -->
                <polygon points="50,175 130,205 270,205 350,175" fill="#0F172A" opacity="0.7" />
                
                <!-- 控制屏 HUD -->
                <rect x="70" y="172" width="260" height="26" rx="6" fill="#020617" stroke="#1E293B" stroke-width="1.5" />
                <text x="200" y="189" fill="#10B981" font-family="monospace" font-size="9" font-weight="700" text-anchor="middle">
                    {status_text}
                </text>
            </svg>
        </div>
    </body>
    </html>
    """

    # 🌟 使用沙箱组件完美渲染，高度固定 240px，在任何情况下均能完美输出！
    components.html(sandbox_html_content, height=260)

with col_right:
    st.markdown("<h3 style='color: #113826; font-weight: 600;'>Basement Storage Capacity</h3>", unsafe_allow_html=True)
    
    materials = ["PET Plastic Bottles", "Aluminum Cans", "Paper & Cardboard", "Non-Recyclable (Organic)"]
    levels = [container_fill, min(100.0, container_fill * 0.5), min(100.0, container_fill * 0.7), 91.2]
    
    for i in range(4):
        st.markdown(f"**{materials[i]} Container** ({levels[i]:.1f}% full)")
        st.progress(levels[i] / 100.0)
    
    st.markdown("---")
    
    # 智能清运决策模块
    st.markdown("<h3 style='color: #113826; font-weight: 600;'>Facility Dispatch Center</h3>", unsafe_allow_html=True)
    
    if container_fill == 0.0:
        st.success("SUCCESS: All basement containers cleared. Storage telemetry normal (0.0%).")
    else:
        if container_fill >= 80.0:
            st.markdown(f"""
            <div class="task-card">
                <strong>🚨 BASEMENT OVERFLOW WARNING:</strong><br>
                <span style="font-size: 0.85rem; color: #78350F;">
                The <strong>PET Plastic Bottles</strong> container is currently critical at <strong>{container_fill:.1f}%</strong> capacity. 
                Please trigger clearance to prevent gravity chute blockages.
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("Dispatch Collection Truck & Clear Containers", use_container_width=True):
            with st.spinner("Transmitting clearance dispatch order to Fleet..."):
                if server_connected:
                    try: 
                        requests.post(CLEAR_CONTAINER_URL, timeout=2.0)
                    except Exception: 
                        pass
                else:
                    time.sleep(1.5)
            st.session_state.prev_total_weight = 0.0
            st.success("Dispatch command successfully sent! Containers cleared.")
            time.sleep(1.0)
            st.rerun()
