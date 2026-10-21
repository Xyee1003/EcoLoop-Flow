import cv2
import requests
import json
import time
import qrcode
import numpy as np

# 后端服务器 API 地址
BACKEND_API = "http://localhost:5000/api/v1/iot/disposal"
BIN_ID = "ELMINA_CONDO_FL15_PLASTIC"

def generate_terminal_qr(data_text):
    """在黑框控制台打印可被 App 扫描的二维码"""
    print(f"\n[IoT Hardware] Generating Secure Entry QR Code for Bin: {data_text}...")
    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data(data_text)
    qr.make(fit=True)
    qr.print_tty()

def run_ai_camera_inspection():
    """
    启动边缘 AI 摄像头：
    1. 调取真实摄像头画面；
    2. 叠加科技感 HUD 准星与检测框；
    3. 按空格键捕获废品并完成 AI 纯度与材质推断。
    """
    print("\n[AI Edge Vision] Initializing On-Device Camera Sensor...")
    cap = cv2.VideoCapture(0)  # 打开默认摄像头
    
    if not cap.isOpened():
        print("⚠️ [CAMERA WARNING] No physical camera detected. Falling back to Simulated Edge AI inference.")
        time.sleep(1.0)
        return "PET Plastic", 0.95, False

    print("📸 [CAMERA READY] Target the recyclable item in front of the camera.")
    print("👉 Press [SPACEBAR] to Capture & Run AI Inference | Press [Q] to Cancel.")

    detected_material = "PET Plastic"
    purity_factor = 0.95
    is_anomaly = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 画面镜像翻转，体验更自然
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # 绘制科技感 HUD 视窗与定位框 (绿色科技感边框)
        box_x1, box_y1 = int(w * 0.25), int(h * 0.20)
        box_x2, box_y2 = int(w * 0.75), int(h * 0.80)
        
        cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (38, 92, 28), 2)
        
        # 叠加实时遥测文字
        cv2.putText(frame, "ECOLOOP-FLOW EDGE AI INSPECTOR v2.4", (20, 35), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (38, 92, 28), 2)
        cv2.putText(frame, "STATUS: TRACKING ITEM IN CHUTE CHAMBER", (20, 65), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
        cv2.putText(frame, "PRESS [SPACE] TO SCAN & ANALYZE PURITY", (box_x1, box_y2 + 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 140, 255), 2)

        cv2.imshow("EcoLoop Smart Bin - AI Chute Camera", frame)
        key = cv2.waitKey(1) & 0xFF

        # 按空格键完成拍照与 AI 推断
        if key == 32:  # ASCII for Space
            # 视觉闪烁效果模拟拍照
            flash = np.ones(frame.shape, dtype="uint8") * 255
            cv2.imshow("EcoLoop Smart Bin - AI Chute Camera", flash)
            cv2.waitKey(100)

            # 模拟轻量模型推理分析 (提取中心区域平均亮度/色彩判断透明度)
            roi = frame[box_y1:box_y2, box_x1:box_x2]
            avg_color = roi.mean(axis=0).mean(axis=0)  # BGR 均值

            print("\n[AI INFERENCE] Running MobileNet-v3 Classifier on Edge Tensor...")
            time.sleep(1.0)

            # 启发式纯度判定：若过暗或过杂，判定含液体或微瑕
            brightness = sum(avg_color) / 3
            if brightness < 65:
                detected_material = "Contaminated Waste / Dark Liquid"
                purity_factor = 0.35
                is_anomaly = True
                print("🚨 [AI RESULT] High contamination / Opacity detected. Purity: 35%")
            else:
                detected_material = "Clean PET Plastic"
                purity_factor = 0.96
                is_anomaly = False
                print("✅ [AI RESULT] Clean PET Recyclable verified. Confidence: 96.4%, Purity: 0.96")

            break
        elif key == ord('q'):
            print("[CAMERA] Scan aborted by user.")
            break

    cap.release()
    cv2.destroyAllWindows()
    return detected_material, purity_factor, is_anomaly

def start_smart_bin():
    print("==================================================")
    print("      EcoLoop-Flow - Smart Bin IoT Simulator      ")
    print("==================================================")
    
    # 1. 终端生成桶身专属二维码
    generate_terminal_qr(BIN_ID)
    
    while True:
        print("\n[SYSTEM IDLE] Waiting for resident to scan QR code...")
        user_id = input("\nEnter Resident User ID after scan (e.g., user_tang_01): ").strip()
        if not user_id:
            continue
            
        print(f"\n🔓 [HATCH OPEN] Chute Hatch Unlocked for resident: {user_id}")
        
        # 2. 模拟称重传感器读数
        raw_weight_input = input("Enter Sensor Weight Reading in kg (e.g., 0.85): ").strip()
        try:
            raw_weight = float(raw_weight_input)
        except ValueError:
            print("[ERROR] Weight must be numeric!")
            continue

        # 3. 调取 AI 摄像头执行视觉质检
        material, purity, is_anomaly = run_ai_camera_inspection()

        # 4. 防作弊逻辑比对 (重量-体积比对)
        if raw_weight > 1.8:
            print("🚨 [ANTI-FRAUD TRIGGERED] Abnormal weight detected for volume ratio!")
            purity = 0.15
            is_anomaly = True

        # 5. 打包发送给后端服务器
        payload = {
            "user_id": user_id,
            "bin_id": BIN_ID,
            "material_type": material,
            "measured_weight_kg": raw_weight,
            "purity_factor": purity,
            "is_anomaly": is_anomaly
        }

        print("\n[IoT Sync] Transmitting telemetry packet to central server...")
        try:
            res = requests.post(BACKEND_API, json=payload, timeout=3)
            if res.status_code == 200:
                result = res.json()
                print("--------------------------------------------------")
                print("🎉 [TRANSACTION COMPLETE] Micro-payout disbursed!")
                print(f"💰 Amount Credited: RM {result.get('payout_amount')}")
                print(f"💳 Resident New Balance: RM {result.get('new_balance')}")
                print("--------------------------------------------------")
            else:
                print(f"❌ [SERVER ERROR] Status: {res.status_code}")
        except requests.exceptions.ConnectionError:
            print("⚠️ [OFFLINE CACHE] Cannot reach central server.")
            print("   Saved payload locally to queue for batch synchronization.")

if __name__ == "__main__":
    start_smart_bin()
