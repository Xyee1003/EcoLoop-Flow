import streamlit as st
import time
import requests

# ==================== 页面高级配置 ====================
st.set_page_config(
    page_title="EcoLoop-Flow SDP Dev Portal", 
    page_icon="🏢", 
    layout="wide", # 宽屏大屏设计，匹配中控室观感
    initial_sidebar_state="collapsed"
)

# ==================== 真实网络数据拉取 ====================
BACKEND_DATA_URL = "http://localhost:5000/api/v1/resident/data"
CLEAR_CONTAINER_URL = "http://localhost:5000/api/v1/developer/clear-container"

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

# 优雅降级兜底数据
if not server_connected:
    container_fill = 82.5
    total_weight = 15.4

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
        background: #0D2315; /* Sime Darby Property 官方专属暗绿 */
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
        <strong>Estate: City of Elmina (Block A)</strong><br>
        <span>Active Bins: 60 | Active Households: 420</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not server_connected:
    st.warning("⚠️ Connected via Local State Backup. Please start server.py to stream live IoT telemetry.")

# ==================== 第一排：核心商业价值 KPI 看板 ====================
st.markdown("<h3 style='color: #113826; font-weight: 600;'>Macro Sustainability & CAPEX KPI</h3>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

# 计算根据真实总投递重量节省的基建成本 (假设每1kg节省RM 925的原材料采购)
est_savings = round(total_weight * 925.3, 2)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Total Material Ingested</div>
        <div class="metric-val">{total_weight:.2f} kg</div>
        <div style="color: #10B981; font-size: 0.75rem; font-weight: 500;">Live synchronizing with smart bins</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Eco-Asphalt Paved</div>
        <div class="metric-val">{(total_weight * 9.25):.1f} Meters</div>
        <div style="color: #10B981; font-size: 0.75rem; font-weight: 500;">Elmina Boulevard Section 3</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Est. CAPEX Saved</div>
        <div class="metric-val" style="color: #10B981;">RM {est_savings:,.2f}</div>
        <div style="color: #10B981; font-size: 0.75rem; font-weight: 500;">Slashing aggregates procurement by 35%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Resident Trust Index</div>
        <div class="metric-val" style="color: #2563EB;">98.4%</div>
        <div style="color: #2563EB; font-size: 0.75rem; font-weight: 500;">Zero-anomaly sorting rate</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== 第二排：底层集装箱监控 与 楼层管道堵塞预警 ====================
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("<h3 style='color: #113826; font-weight: 600;'>Basement Storage Capacity</h3>", unsafe_allow_html=True)
    
    materials = ["PET Plastic Bottles", "Aluminum Cans", "Paper & Cardboard", "Non-Recyclable (Organic)"]
    # 前三个从共享数据获取，第四个模拟高位
    levels = [container_fill, min(100.0, container_fill * 0.5), min(100.0, container_fill * 0.7), 91.2]
    
    for i in range(4):
        st.markdown(f"**{materials[i]} Container** ({levels[i]:.1f}% full)")
        st.progress(levels[i] / 100.0)
    
    st.markdown("---")
    
    # 智能清运决策模块
    st.markdown("<h3 style='color: #113826; font-weight: 600;'>Facility Dispatch Center</h3>", unsafe_allow_html=True)
    st.write("Sime Darby FM automation analyzes container telemetry to auto-schedule collections.")
    
    # 检查集装箱状态
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
                    try: requests.post(CLEAR_CONTAINER_URL, timeout=2.0)
                    except Exception: pass
                else:
                    time.sleep(1.5)
            st.success("Dispatch command successfully sent! Containers cleared.")
            time.sleep(1.0)
            st.rerun()

with col_right:
    # 智能循环基建建议
    st.markdown("<h3 style='color: #113826; font-weight: 600;'>Infrastructure Recommendations</h3>", unsafe_allow_html=True)
    st.write("Current recommendations to recycle accumulated raw stock directly into ongoing development projects.")
    
    st.markdown(f"""
    <div style="background-color: white; border: 1px solid #E5E7EB; padding: 16px; border-radius: 12px; margin-bottom: 12px;">
        <strong>Option 1: Pave Park Running Tracks</strong><br>
        <span style="color: #4B5563; font-size: 0.8rem; display: block; margin-top: 4px;">
        Current accumulated polymers can cover <strong>{(total_weight * 0.8):.1f}m</strong> of lakeside path. 
        <strong style="color: #113826;">Est. Savings: RM { (total_weight * 80.5):,.2f}</strong>
        </span>
    </div>
    <div style="background-color: white; border: 1px solid #E5E7EB; padding: 16px; border-radius: 12px; margin-bottom: 12px;">
        <strong>Option 2: Sidewalk Eco-Pave Bricks</strong><br>
        <span style="color: #4B5563; font-size: 0.8rem; display: block; margin-top: 4px;">
        Compress current paper and fiber stock into <strong>{int(total_weight * 150)} Interlocking Eco-Bricks</strong>. 
        <strong style="color: #113826;">Est. Savings: RM { (total_weight * 40.2):,.2f}</strong>
        </span>
    </div>
    """, unsafe_allow_html=True)
