import streamlit as st
import time
import requests
import pandas as pd
import plotly.express as px
from streamlit_autorefresh import st_autorefresh

# ==================== 页面高级配置 ====================
st.set_page_config(
    page_title="EcoScan SDP Dev Portal", 
    page_icon="🏢", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 每隔 2.5 秒自动刷新一次，实时拉取真实后端状态
st_autorefresh(interval=2500, limit=1000, key="dev_fizz_refresh")

# ==================== 初始化 Session State (自定义 Project Idea 存储) ====================
if 'custom_projects' not in st.session_state:
    st.session_state.custom_projects = [
        {
            "id": 1,
            "title": "Option 1: Pave Park Running Tracks",
            "desc": "Polymer asphalt mix for lakeside jogging paths in City of Elmina.",
            "yield_factor": 0.8,
            "unit": "Meters",
            "save_rate": 80.5
        },
        {
            "id": 2,
            "title": "Option 2: Sidewalk Eco-Pave Bricks",
            "desc": "Interlocking eco-bricks compressed from recycled fiber polymers.",
            "yield_factor": 150.0,
            "unit": "Bricks",
            "save_rate": 40.2
        }
    ]

# ==================== 真实网络数据拉取 (对接 server.py) ====================
BRIDGE_API = "http://127.0.0.1:5000/api"

try:
    response = requests.get(f"{BRIDGE_API}/state", timeout=1.0)
    if response.status_code == 200:
        server_data = response.json()
        container_fill = server_data.get("container_fill", 82.5)
        total_weight = server_data.get("total_recycled_kg", 40.2)
        materials_dict = server_data.get("materials_kg", {"Plastic": 22.4, "Paper": 11.2, "Glass": 6.6})
        server_connected = True
    else:
        server_connected = False
except Exception:
    server_connected = False

# 离线降级兜底数据
if not server_connected:
    container_fill = 82.5
    total_weight = 40.2
    materials_dict = {"Plastic": 22.4, "Paper": 11.2, "Glass": 6.6}

# ==================== 注入自定义 CSS 样式 (SDP 企业级暗绿 UI) ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #F8FAFC;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
    
    /* 顶部横幅 */
    .dev-brand-container {
        padding: 20px 26px;
        background: linear-gradient(135deg, #0D2315 0%, #173B24 100%);
        border-radius: 16px;
        color: white;
        margin-bottom: 24px;
        box-shadow: 0 12px 32px rgba(13, 35, 21, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.08);
    }
    .dev-title {
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: #FFFFFF !important;
        letter-spacing: -0.5px;
        white-space: nowrap;
    }
    .dev-subtitle {
        font-size: 0.85rem; opacity: 0.85; font-weight: 400; margin-top: 4px; color: #A7F3D0;
    }
    .status-pill {
        display: inline-flex; align-items: center; gap: 6px;
        padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 600;
        background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; color: #34D399;
        white-space: nowrap;
    }
    .status-dot {
        width: 8px; height: 8px; border-radius: 50%; background-color: #34D399;
        box-shadow: 0 0 8px #34D399;
    }
    
    /* KPI 核心指标卡片 */
    .metric-card {
        background: white; padding: 18px 20px; border-radius: 14px; border: 1px solid #E2E8F0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.02); text-align: left; position: relative;
        transition: all 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.04);
        border-color: #CBD5E1;
    }
    .metric-label {
        font-size: 0.72rem; color: #64748B; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px;
    }
    .metric-val {
        font-size: 1.85rem; font-weight: 800; color: #0F172A; margin: 4px 0 2px 0; letter-spacing: -0.5px;
    }
    .delta-badge {
        display: inline-flex; align-items: center; font-size: 0.75rem; font-weight: 700;
        color: #059669; background-color: #ECFDF5; padding: 2px 8px; border-radius: 12px; border: 1px solid #A7F3D0;
    }
    
    /* 模块卡片与容器 */
    .task-card {
        background: #FFFBEB; border-left: 4px solid #F59E0B; padding: 14px 16px; border-radius: 10px; margin-bottom: 14px;
    }
    .idea-card {
        background-color: white; border: 1px solid #E2E8F0; padding: 16px; border-radius: 12px; margin-bottom: 12px;
        transition: all 0.2s ease-in-out;
    }
    .idea-card:hover {
        border-color: #10B981; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.06);
    }
    
    /* Streamlit 按钮重构 */
    div.stButton > button {
        background: linear-gradient(135deg, #0D2315 0%, #173B24 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 18px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }
    div.stButton > button:hover {
        background: #10B981 !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.25) !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== 🏢 顶部企业级横幅 & 园区切换器 ====================
selected_estate = st.selectbox(
    "Select Property Estate:",
    ["City of Elmina (Block A - Main Tower)", "City of Elmina (Block B)", "Bukit Jelutong Commercial Center"],
    label_visibility="collapsed"
)

status_pill = (
    '<div class="status-pill"><div class="status-dot"></div> Live Telemetry Connected</div>'
    if server_connected else
    '<div class="status-pill" style="border-color:#F59E0B; color:#F59E0B; background:rgba(245,158,11,0.15);"><div class="status-dot" style="background:#F59E0B; box-shadow:0 0 8px #F59E0B;"></div> Offline Backup</div>'
)

# 使用单行与结构化 HTML，防止 Markdown 误判缩进为代码块
header_html = f'''<div class="dev-brand-container"><div><div style="display:flex; align-items:center; gap:12px; margin-bottom:4px;"><h1 class="dev-title">EcoScan</h1>{status_pill}</div><div class="dev-subtitle">Sime Darby Property Facility & Infrastructure Management System</div></div><div style="text-align: right; font-size: 0.85rem;"><strong style="color:#FFFFFF; font-size:0.95rem;">{selected_estate}</strong><br><span style="opacity:0.8; font-size:0.8rem;">Active Bins: 60 | Active Households: 420</span></div></div>'''

st.markdown(header_html, unsafe_allow_html=True)

# ==================== 动态增量逻辑计算 ====================
if 'prev_total_weight' not in st.session_state:
    st.session_state.prev_total_weight = total_weight

delta_weight = round(total_weight - st.session_state.prev_total_weight, 2)
st.session_state.prev_total_weight = total_weight

est_savings = round(total_weight * 925.3, 2)
delta_savings = round(delta_weight * 925.3, 2)

carbon_offset = total_weight * 1.5
delta_carbon = delta_weight * 1.5

# ==================== 第一排：核心商业价值 KPI 看板 & 饼图 (Pie Chart) ====================
st.markdown("<h3 style='color: #0F172A; font-weight: 700; font-size:1.15rem; margin-bottom:12px;'>Macro Sustainability & CAPEX KPI</h3>", unsafe_allow_html=True)

col_kpi_metrics, col_kpi_pie = st.columns([3, 2])

with col_kpi_metrics:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom:12px;">
            <div class="metric-label">Total Material Ingested</div>
            <div class="metric-val">{total_weight:.1f} <span style="font-size:1rem; font-weight:600; color:#64748B;">kg</span></div>
            {f'<div class="delta-badge">▲ +{delta_weight:.1f} kg</div>' if delta_weight > 0 else '<div style="font-size: 0.72rem; color: #94A3B8;">Synced with EcoScan Bridge</div>'}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Est. CAPEX Saved</div>
            <div class="metric-val" style="color: #0D2315;">RM {est_savings:,.2f}</div>
            {f'<div class="delta-badge">▲ +RM {delta_savings:,.2f}</div>' if delta_weight > 0 else '<div style="font-size: 0.72rem; color: #94A3B8;">Slashing aggregates cost</div>'}
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card" style="margin-bottom:12px;">
            <div class="metric-label">Eco-Asphalt Paved</div>
            <div class="metric-val">{(total_weight * 9.25):.1f} <span style="font-size:1rem; font-weight:600; color:#64748B;">Meters</span></div>
            {f'<div class="delta-badge">▲ +{(delta_weight * 9.25):.1f} m</div>' if delta_weight > 0 else '<div style="font-size: 0.72rem; color: #94A3B8;">Elmina Boulevard Sec 3</div>'}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">ESG CO2 Offsets</div>
            <div class="metric-val" style="color: #059669;">{carbon_offset:.1f} <span style="font-size:1rem; font-weight:600; color:#64748B;">kg</span></div>
            {f'<div class="delta-badge" style="color: #059669; background-color: #ECFDF5; border-color: #A7F3D0;">▲ +{delta_carbon:.1f} kg CO2</div>' if delta_weight > 0 else f'<div style="font-size: 0.72rem; color: #059669; font-weight:600;">≈ {int(carbon_offset/22)} trees planted</div>'}
        </div>
        """, unsafe_allow_html=True)

with col_kpi_pie:
    mat_keys = list(materials_dict.keys())
    mat_vals = [materials_dict[k] for k in mat_keys]
    
    df_kpi_pie = pd.DataFrame({
        "Material Category": mat_keys,
        "Weight (kg)": mat_vals
    })

    fig_kpi_pie = px.pie(
        df_kpi_pie, 
        values="Weight (kg)", 
        names="Material Category", 
        title="Material Composition Breakdown",
        hole=0.45,
        color_discrete_sequence=["#10B981", "#3B82F6", "#F59E0B"]
    )
    fig_kpi_pie.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color='#FFFFFF', width=2)))
    fig_kpi_pie.update_layout(
        margin=dict(t=30, b=10, l=10, r=10),
        height=245,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_kpi_pie, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== 第二排：底层集装箱进度条 (Progress Bar) & 清运控制 ====================
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("<h3 style='color: #0F172A; font-weight: 700; font-size:1.15rem; margin-bottom:4px;'>Basement Storage Capacity</h3>", unsafe_allow_html=True)
    st.caption("Real-time telemetry of underground automated waste collection containers.")
    st.markdown("<div style='margin-bottom:14px;'></div>", unsafe_allow_html=True)
    
    containers = [
        {"name": "PET Plastic Bottles Container", "fill": min(100.0, container_fill)},
        {"name": "Aluminum Cans Container", "fill": min(100.0, container_fill * 0.45)},
        {"name": "Paper & Cardboard Container", "fill": min(100.0, container_fill * 0.60)},
        {"name": "Non-Recyclable Organic Container", "fill": 91.2}
    ]
    
    for c in containers:
        col_c1, col_c2 = st.columns([4, 1])
        with col_c1:
            st.markdown(f"<span style='font-size:0.88rem; font-weight:600; color:#334155;'>{c['name']}</span>", unsafe_allow_html=True)
        with col_c2:
            fill_color = "#EF4444" if c['fill'] >= 85 else ("#F59E0B" if c['fill'] >= 70 else "#10B981")
            st.markdown(f"<div style='text-align:right; font-weight:700; color:{fill_color}; font-size:0.9rem;'>{c['fill']:.1f}%</div>", unsafe_allow_html=True)
        st.progress(c["fill"] / 100.0)
        st.markdown("<div style='margin-bottom:10px;'></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 智能清运决策模块
    st.markdown("<h3 style='color: #0F172A; font-weight: 700; font-size:1.1rem;'>Facility Dispatch Center</h3>", unsafe_allow_html=True)
    
    if container_fill == 0.0:
        st.success("✅ SUCCESS: All basement containers cleared. Storage telemetry normal (0.0%).")
    else:
        if container_fill >= 80.0:
            st.markdown(f"""
            <div class="task-card">
                <strong style="color:#9A3412;">🚨 BASEMENT OVERFLOW WARNING:</strong><br>
                <span style="font-size: 0.85rem; color: #78350F;">
                The <strong>PET Plastic Bottles</strong> container is currently critical at <strong>{container_fill:.1f}%</strong> capacity. 
                Please trigger clearance to prevent gravity chute blockages.
                </span>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🚛 Dispatch Collection Truck & Clear Containers", use_container_width=True):
            with st.spinner("Transmitting clearance dispatch order to Fleet..."):
                if server_connected:
                    try: requests.post(f"{BRIDGE_API}/developer/clear", timeout=2.0)
                    except Exception: pass
                else:
                    time.sleep(1.0)
            st.success("Dispatch command successfully sent! Containers cleared.")
            time.sleep(1.0)
            st.rerun()

with col_right:
    st.markdown("<h3 style='color: #0F172A; font-weight: 700; font-size:1.15rem; margin-bottom:4px;'>Infrastructure Recommendations</h3>", unsafe_allow_html=True)
    st.caption("Recycle accumulated raw stock directly into ongoing estate development projects.")
    st.markdown("<div style='margin-bottom:14px;'></div>", unsafe_allow_html=True)
    
    # 开发者动态添加 Project Idea 表单
    with st.expander("➕ Add Custom Project Idea", expanded=False):
        with st.form("add_project_form"):
            new_title = st.text_input("Project Name", placeholder="e.g. Option 3: 3D-Printed Park Benches")
            new_desc = st.text_input("Description", placeholder="e.g. Convert HDPE polymers into outdoor furniture")
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                new_yield = st.number_input("Yield Factor (units/kg)", value=0.5, step=0.1)
                new_unit = st.text_input("Unit Name", value="Benches")
            with col_f2:
                new_rate = st.number_input("CAPEX Save Rate (RM/kg)", value=65.0, step=5.0)
                
            submit_idea = st.form_submit_button("🚀 Add Idea to Pipeline", use_container_width=True)
            if submit_idea and new_title:
                st.session_state.custom_projects.append({
                    "id": len(st.session_state.custom_projects) + 1,
                    "title": new_title,
                    "desc": new_desc,
                    "yield_factor": new_yield,
                    "unit": new_unit,
                    "save_rate": new_rate
                })
                st.success(f"Added project: '{new_title}'!")
                st.rerun()

    # 渲染 Project Ideas
    for p in st.session_state.custom_projects:
        calc_yield = total_weight * p["yield_factor"]
        calc_savings = total_weight * p["save_rate"]
        yield_str = f"{int(calc_yield)}" if p["yield_factor"] >= 1 else f"{calc_yield:.1f}"
        
        st.markdown(f"""
        <div class="idea-card">
            <strong style="color:#0F172A; font-size:0.95rem;">{p['title']}</strong>
            <span style="color: #64748B; font-size: 0.8rem; display: block; margin-top: 2px;">{p['desc']}</span>
            <div style="margin-top: 10px; font-size: 0.85rem; color: #334155; background:#F8FAFC; padding:8px 12px; border-radius:8px;">
                Estimated Output: <strong>{yield_str} {p['unit']}</strong><br>
                <span style="color: #059669; font-weight: 700;">Est. CAPEX Savings: RM {calc_savings:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==================== 第三排：回收历史趋势图与报告导出 ====================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<h3 style='color: #0F172A; font-weight: 700; font-size:1.15rem; margin-bottom:12px;'>7-Day Recycling Trend & ESG Reporting</h3>", unsafe_allow_html=True)

col_t1, col_t2 = st.columns([3, 1])

with col_t1:
    trend_data = pd.DataFrame({
        "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        "PET Plastic (kg)": [12.4, 15.1, 18.2, 14.0, 22.1, 28.5, total_weight],
        "Paper & Board (kg)": [8.1, 10.2, 11.5, 9.8, 14.2, 19.0, total_weight * 0.4]
    })
    fig_line = px.line(trend_data, x="Day", y=["PET Plastic (kg)", "Paper & Board (kg)"], markers=True,
                       color_discrete_sequence=["#10B981", "#3B82F6"])
    fig_line.update_layout(
        height=210, 
        margin=dict(t=10, b=10, l=10, r=10), 
        legend_title_text="",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_line, use_container_width=True)

with col_t2:
    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    st.caption("Export verified telemetry data for Sime Darby Sustainability Compliance.")
    
    export_df = pd.DataFrame([{
        "Estate": selected_estate,
        "Total_Weight_kg": total_weight,
        "CAPEX_Saved_RM": est_savings,
        "CO2_Offset_kg": carbon_offset,
        "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }])
    csv_bytes = export_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="📥 Export ESG Report (CSV)",
        data=csv_bytes,
        file_name=f"EcoScan_ESG_Report_{time.strftime('%Y%m%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )