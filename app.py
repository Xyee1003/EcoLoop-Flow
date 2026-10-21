import streamlit as st
import time

# ==================== 页面高定配置 ====================
st.set_page_config(
    page_title="EcoLoop-Flow", 
    page_icon="🌱", 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==================== 注入自定义 CSS 样式 (精美高定 UI) ====================
st.markdown("""
<style>
    /* 全局背景与字体 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #F7F9F6;
    }
    
    /* 隐藏 Streamlit 默认页眉和页脚 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* 头部横幅卡片 */
    .brand-container {
        text-align: center;
        padding: 24px 10px;
        background: linear-gradient(135deg, #113826 0%, #1c5c36 100%);
        border-radius: 20px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px rgba(17, 56, 38, 0.15);
    }
    .brand-title {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin: 0 !important;
        letter-spacing: -1px;
        color: #E8F5E9 !important;
    }
    .brand-subtitle {
        font-size: 0.95rem;
        opacity: 0.85;
        margin-top: 4px;
        font-weight: 300;
    }

    /* 炫酷钱包卡片 */
    .wallet-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #E0E8E1;
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    .wallet-header {
        font-size: 0.85rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .wallet-balance {
        font-size: 2.4rem;
        font-weight: 700;
        color: #113826;
        margin: 8px 0;
    }
    
    /* 历史账单卡片 */
    .history-card {
        padding: 14px 16px;
        border-radius: 12px;
        background-color: white;
        margin-bottom: 10px;
        border: 1px solid #EEF2EE;
        box-shadow: 0 2px 8px rgba(0,0,0,0.01);
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
        color: #999;
    }
    .history-material {
        font-size: 0.95rem;
        font-weight: 600;
        color: #2D3748;
        margin-top: 2px;
    }
    .history-weight {
        font-size: 0.8rem;
        color: #4A5568;
    }
    .history-earn {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1c5c36;
    }

    /* Tab 样式美化 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #EBF1EC;
        padding: 6px;
        border-radius: 12px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 40px;
        border-radius: 8px;
        border: none;
        background-color: transparent;
        color: #555;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #113826 !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
</style>
""", unsafe_allow_html=True)

# ==================== 初始化本地缓存数据库 ====================
if 'balance' not in st.session_state:
    st.session_state.balance = 18.20  # 初始余额 RM 18.20
if 'total_weight' not in st.session_state:
    st.session_state.total_weight = 12.8  # 累计回收 12.8kg
if 'history' not in st.session_state:
    st.session_state.history = [
        {"date": "2026-10-18", "type": "🔴 Aluminum", "weight": 1.2, "earn": 3.60},
        {"date": "2026-10-19", "type": "🔵 Plastic", "weight": 2.5, "earn": 2.00},
        {"date": "2026-10-20", "type": "🟢 Paper", "weight": 5.4, "earn": 2.16}
    ]

# ==================== 📱 App 顶部精美横幅 ====================
st.markdown("""
<div class="brand-container">
    <h1 class="brand-title">🌱 EcoLoop-Flow</h1>
    <div class="brand-subtitle">Sime Darby Smart Condo Micro-Payout Network</div>
</div>
""", unsafe_allow_html=True)

# ==================== Tab 导航栏 ====================
tab1, tab2, tab3 = st.tabs(["🏠 My Wallet", "🔑 Scan & Drop", "🛣️ Condo Eco-Road"])

# ==================== TAB 1: 个人钱包与历史 ====================
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="wallet-card">
        <div class="wallet-header">Available Balance</div>
        <div class="wallet-balance">RM {st.session_state.balance:.2f}</div>
        <div style="color: #666; font-size: 0.85rem; display: flex; justify-content: space-between;">
            <span>📍 Elmina Block A, Lvl 15</span>
            <span style="font-weight: 600; color: #1c5c36;">Total Recycled: {st.session_state.total_weight:.1f} kg</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # DuitNow / TnG 一键提现
    if st.button("💸 Instant Cash-out to Touch 'n Go eWallet", use_container_width=True):
        if st.session_state.balance > 0:
            with st.spinner("Establishing secure DuitNow transaction..."):
                time.sleep(1.5)
            st.success(f"🎉 RM {st.session_state.balance:.2f} has been instantly credited to your eWallet!")
            st.session_state.balance = 0.00
            st.rerun()
        else:
            st.warning("Your balance is RM 0.00. Time to drop some plastic bottles!")

    # 投递历史明细
    st.markdown("<h3 style='color: #113826; margin-top: 24px;'>📜 Recycling Statements</h3>", unsafe_allow_html=True)
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

# ==================== TAB 2: 扫码投递 (真机扫码演示版) ====================
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #113826; margin: 0;'>🔑 Unlock Floor Smart Chute</h3>", unsafe_allow_html=True)
    st.write("Align the bin's QR code within the camera frame below to unlock.")
    
    # 📸 调用手机/电脑摄像头进行真实扫码模拟
    picture = st.camera_input("Point your camera at the Smart Bin's QR Code")
    
    if picture:
        st.success("📸 QR Code Image captured successfully!")
        with st.status("Analyzing QR Code & Verifying resident ID via Portal...", expanded=True) as status:
            time.sleep(1.2)
            st.write("🔑 Decoded: Bin_ID = [ELMINA_CONDO_FL15_PLASTIC]")
            time.sleep(0.8)
            st.write("🔒 Secure Handshake established with Floor IoT Controller...")
            time.sleep(0.8)
            status.update(label="🔓 Hatch Gate Unlocked! You may now drop your items.", state="complete")
        st.balloons()
        
        st.markdown("---")
        # 模拟真实的 IoT 传感器传上来的重量和防作弊数据
        st.markdown("<h4>🤫 IoT Hardware Telemetry Simulation</h4>", unsafe_allow_html=True)
        st.write("Simulate physical drop-off weight and camera purity detection:")
        
        sim_weight = st.slider("Step 1: Set Garbage Weight (kg)", 0.1, 4.0, 0.85)
        sim_purity = st.slider("Step 2: Set Cleanliness/Purity Factor", 0.0, 1.0, 0.95)
        
        if st.button("🎯 Simulate Disposal Complete & Recalculate"):
            material = "🔵 Plastic"
            rate = 0.80
            earnings = sim_weight * rate * sim_purity
            
            # 更新缓存
            st.session_state.balance += earnings
            st.session_state.total_weight += sim_weight
            st.session_state.history.append({
                "date": "2026-10-21",
                "type": material,
                "weight": sim_weight,
                "earn": earnings
            })
            st.success(f"Disposal success! AI verified {sim_weight}kg with {sim_purity*100:.0f}% purity. +RM {earnings:.2f} credited!")
            time.sleep(2)
            st.rerun()


# ==================== TAB 3: 社区筑路大屏 (Sime Darby Core Business Show) ====================
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #113826; margin: 0;'>🛣️ Building Our Community Road</h3>", unsafe_allow_html=True)
    st.write("Sime Darby Property transforms your recycled plastics directly into sustainable local infrastructure.")
    
    # 社区筑路数据卡片
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("""
        <div style="background-color: #E8F5E9; padding: 15px; border-radius: 12px; border: 1px solid #C8E6C9; text-align: center;">
            <div style="color: #2E7D32; font-size: 0.8rem; font-weight: 600; text-transform: uppercase;">Eco-Pave Completed</div>
            <div style="color: #1B5E20; font-size: 1.8rem; font-weight: 700; margin-top: 4px;">142.5 Meters</div>
            <div style="color: #388E3C; font-size: 0.75rem; margin-top: 4px;">📈 +12m added this week</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="background-color: #E8F5E9; padding: 15px; border-radius: 12px; border: 1px solid #C8E6C9; text-align: center;">
            <div style="color: #2E7D32; font-size: 0.8rem; font-weight: 600; text-transform: uppercase;">Procurement Saved</div>
            <div style="color: #1B5E20; font-size: 1.8rem; font-weight: 700; margin-top: 4px;">RM 14,250</div>
            <div style="color: #388E3C; font-size: 0.75rem; margin-top: 4px;">💰 Slashing road material costs</div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("#### 📍 Current Live Project: Elmina Boulevard Eco-Pathway")
    
    # 进度条
    st.progress(71)
    st.caption("⚡ **71% Progress** (Target: 200m Sustainable Paving by Dec 2026)")
    
    # 实物图解小贴士
    st.markdown("""
    <div style="background-color: white; border: 1px solid #E2E8F0; padding: 16px; border-radius: 12px; margin-top: 15px;">
        <span style="font-size: 1.2rem;">💡</span> <strong>The Road Under Your Feet:</strong><br>
        <span style="color: #4A5568; font-size: 0.85rem;">
        The plastic bottles you recycled this week are shredded into polymer pellets and mixed with asphalt. This paving is 40% more durable against heavy tropical monsoons, saving Sime Darby Property millions in pothole repairs!
        </span>
    </div>
    """, unsafe_allow_html=True)
