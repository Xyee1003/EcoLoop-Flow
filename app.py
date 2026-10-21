import streamlit as st
import time

# ==================== 页面高级配置 ====================
st.set_page_config(
    page_title="EcoLoop-Flow", 
    page_icon="🌱", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== 注入自定义 CSS 样式 (去Emoji、高端极简 UI) ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #FAFAF9; /* 温暖舒缓的极简米白 */
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

    /* 极简精致钱包卡片 */
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

    /* 楼层排名表格行 */
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

# ==================== 初始化本地缓存数据库 ====================
if 'balance' not in st.session_state: st.session_state.balance = 24.50
if 'total_weight' not in st.session_state: st.session_state.total_weight = 15.4
if 'history' not in st.session_state:
    st.session_state.history = [
        {"date": "2026-10-18", "type": "Aluminum Cans", "weight": 1.2, "earn": 3.60},
        {"date": "2026-10-19", "type": "PET Plastic Bottles", "weight": 2.5, "earn": 2.00},
        {"date": "2026-10-20", "type": "Paper & Cardboard", "weight": 5.4, "earn": 2.16}
    ]
if 'container_fill' not in st.session_state: st.session_state.container_fill = 82.5

# ==================== 📱 App 顶部企业横幅 ====================
st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">EcoLoop-Flow</h1>
    <div class="brand-subtitle">Smart Condo Micro-Payout & Utility Offset Network</div>
</div>
""", unsafe_allow_html=True)

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
                with st.spinner("Connecting to secure TNG Merchant API..."): time.sleep(1.5)
                st.success(f"RM {st.session_state.balance:.2f} successfully credited to your Touch 'n Go Wallet.")
                st.session_state.balance = 0.00
                st.rerun()
            else: st.warning("Insufficient balance to withdraw.")
                
    elif "Bills" in payout_channel:
        utility_choice = st.selectbox("Select Utility Bill:", ["TNB (Electricity Bill) - Account: 2201992...", "Syabas (Water Bill) - Account: 9923018..."])
        if st.button(f"Apply Credit to {utility_choice.split()[0]}", use_container_width=True):
            if st.session_state.balance > 0:
                with st.spinner("Applying rebate to your next utility statement..."): time.sleep(1.5)
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

# ==================== TAB 2: 扫码投递 (带 AI 防作弊) ====================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #113826; margin: 0; font-weight:600;'>Unlock Floor Smart Chute</h3>", unsafe_allow_html=True)
    st.write("Align the bin's QR code within the camera frame below to unlock.")
    
    picture = st.camera_input("Point your camera at the Smart Bin's QR Code", label_visibility="collapsed")
    
    if picture:
        st.success("QR Code Image captured successfully.")
        with st.status("Analyzing QR Code & Verifying resident ID...", expanded=True) as status:
            time.sleep(1.0)
            st.write("🔑 Decoded: Bin_ID = [ELMINA_CONDO_FL15_PLASTIC]")
            time.sleep(0.5)
            status.update(label="Hatch Gate Unlocked. Drop your items now.", state="complete")
        st.balloons()
        
        st.markdown("---")
        st.markdown("<h4>IoT Hardware Telemetry Simulation</h4>", unsafe_allow_html=True)
        
        sim_weight = st.slider("Step 1: Set Garbage Weight (kg)", 0.1, 4.0, 0.85)
        sim_purity = st.slider("Step 2: Set Cleanliness/Purity Factor", 0.0, 1.0, 0.95)
        
        is_anomaly = False
        if sim_weight > 1.8:
            is_anomaly = True
            st.error("🚨 **AI High-Density Anomaly Detected:** Volume-to-weight ratio mismatch. Hatch locked.")

        if st.button("Simulate Disposal Complete"):
            if is_anomaly:
                st.error("Disposal Rejected. Please clean the bottles of any liquids and retry.")
            else:
                material = "Plastic"
                rate = 0.80
                earnings = sim_weight * rate * sim_purity
                st.session_state.balance += earnings
                st.session_state.total_weight += sim_weight
                st.session_state.container_fill = min(100.0, st.session_state.container_fill + (sim_weight * 0.5))
                st.session_state.history.append({
                    "date": "2026-10-21", "type": material, "weight": sim_weight, "earn": earnings
                })
                st.success("Disposal success. Balance credited.")
                time.sleep(1.5)
                st.rerun()

# ==================== TAB 3: 🌟 社区筑路交互地图与计划进度 🌟 ====================
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #113826; margin: 0; font-weight:600;'>EcoLoop-Flow Live Paving Map</h3>", unsafe_allow_html=True)
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

    # 🗺️ 极精美高保真社区 SVG 地图 🗺️
    st.markdown("""
    <div style="background-color: #F3F4F6; padding: 15px; border-radius: 16px; border: 1px solid #E5E7EB; text-align: center; margin-bottom: 20px; box-shadow: inset 0 2px 10px rgba(0,0,0,0.03);">
        <svg viewBox="0 0 400 240" width="100%" height="auto" style="border-radius: 12px; background-color: #ECFDF5;">
            <defs>
                <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
                    <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#D1FAE5" stroke-width="0.5"/>
                </pattern>
            </defs>
            <rect width="400" height="240" fill="url(#grid)" />
            
            <path d="M 40 120 C 120 40, 280 40, 360 120" stroke="#94A3B8" stroke-width="12" fill="none" stroke-linecap="round" />
            <path d="M 40 120 C 120 200, 280 200, 360 120" stroke="#113826" stroke-width="12" fill="none" stroke-linecap="round" />
            <path d="M 40 120 C 120 200, 280 200, 360 120" stroke="#FFFFFF" stroke-dasharray="8,6" stroke-width="2" fill="none" stroke-linecap="round" />
            
            <g transform="translate(60, 45)">
                <rect x="0" y="0" width="65" height="42" rx="8" fill="#113826" />
                <text x="32" y="25" fill="#FFFFFF" font-family="'Inter'" font-size="10" font-weight="700" text-anchor="middle">Block A</text>
            </g>
            <g transform="translate(275, 45)">
                <rect x="0" y="0" width="65" height="42" rx="8" fill="#113826" />
                <text x="32" y="25" fill="#FFFFFF" font-family="'Inter'" font-size="10" font-weight="700" text-anchor="middle">Block B</text>
            </g>
            
            <circle cx="200" cy="120" r="38" fill="#34D399" opacity="0.85" />
            <circle cx="200" cy="120" r="33" fill="none" stroke="#FFFFFF" stroke-dasharray="4,3" stroke-width="1" />
            <text x="200" y="123" fill="#064E3B" font-family="'Inter'" font-size="9" font-weight="bold" text-anchor="middle">Eco-Park</text>
            
            <g transform="translate(200, 105)">
                <path d="M 0 0 C -6 -6, -10 -14, -10 -20 C -10 -26, -5 -30, 0 -30 C 5 -30, 10 -26, 10 -20 C 10 -14, 6 -6, 0 0 Z" fill="#EF4444" />
                <circle cx="0" cy="-20" r="4" fill="#FFFFFF" />
                <text x="0" y="-34" fill="#EF4444" font-family="'Inter'" font-size="8" font-weight="bold" text-anchor="middle">Playground</text>
            </g>
            
            <g transform="translate(140, 180)">
                <path d="M 0 0 C -6 -6, -10 -14, -10 -20 C -10 -26, -5 -30, 0 -30 C 5 -30, 10 -26, 10 -20 C 10 -14, 6 -6, 0 0 Z" fill="#10B981" />
                <circle cx="0" cy="-20" r="4" fill="#FFFFFF" />
                <text x="0" y="-34" fill="#10B981" font-family="'Inter'" font-size="8" font-weight="bold" text-anchor="middle">Jog Track</text>
            </g>
            
            <g transform="translate(280, 150)">
                <path d="M 0 0 C -6 -6, -10 -14, -10 -20 C -10 -26, -5 -30, 0 -30 C 5 -30, 10 -26, 10 -20 C 10 -14, 6 -6, 0 0 Z" fill="#3B82F6" />
                <circle cx="0" cy="-20" r="4" fill="#FFFFFF" />
                <text x="0" y="-34" fill="#3B82F6" font-family="'Inter'" font-size="8" font-weight="bold" text-anchor="middle">Main Road</text>
            </g>
        </svg>
    </div>
    """, unsafe_allow_html=True) # 已经加上了 unsafe_allow_html=True
    
    # 实时计划进度
    st.markdown("<h4 style='color: #113826; margin-top: 15px; font-weight:600;'>Live Sustainability Projects</h4>", unsafe_allow_html=True)
    st.write("Sime Darby Property’s active infrastructure projects in our condominium:")
    
    st.markdown("**1. Elmina Boulevard Loop 3 (Eco-Asphalt Paving)**")
    st.progress(71)
    st.caption("⚡ **71% Progress** (Target: 200m Eco-Pave Road by Dec 2026)")
    
    st.markdown("**2. Lakeside Jogging Track (Luminescent Path)**")
    st.progress(45)
    st.caption("⚡ **45% Progress** (Target: 300m Luminescent Path by Jan 2027)")
    
    st.markdown("<br>", unsafe_allow_html=True)

    # 社区地标详情
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
