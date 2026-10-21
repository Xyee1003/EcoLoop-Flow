import streamlit as st
import time

# ==================== 页面高定配置 ====================
st.set_page_config(
    page_title="EcoLoop-Flow SDP Dev Portal", 
    page_icon="🏢", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== 注入自定义 CSS 样式 (SDP 企业级暗绿 UI) ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Inter', sans-serif;
        background-color: #F3F4F6;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    /* 顶部导航企业横幅 */
    .dev-brand-container {
        padding: 24px 30px;
        background: #0D2315; /* 更深沉沉稳的绿色 */
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
        font-size: 0.85rem;
        opacity: 0.8;
        font-weight: 300;
        margin-top: 2px;
    }
    
    /* 统计大卡片 */
    .metric-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0,0,0,0.01);
        text-align: center;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #6B7280;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-val {
        font-size: 2.2rem;
        font-weight: 700;
        color: #113826;
        margin: 6px 0;
        letter-spacing: -0.5px;
    }
    
    /* 智能派单任务卡片 */
    .task-card {
        background: #FEF3C7;
        border-left: 5px solid #D97706;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 12px;
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
        <strong>📍 Estate: City of Elmina (Block A)</strong><br>
        <span>Active Bins: 60 | Active Households: 420</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==================== 初始化数据 ====================
if 'is_dispatched' not in st.session_state:
    st.session_state.is_dispatched = False

# ==================== 第一排：核心商业价值 KPI 看板 ====================
st.markdown("<h3 style='color: #113826; font-weight: 600;'>Macro Sustainability & CAPEX KPI</h3>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Total Plastic Ingested</div>
        <div class="metric-val">4.82 Tonnes</div>
        <div style="color: #10B981; font-size: 0.75rem; font-weight: 500;">📈 +0.45T accumulated this week</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Eco-Asphalt Paved</div>
        <div class="metric-val">142.5 Meters</div>
        <div style="color: #10B981; font-size: 0.75rem; font-weight: 500;">🛣️ Elmina Boulevard Loop 3</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Est. CAPEX Saved</div>
        <div class="metric-val" style="color: #10B981;">RM 14,250</div>
        <div style="color: #10B981; font-size: 0.75rem; font-weight: 500;">Slashing road material budgets by 35%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Resident Trust Index</div>
        <div class="metric-val" style="color: #2563EB;">98.4%</div>
        <div style="color: #2563EB; font-size: 0.75rem; font-weight: 500;">Zero-anomaly sort rate</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== 第二排：底层集装箱监控 与 楼层管道堵塞预警 ====================
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("<h3 style='color: #113826; font-weight: 600;'>Basement Storage Capacity</h3>", unsafe_allow_html=True)
    
    materials = ["PET Plastic", "Aluminum Cans", "Paper & Cardboard", "Non-Recyclable (Organic)"]
    levels = [82.5, 42.0, 56.4, 91.2]
    
    for i in range(4):
        st.markdown(f"**{materials[i]} Container** ({levels[i]}% full)")
        st.progress(levels[i] / 100.0)
    
    st.markdown("---")
    
    # 智能清运决策模块
    st.markdown("<h3 style='color: #113826; font-weight: 600;'>Facility Dispatch Center</h3>", unsafe_allow_html=True)
    st.write("Sime Darby FM automation analyzes container telemetry to auto-schedule collections.")
    
    if st.session_state.is_dispatched:
        st.success("🚚 **Collection Dispatched:** Task #SDP-8823 has been sent to **FM Truck #04**. Scheduled pickup: **Tonight 9:00 PM**.")
    else:
        st.markdown(f"""
        <div class="task-card">
            <strong>🚨 BASEMENT OVERFLOW WARNING:</strong><br>
            <span style="font-size: 0.85rem; color: #78350F;">
            The <strong>Non-Recyclable</strong> container is at <strong>91.2%</strong> and <strong>PET Plastic</strong> is at <strong>82.5%</strong>. 
            To prevent gravity chute blockage in Block A, immediate clearance is highly recommended.
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Dispatch Autonomous Collection Truck", use_container_width=True):
            st.session_state.is_dispatched = True
            st.success("Dispatch command transmitted to IoT Fleet Management.")
            time.sleep(1.5)
            st.rerun()

with col_right:
    # 智能循环基建建议
    st.markdown("<h3 style='color: #113826; font-weight: 600;'>Infrastructure Recommendations</h3>", unsafe_allow_html=True)
    st.write("Current recommendations to recycle accumulated raw stock directly into ongoing development projects.")
    
    st.markdown("""
    <div style="background-color: white; border: 1px solid #E5E7EB; padding: 16px; border-radius: 12px; margin-bottom: 12px;">
        <strong>Option 1: Pave Park Running Tracks</strong><br>
        <span style="color: #4B5563; font-size: 0.8rem; display: block; margin-top: 4px;">
        Current <strong>4.82 tonnes</strong> of stored PET polymer can cover <strong>80m</strong> of lakeside path. 
        <strong style="color: #113826;">Est. Savings: RM 8,000</strong>
        </span>
    </div>
    <div style="background-color: white; border: 1px solid #E5E7EB; padding: 16px; border-radius: 12px; margin-bottom: 12px;">
        <strong>Option 2: Sidewalk Eco-Pave Bricks</strong><br>
        <span style="color: #4B5563; font-size: 0.8rem; display: block; margin-top: 4px;">
        Compress Paper and Plastic stock into <strong>3,500 Interlocking Eco-Bricks</strong> for the Block B entrance walkway. 
        <strong style="color: #113826;">Est. Savings: RM 6,250</strong>
        </span>
    </div>
    <div style="background-color: white; border: 1px solid #E5E7EB; padding: 16px; border-radius: 12px;">
        <strong>Option 3: B2B High-Contamination Trade</strong><br>
        <span style="color: #4B5563; font-size: 0.8rem; display: block; margin-top: 4px;">
        Export high-purity Aluminum cans (0.42 tonnes) directly to <strong>Lotte Chemical</strong> at RM 3.10/kg.
        <strong style="color: #113826;">Est. Revenue: RM 1,302</strong>
        </span>
    </div>
    """, unsafe_allow_html=True)
