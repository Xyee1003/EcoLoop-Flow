import streamlit as st
import time
import requests
from streamlit_autorefresh import st_autorefresh

# ==================== 页面高级配置 ====================
st.set_page_config(
    page_title="EcoLoop-Flow", 
    page_icon="🌱", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 🌟 核心同步大杀器：每隔 3 秒自动刷新一次网页拉取服务器最新状态
# 这样当 IoT 投递成功后，网页最多等 3 秒就会自动同步更新，无需手动刷新！
st.logo("https://i.imgur.com/vA1z43I.png", icon_image="https://i.imgur.com/vA1z43I.png")

# 使用 Streamlit 官方自带的定时执行组件
# 每 3000 毫秒（3秒）自动刷新一次状态
st_autorefresh(interval=3000, limit=1000, key="fizzbuzzcounter")

# ==================== 后端中转 API 配置 ====================
BACKEND_URL = "http://127.0.0.1:5000/api/v1/resident/data"
CASHOUT_URL = "http://127.0.0.1:5000/api/v1/resident/cashout"

try:
    response = requests.get(BACKEND_URL, timeout=1.5)
    if response.status_code == 200:
        server_data = response.json()
        # 🌟 核心修复：直接将服务器数据强制写入 session_state 缓存，确保双向绑定 🌟
        st.session_state.balance = server_data["balance"]
        st.session_state.total_weight = server_data["total_weight"]
        st.session_state.history = server_data["history"]
        st.session_state.container_fill = server_data["container_fill"]
        server_connected = True
    else:
        server_connected = False
except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
    server_connected = False

# 优雅降级数据兜底机制（服务器没启动时使用本地模拟数据）
if not server_connected:
    if 'balance' not in st.session_state: st.session_state.balance = 24.50
    if 'total_weight' not in st.session_state: st.session_state.total_weight = 15.4
    if 'history' not in st.session_state:
        st.session_state.history = [
            {"date": "2026-10-18", "type": "Aluminum Cans", "weight": 1.2, "earn": 3.60},
            {"date": "2026-10-19", "type": "PET Plastic Bottles", "weight": 2.5, "earn": 2.00},
            {"date": "2026-10-20", "type": "Paper & Cardboard", "weight": 5.4, "earn": 2.16}
        ]
    if 'container_fill' not in st.session_state: st.session_state.container_fill = 82.5

# ==================== 注入自定义 CSS 样式 (高端极简、极具现代感) ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FAFAF9; /* 极简米白 */
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    /* 头部企业级暗绿横幅 */
    .brand-container {
        text-align: center;
        padding: 32px 15px;
        background: #113826; /* Sime Darby 官方深森林绿 */
        border-radius: 16px;
        color: #F3F4F6;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(17, 56, 38, 0.08);
    }
    .brand-title {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: -1.5px;
        color: #FFFFFF !important;
    }
    .brand-subtitle {
        font-size: 0.9rem;
        opacity: 0.8;
        margin-top: 6px;
        font-weight: 300;
        letter-spacing: 0.5px;
    }

    /* 奢华钱包大卡片 */
    .wallet-card {
        background: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.01), 0 8px 24px rgba(0, 0, 0, 0.02);
        margin-bottom: 20px;
    }
    .wallet-header {
        font-size: 0.8rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .wallet-balance {
        font-size: 2.8rem;
        font-weight: 700;
        color: #113826;
        margin: 10px 0;
        letter-spacing: -1px;
    }
    
    /* 提现功能区域容器 */
    .payout-btn-container {
        background-color: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }

    /* 精美记录卡片 */
    .history-card {
        padding: 16px 20px;
        border-radius: 12px;
        background-color: white;
        margin-bottom: 12px;
        border: 1px solid #F3F4F6;
        box-shadow: 0 1px 2px rgba(0,0,0,0.01);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .history-left {
        display: flex;
        flex-direction: column;
    }
    .history-date {
        font-size: 0.75rem;
        color: #9CA3AF;
        font-weight: 500;
    }
    .history-material {
        font-size: 0.95rem;
        font-weight: 600;
        color: #111827;
        margin-top: 3px;
    }
    .history-weight {
        font-size: 0.8rem;
        color: #4B5563;
        margin-top: 1px;
    }
    .history-earn {
        font-size: 1.15rem;
        font-weight: 700;
        color: #113826;
    }

    /* 楼层排名行样式 */
    .leaderboard-row {
        background: white; 
        border-radius: 10px; 
        padding: 12px 16px; 
        margin-bottom: 8px; 
        border: 1px solid #E5E7EB; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
    }

    /* 地图地标详情卡片 */
    .map-pointer-card {
        background: white;
        border: 1px solid #E5E7EB;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        border-left: 4px solid #113826;
    }

    /* Tab 选项卡样式高级美化 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #F3F4F6;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 8px;
        border: none;
        background-color: transparent;
        color: #4B5563;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #113826 !important;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

# ==================== 📱 App 顶部企业横幅 ====================
st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">EcoLoop-Flow</h1>
    <div class="brand-subtitle">Smart Condo Micro-Payout & Utility Offset Network</div>
</div>
""", unsafe_allow_html=True)

if not server_connected:
    st.caption("ℹ️ *Running in Offline Demo Mode. Start server.py to connect to real smart bins.*")

# ==================== Tab 导航栏 ====================
tab1, tab2, tab3 = st.tabs(["Wallet & Offsets", "Scan & Drop", "Community Map"])

# ==================== TAB 1: 提现与账单抵扣 ====================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="wallet-card">
        <div class="wallet-header">EcoLoop Balance</div>
        <div class="wallet-balance">RM {st.session_state.balance:.2f}</div>
        <div style="color: #4B5563; font-size: 0.85rem; display: flex; justify-content: space-between; font-weight: 500;">
            <span>📍 Elmina Condo, Block A, Lvl 15</span>
            <span style="font-weight: 600; color: #113826;">Total Recycled: {st.session_state.total_weight:.1f} kg</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='color: #113826; margin-top: 10px; font-weight: 600;'>Select Payout Method</h4>", unsafe_allow_html=True)
    
    payout_channel = st.radio(
        "Choose where to send your recycling earnings:",
        [
            "Touch 'n Go eWallet (Instant Cashout)",
            "TNB / Syabas Bills (Offset Water & Electricity bills)",
            "F&B Merchant Vouchers (1.5x Value multiplier)"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("<div class='payout-btn-container'>", unsafe_allow_html=True)
    if "Touch 'n Go" in payout_channel:
        if st.button("Proceed Touch 'n Go Transfer", use_container_width=True):
            if st.session_state.balance > 0:
                with st.spinner("Connecting to secure TNG Merchant API..."):
                    if server_connected:
                        try: requests.post(CASHOUT_URL, timeout=2)
                        except requests.exceptions.RequestException: pass
                    else:
                        time.sleep(1.5)
                st.success(f"RM {st.session_state.balance:.2f} successfully credited to your Touch 'n Go Wallet.")
                st.session_state.balance = 0.00
                st.rerun()
            else: st.warning("Insufficient balance to withdraw.")
                
    elif "Bills" in payout_channel:
        utility_choice = st.selectbox("Select Utility Bill:", ["TNB (Electricity Bill) - Account: 2201992...", "Syabas (Water Bill) - Account: 9923018..."])
        if st.button(f"Apply Credit to {utility_choice.split()[0]}", use_container_width=True):
            if st.session_state.balance > 0:
                with st.spinner("Applying rebate to your next utility statement..."):
                    if server_connected:
                        try: requests.post(CASHOUT_URL, timeout=2)
                        except requests.exceptions.RequestException: pass
                    else:
                        time.sleep(1.5)
                st.success(f"Approved. RM {st.session_state.balance:.2f} will be automatically deducted from your next bill.")
                st.session_state.balance = 0.00
                st.rerun()
            else: st.warning("Insufficient balance.")
                
    elif "Merchant Vouchers" in payout_channel:
        st.markdown("<small style='color: #113826; font-weight:600;'>Promotion: Get **1.5x value** (RM 10.00 voucher costs only RM 6.60 in EcoBalance!)</small>", unsafe_allow_html=True)
        voucher_choice = st.selectbox("Select Neighborhood Voucher:", ["Starbucks RM 10 Voucher (Costs: RM 6.60)", "FamilyMart RM 15 Voucher (Costs: RM 10.00)"])
        cost = 6.60 if "Starbucks" in voucher_choice else 10.00
        if st.button("Claim and Redeeem Voucher", use_container_width=True):
            if st.session_state.balance >= cost:
                st.session_state.balance -= cost
                st.balloons()
                st.success("Voucher claimed. Your unique QR code has been saved to 'My Rewards'.")
                time.sleep(1.5)
                st.rerun()
            else: st.error("Insufficient balance for this voucher.")
    st.markdown("</div>", unsafe_allow_html=True)

    # 🥇 楼层排名 🥇
    st.markdown("<h3 style='color: #113826; margin-top: 24px; margin-bottom: 2px; font-weight:600;'>Inter-Floor Recycling League</h3>", unsafe_allow_html=True)
    st.caption("The winning floor this month receives a 10% Maintenance Fee rebate sponsored by Sime Darby Property.")
    
    leaderboard_data = {
        "Rank": ["1st", "2nd", "3rd", "4th"],
        "Floor": ["Floor 15 (Your Floor!)", "Floor 08", "Floor 12", "Floor 03"],
        "Weight": [f"{st.session_state.total_weight + 120.4:.1f} kg", "128.0 kg", "98.4 kg", "64.2 kg"]
    }
    
    for i in range(len(leaderboard_data["Floor"])):
        style_bold = "font-weight: 700; color: #113826;" if "Your Floor" in leaderboard_data["Floor"][i] else ""
        st.markdown(f"""
        <div class="leaderboard-row" style="{ 'background-color: #EEF2EE; border: 1.5px solid #113826;' if i==0 else '' }">
            <div style="{style_bold}">
                <strong>{leaderboard_data['Rank'][i]}</strong> — {leaderboard_data['Floor'][i]}
            </div>
            <div style="color: #113826; font-weight: 700;">{leaderboard_data['Weight'][i]}</div>
        </div>
        """, unsafe_allow_html=True)

    # 历史记录
    st.markdown("<h3 style='color: #113826; margin-top: 24px; font-weight:600;'>Recycling Statements</h3>", unsafe_allow_html=True)
    for item in reversed(st.session_state.history):
        st.markdown(f"""
        <div class="history-card">
            <div class="history-left">
                <span class="history-date">📅 {item['date']}</span>
                <span class="history-material">{item['type']}</span>
                <span class="history-weight">Weight: {item['weight']:.2f} kg</span>
            </div>
            <div class="history-earn">+RM {item['earn']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

# ==================== TAB 2: 🔑 Scan & Drop (数字孪生动态扫描中心与实时遥测) ====================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #113826; margin: 0; font-weight:600;'>Smart Chute Live Telemetry</h3>", unsafe_allow_html=True)
    st.write("Scan to unlock floor gravity chute. Live sensors and Edge AI will inspect the weight, material grade, and purity factor.")

    # 扫描与解锁卡片
    if 'hatch_unlocked' not in st.session_state:
        st.session_state.hatch_unlocked = False

    if not st.session_state.hatch_unlocked:
        # 雷达扫描激活按钮
        st.markdown("""
        <div style="background: white; border: 1px solid #E5E7EB; border-radius: 14px; padding: 24px; text-align: center; margin: 15px 0 20px 0;">
            <div style="font-size: 0.85rem; color: #6B7280; font-weight: 600; text-transform: uppercase;">Proximity Chute Node</div>
            <div style="font-size: 1.3rem; font-weight: 700; color: #113826; margin: 4px 0;">ELMINA_CONDO_FL15_PLASTIC</div>
            <div style="font-size: 0.8rem; color: #9CA3AF; margin-bottom: 16px;">Bluetooth Low Energy (BLE) Beacon Signal: Strong (-48 dBm)</div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Unlock Chute Hatch", use_container_width=True):
            with st.spinner("Authorizing resident token with Floor Controller..."):
                time.sleep(1.0)
            st.session_state.hatch_unlocked = True
            st.balloons()
            st.rerun()

    else:
        # 状态：已开锁并进入实时称重与 AI 质检阶段
        st.markdown("""
        <div style="background-color: #EEF2EE; border: 1.5px solid #113826; border-radius: 12px; padding: 14px 18px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
            <div>
                <span style="color: #113826; font-weight: 700;">Hatch Status: OPEN</span>
                <span style="color: #4B5563; font-size: 0.85rem; margin-left: 10px;">ID: ELMINA_CONDO_FL15</span>
            </div>
            <span style="font-size: 0.8rem; background-color: #113826; color: white; padding: 4px 10px; border-radius: 20px; font-weight: 600;">AI Camera Active</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<h4 style='color: #113826; margin-top: 10px; font-weight:600;'>Live Sensor Readings</h4>", unsafe_allow_html=True)
        
        # 演示滑块：调节重量与纯度（演示时可随时拖动）
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            sim_weight = st.slider("Scale Weight (kg)", min_value=0.10, max_value=4.00, value=1.25, step=0.05)
        with col_s2:
            sim_purity = st.slider("AI Purity Score", min_value=0.10, max_value=1.00, value=0.96, step=0.02)

        # 核心参数计算
        material_name = "PET Plastic"
        unit_rate = 0.80  # RM 0.80 / kg
        is_anomaly = sim_weight > 2.0 or sim_purity < 0.40
        payout_earned = round(sim_weight * unit_rate * sim_purity, 2)

        # 4 宫格遥测看板 (高质感卡片布局)
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin: 15px 0;">
            <!-- 1. 重量卡片 -->
            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.75rem; color: #6B7280; font-weight: 600; text-transform: uppercase;">1. Measured Weight</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #113826; margin-top: 4px;">{sim_weight:.2f} <span style="font-size: 1rem; font-weight: 500;">kg</span></div>
                <div style="font-size: 0.75rem; color: #10B981; margin-top: 2px;">High-precision load cell</div>
            </div>
            <!-- 2. 材质与单价卡片 -->
            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.75rem; color: #6B7280; font-weight: 600; text-transform: uppercase;">2. Material & Rate</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #113826; margin-top: 4px;">RM {unit_rate:.2f} <span style="font-size: 0.9rem; font-weight: 500;">/kg</span></div>
                <div style="font-size: 0.75rem; color: #4B5563; margin-top: 2px;">Grade: {material_name}</div>
            </div>
            <!-- 3. AI 纯度卡片 -->
            <div style="background: white; border: 1px solid #E5E7EB; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.75rem; color: #6B7280; font-weight: 600; text-transform: uppercase;">3. AI Purity Factor</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: {'#113826' if sim_purity >= 0.7 else '#D97706'}; margin-top: 4px;">{int(sim_purity * 100)}%</div>
                <div style="font-size: 0.75rem; color: {'#10B981' if sim_purity >= 0.7 else '#D97706'}; margin-top: 2px;">{'Clean, dry recyclable' if sim_purity >= 0.7 else 'Minor impurity detected'}</div>
            </div>
            <!-- 4. 即时收益卡片 -->
            <div style="background: white; border: 1.5px solid #113826; border-radius: 12px; padding: 16px;">
                <div style="font-size: 0.75rem; color: #113826; font-weight: 600; text-transform: uppercase;">4. Instant Payout</div>
                <div style="font-size: 1.8rem; font-weight: 700; color: #113826; margin-top: 4px;">RM {payout_earned:.2f}</div>
                <div style="font-size: 0.75rem; color: #10B981; margin-top: 2px;">Direct credit to wallet</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 透明公式明细卡片
        st.markdown(f"""
        <div style="background-color: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 10px; padding: 14px 18px; margin-bottom: 20px;">
            <div style="font-size: 0.8rem; color: #6B7280; font-weight: 600; text-transform: uppercase; margin-bottom: 6px;">Transparent Calculation Breakdown</div>
            <div style="font-family: monospace; font-size: 0.95rem; color: #111827;">
                {sim_weight:.2f} kg &times; RM {unit_rate:.2f} &times; {int(sim_purity * 100)}% Purity = <strong style="color: #113826; font-size: 1.05rem;">RM {payout_earned:.2f}</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 防作弊提示或完成投递按钮
        if is_anomaly:
            st.error("Anomaly Alert: The measured density or purity violates safety thresholds. Please remove liquids or unapproved items to proceed.")
        else:
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("Confirm Disposal & Disburse", use_container_width=True):
                    with st.spinner("Locking hatch and issuing micro-payout..."):
                        if server_connected:
                            try:
                                payload = {
                                    "user_id": "user_tang_01",
                                    "measured_weight_kg": sim_weight,
                                    "purity_factor": sim_purity,
                                    "material_type": material_name
                                }
                                # 🌟 核心同步修复：投递数据上传给中转站 🌟
                                requests.post("http://127.0.0.1:5000/api/v1/iot/disposal", json=payload, timeout=2.0)
                            except Exception:
                                pass
                        else:
                            st.session_state.balance += payout_earned
                            st.session_state.total_weight += sim_weight
                            st.session_state.container_fill = min(100.0, st.session_state.container_fill + (sim_weight * 0.5))
                            st.session_state.history.append({
                                "date": "2026-10-21",
                                "type": material_name,
                                "weight": sim_weight,
                                "earn": payout_earned
                            })
                            time.sleep(1.0)
                    st.success(f"Disposal complete. RM {payout_earned:.2f} has been credited to your EcoBalance.")
                    st.session_state.hatch_unlocked = False
                    time.sleep(1.2)
                    st.rerun()

            with col_b2:
                if st.button("Cancel & Lock Hatch", use_container_width=True):
                    st.session_state.hatch_unlocked = False
                    st.rerun()

# ==================== TAB 3: 🌟 社区筑路 2.5D 等距交互地图 🌟 ====================
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #113826; margin: 0; font-weight:600;'>EcoLoop-Flow Live 3D Paving Map</h3>", unsafe_allow_html=True)
    st.write("Sime Darby Property transforms your recycled plastics directly into high-value township infrastructure. Walk around and see your eco-impact!")
    
    # 进度与省钱看板小卡片
    col_metric1, col_metric2 = st.columns(2)
    with col_metric1:
        st.markdown("""
        <div style="background-color: #EEF2EE; padding: 16px; border-radius: 12px; border: 1.5px solid #113826; text-align: center;">
            <div style="color: #6B7280; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Eco-Pave Completed</div>
            <div style="color: #113826; font-size: 1.8rem; font-weight: 700; margin-top: 4px; letter-spacing: -0.5px;">142.5 Meters</div>
            <div style="color: #10B981; font-size: 0.75rem; margin-top: 4px; font-weight: 600;">📈 +12m successfully laid this week</div>
        </div>
        """, unsafe_allow_html=True)
    with col_metric2:
        st.markdown("""
        <div style="background-color: #EEF2EE; padding: 16px; border-radius: 12px; border: 1.5px solid #113826; text-align: center;">
            <div style="color: #6B7280; font-size: 0.8rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Procurement Saved</div>
            <div style="color: #113826; font-size: 1.8rem; font-weight: 700; margin-top: 4px; letter-spacing: -0.5px;">RM 14,250</div>
            <div style="color: #10B981; font-size: 0.75rem; margin-top: 4px; font-weight: 600;">💰 Slashing road aggregates cost by 35%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 🗺️ 极精美等距 2.5D 科技风格地图
    st.markdown("""
    <div style="background-color: #F3F4F6; padding: 15px; border-radius: 16px; border: 1px solid #E5E7EB; text-align: center; margin-bottom: 20px; box-shadow: inset 0 2px 10px rgba(0,0,0,0.03);">
        <svg viewBox="0 0 400 280" width="100%" height="auto" style="border-radius: 12px; background-color: #F8FAFC;">
            <defs>
                <pattern id="iso-grid" width="30" height="15" patternUnits="userSpaceOnUse">
                    <path d="M 15 0 L 30 7.5 L 15 15 L 0 7.5 Z" fill="none" stroke="#E2E8F0" stroke-width="0.5"/>
                </pattern>
                
                <linearGradient id="wall-front" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stop-color="#113826"/>
                    <stop offset="100%" stop-color="#092113"/>
                </linearGradient>
                <linearGradient id="wall-side" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stop-color="#1E5C36"/>
                    <stop offset="100%" stop-color="#113826"/>
                </linearGradient>
                <linearGradient id="roof-top" x1="0" y1="0" x2="1" y2="1">
                    <stop offset="0%" stop-color="#34D399"/>
                    <stop offset="100%" stop-color="#10B981"/>
                </linearGradient>
                
                <filter id="soft-shadow" x="-10%" y="-10%" width="120%" height="120%">
                    <feDropShadow dx="0" dy="8" stdDeviation="5" flood-color="#000000" flood-opacity="0.08" />
                </filter>
            </defs>
            
            <rect width="400" height="280" fill="#F1F5F9" />
            <rect width="400" height="280" fill="url(#iso-grid)" opacity="0.6" />
            
            <path d="M 50 140 L 200 65 L 350 140 L 200 215 Z" fill="#94A3B8" />
            <path d="M 50 140 L 200 65 L 350 140 L 200 215 Z" fill="none" stroke="#113826" stroke-width="16" stroke-linejoin="round" />
            <path d="M 50 140 L 200 65 L 350 140 L 200 215 Z" fill="none" stroke="#FFFFFF" stroke-dasharray="6,5" stroke-width="2" stroke-linejoin="round" opacity="0.8"/>
            
            <ellipse cx="200" cy="144" rx="42" ry="22" fill="#059669" />
            <ellipse cx="200" cy="140" rx="42" ry="22" fill="#34D399" filter="url(#soft-shadow)" />
            <text x="200" y="143" fill="#064E3B" font-family="'Inter'" font-size="8" font-weight="bold" text-anchor="middle">Eco-Park</text>
            
            <g transform="translate(60, 60)" filter="url(#soft-shadow)">
                <polygon points="0,75 35,57.5 70,75 35,92.5" fill="#000000" opacity="0.15" />
                <polygon points="0,25 35,42.5 35,75 0,57.5" fill="url(#wall-front)" />
                <polygon points="35,42.5 70,25 70,57.5 35,75" fill="url(#wall-side)" />
                <polygon points="0,25 35,7.5 70,25 35,42.5" fill="url(#roof-top)" />
                <text x="35" y="32" fill="#FFFFFF" font-family="'Inter'" font-size="9" font-weight="700" text-anchor="middle">Block A</text>
            </g>
            
            <g transform="translate(270, 60)" filter="url(#soft-shadow)">
                <polygon points="0,75 35,57.5 70,75 35,92.5" fill="#000000" opacity="0.15" />
                <polygon points="0,25 35,42.5 35,75 0,57.5" fill="url(#wall-front)" />
                <polygon points="35,42.5 70,25 70,57.5 35,75" fill="url(#wall-side)" />
                <polygon points="0,25 35,7.5 70,25 35,42.5" fill="url(#roof-top)" />
                <text x="35" y="32" fill="#FFFFFF" font-family="'Inter'" font-size="9" font-weight="700" text-anchor="middle">Block B</text>
            </g>
            
            <path d="M 112 112 L 158 130" stroke="#60A5FA" stroke-width="4" stroke-dasharray="5,3" fill="none" opacity="0.8"/>
            <path d="M 288 112 L 242 130" stroke="#60A5FA" stroke-width="4" stroke-dasharray="5,3" fill="none" opacity="0.8"/>
            
            <g transform="translate(200, 125)">
                <ellipse cx="0" cy="0" rx="6" ry="3" fill="#000000" opacity="0.2" />
                <path d="M 0 -8 C -4 -12, -7 -18, -7 -22 C -7 -26, -3 -29, 0 -29 C 3 -29, 7 -26, 7 -22 C 7 -18, 4 -12, 0 -8 Z" fill="#EF4444" />
                <circle cx="0" cy="-22" r="2.5" fill="#FFFFFF" />
                <text x="0" y="-33" fill="#EF4444" font-family="'Inter'" font-size="7.5" font-weight="bold" text-anchor="middle">Playground</text>
            </g>
            
            <g transform="translate(130, 175)">
                <ellipse cx="0" cy="0" rx="6" ry="3" fill="#000000" opacity="0.2" />
                <path d="M 0 -8 C -4 -12, -7 -18, -7 -22 C -7 -26, -3 -29, 0 -29 C 3 -29, 7 -26, 7 -22 C 7 -18, 4 -12, 0 -8 Z" fill="#10B981" />
                <circle cx="0" cy="-22" r="2.5" fill="#FFFFFF" />
                <text x="0" y="-33" fill="#10B981" font-family="'Inter'" font-size="7.5" font-weight="bold" text-anchor="middle">Jog Track</text>
            </g>
            
            <g transform="translate(270, 175)">
                <ellipse cx="0" cy="0" rx="6" ry="3" fill="#000000" opacity="0.2" />
                <path d="M 0 -8 C -4 -12, -7 -18, -7 -22 C -7 -26, -3 -29, 0 -29 C 3 -29, 7 -26, 7 -22 C 7 -18, 4 -12, 0 -8 Z" fill="#3B82F6" />
                <circle cx="0" cy="-22" r="2.5" fill="#FFFFFF" />
                <text x="0" y="-33" fill="#3B82F6" font-family="'Inter'" font-size="7.5" font-weight="bold" text-anchor="middle">Main Road</text>
            </g>
        </svg>
    </div>
    """, unsafe_allow_html=True)
    
    # 实时项目计划进度条
    st.markdown("<h4 style='color: #113826; margin-top: 15px; font-weight:600;'>Live Sustainability Projects</h4>", unsafe_allow_html=True)
    st.write("Sime Darby Property’s active infrastructure projects in our condominium:")
    
    st.markdown("**1. Elmina Boulevard Loop 3 (Eco-Asphalt Paving)**")
    st.progress(71)
    st.caption("⚡ **71% Progress** (Target: 200m Eco-Pave Road by Dec 2026)")
    
    st.markdown("**2. Lakeside Jogging Track (Luminescent Path)**")
    st.progress(45)
    st.caption("⚡ **45% Progress** (Target: 300m Luminescent Path by Jan 2027)")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 社区筑路地标详情描述
    st.markdown("<h4 style='color: #113826; margin-top: 10px; font-weight:600;'>Recycled Infrastructure Landmarks</h4>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="map-pointer-card" style="border-left-color: #EF4444;">
        <strong>Kids' Safety Eco-Playground Mat (Central Eco-Park)</strong><br>
        <span style="font-size: 0.82rem; color: #4B5563; display: block; margin-top: 4px;">
        Made from <strong>45,000 recycled PET plastic bottles</strong>. Highly durable shock-absorbing safety cushion that reduces fall injury risks for children.
        </span>
    </div>
    <div class="map-pointer-card" style="border-left-color: #10B981;">
        <strong>Glow-in-the-Dark Running Track (Lakeside Loop)</strong><br>
        <span style="font-size: 0.82rem; color: #4B5563; display: block; margin-top: 4px;">
        Constructed using <strong>3.2 tonnes of polymer-modified asphalt</strong> recycled from Block A & B. Features glowing aggregates for safe night jogging.
        </span>
    </div>
    <div class="map-pointer-card" style="border-left-color: #3B82F6;">
        <strong>Elmina West Main Boulevard Eco-Paving</strong><br>
        <span style="font-size: 0.82rem; color: #4B5563; display: block; margin-top: 4px;">
        Paved with plastic-asphalt compound, saving Sime Darby Property <strong>RM 48,000</strong> in raw aggregates and reducing future potholes by 40%.
        </span>
    </div>
    """, unsafe_allow_html=True)
