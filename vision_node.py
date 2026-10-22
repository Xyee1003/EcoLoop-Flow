import streamlit as st
import cv2
import numpy as np
import requests
import os

st.set_page_config(page_title="Node 2: AI Vision Camera", page_icon="📸", layout="wide")

# CSS 修复按钮白色样式
st.markdown("""
<style>
    div.stButton > button {
        background-color: #1E293B !important;
        color: #6FFFE9 !important;
        border: 1px solid #3A506B !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        background-color: #3B82F6 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

BRIDGE_URL = "http://127.0.0.1:5000/api"
ASSETS_DIR = "demo_assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

def load_user_image(stage_key):
    base_prefix = "s1" if stage_key == "stage1" else ("s2" if stage_key == "stage2" else "s3")
    candidate_names = [
        f"{base_prefix}.jpg", f"{base_prefix}.png", f"{base_prefix}.jpeg",
        f"{base_prefix}.jpg.png", f"{base_prefix}.png.png"
    ]
    for fname in candidate_names:
        img_path = os.path.join(ASSETS_DIR, fname)
        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            if img is not None:
                return cv2.resize(img, (640, 360))
                
    if os.path.exists(ASSETS_DIR):
        for f in os.listdir(ASSETS_DIR):
            if f.lower().startswith(base_prefix):
                img = cv2.imread(os.path.join(ASSETS_DIR, f))
                if img is not None:
                    return cv2.resize(img, (640, 360))

    placeholder = np.full((360, 640, 3), 25, dtype=np.uint8)
    cv2.putText(placeholder, f"File missing: {base_prefix}.jpg", 
                (40, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 165, 255), 2)
    return placeholder

def render_annotated_frame(base_img, boxes, banner_text, banner_color):
    frame = base_img.copy()
    for (x1, y1, x2, y2, label, color) in boxes:
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.45, 1)
        cv2.rectangle(frame, (x1, y1 - th - 8), (x1 + tw + 6, y1), color, -1)
        cv2.putText(frame, label, (x1 + 3, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.rectangle(frame, (0, 0), (640, 32), (15, 23, 42), -1)
    cv2.putText(frame, banner_text, (12, 21), cv2.FONT_HERSHEY_SIMPLEX, 0.50, banner_color, 2, cv2.LINE_AA)
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

st.markdown("## 📸 [ Node 2: Vision ] Edge AI Camera Inspector")
st.caption("Live Camera Feed • Multi-Object Material Detection • Contamination Test")

col_left, col_right = st.columns([2, 3])

with col_left:
    st.subheader("1. Select Input Source")
    input_mode = st.radio("Camera Source:", ["🎬 Preset Demo Scenarios (Your Photos)", "📷 Live Webcam / Phone Cam"])

    scenario_choice = st.selectbox(
        "Select Inspection Scenario:",
        [
            "Scenario 1: Mixed PET + Organic Banana Peel (Anomaly ❌)",
            "Scenario 2: PET Bottles + Residual Liquid Cola (50% Purity ⚠️)",
            "Scenario 3: Dispersed Clean PET Bottles (98% Purity ✅)"
        ]
    )

    live_img = None
    if "Live" in input_mode:
        cam_file = st.camera_input("Take a snapshot of the tray")
        if cam_file is not None:
            file_bytes = np.asarray(bytearray(cam_file.read()), dtype=np.uint8)
            live_img = cv2.resize(cv2.imdecode(file_bytes, 1), (640, 360))

    if "Scenario 1" in scenario_choice:
        stage_key = "stage1"
        weight_val = 0.45
        purity_val = 0
        is_anomaly = True  # 香蕉皮有机污染
        boxes = [
            (130, 110, 230, 310, "PET Plastic Bottle #1 (96%)", (38, 192, 28)),
            (390, 80, 480, 270, "PET Plastic Bottle #2 (94%)", (38, 192, 28)),
            (240, 110, 400, 270, "ANOMALY: BANANA_PEEL (98.4%)", (0, 0, 255))
        ]
        tray_items = [
            {"name": "PET Plastic Bottle #1", "status": "Clean Recyclable", "confidence": "96%", "ok": True},
            {"name": "PET Plastic Bottle #2", "status": "Clean Recyclable", "confidence": "94%", "ok": True},
            {"name": "Organic Waste (Banana Peel)", "status": "CONTAMINATION BLOCKED", "confidence": "98.4%", "ok": False}
        ]
        banner = ("EDGE AI: CONTAMINATION DETECTED (CHUTE LOCKED)", (0, 0, 255))

    elif "Scenario 2" in scenario_choice:
        stage_key = "stage2"
        weight_val = 1.00
        purity_val = 50
        is_anomaly = False # 🌟 设为 False，避免误触发香蕉皮报警
        boxes = [
            (130, 140, 280, 320, "PET Bottle #1 (95%)", (38, 192, 28)),
            (355, 120, 550, 340, "PET Bottle #2 (97%)", (38, 192, 28)),
            (275, 30, 365, 320, "WARN: LIQUID_RESIDUE (-50% Purity)", (0, 0, 255))
        ]
        tray_items = [
            {"name": "PET Plastic Bottle #1", "status": "Clean Recyclable", "confidence": "95%", "ok": True},
            {"name": "PET Plastic Bottle #2", "status": "Clean Recyclable", "confidence": "97%", "ok": True},
            {"name": "Cola Bottle (Liquid Residual)", "status": "LIQUID DETECTED (0 REWARD)", "confidence": "91.5%", "ok": False}
        ]
        banner = ("EDGE AI: LIQUID RESIDUAL DETECTED (CHUTE LOCKED)", (0, 0, 255))

    else:
        stage_key = "stage3"
        weight_val = 0.65
        purity_val = 98
        is_anomaly = False
        boxes = [
            (95, 230, 225, 350, "Premium PET #1 (98%)", (38, 192, 28)),
            (205, 220, 320, 350, "Premium PET #2 (99%)", (38, 192, 28)),
            (310, 160, 410, 270, "Premium PET #3 (97%)", (38, 192, 28)),
            (295, 240, 420, 350, "Premium PET #4 (98%)", (38, 192, 28))
        ]
        tray_items = [
            {"name": "Premium PET Bottle #1", "status": "Verified Clean & Flat", "confidence": "98%", "ok": True},
            {"name": "Premium PET Bottle #2", "status": "Verified Clean & Flat", "confidence": "99%", "ok": True},
            {"name": "Premium PET Bottle #3", "status": "Verified Clean & Flat", "confidence": "97%", "ok": True},
            {"name": "Premium PET Bottle #4", "status": "Verified Clean & Flat", "confidence": "98%", "ok": True}
        ]
        banner = ("EDGE AI: ALL ITEMS VERIFIED CLEAN PET (98% PURITY)", (38, 192, 28))

    weight_input = st.slider("Simulated Load Cell Weight (kg):", 0.10, 2.00, weight_val, 0.05)

    if st.button("🚀 AI SCAN & SEND TO USER APP", use_container_width=True):
        payload = {
            "tray_items": tray_items,
            "weight": weight_input,
            "purity": purity_val,
            "is_anomaly": is_anomaly
        }
        try:
            r = requests.post(f"{BRIDGE_URL}/vision/scan", json=payload, timeout=2.0)
            if r.status_code == 200:
                st.success("✅ Scan telemetry transmitted to Shared Bridge! Check User App & EcoBin.")
        except Exception as e:
            st.error(f"Cannot reach Shared Bridge server.py: {e}")

with col_right:
    st.subheader("2. Live Edge AI Object Detection Feed")
    base_frame = live_img if live_img is not None else load_user_image(stage_key)
    annotated_rgb = render_annotated_frame(base_frame, boxes, banner[0], banner[1])
    st.image(annotated_rgb, use_container_width=True, caption="Multi-Object Bounding Box Output (Real Photo Detection)")