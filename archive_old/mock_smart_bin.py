import cv2
import numpy as np
import time
import requests
import urllib.request
import os

# ==================== 🛠️ 模拟环境配置 ====================
BACKEND_API_URL = "http://127.0.0.1:5000/api/v1/resident/submit-deposit"

# 🌟 三个场景的高清实物大图 URL (精心挑选的免版权、高画质工业废品检测场景图)
IMAGE_URLS = {
    "scenario_1": "https://images.unsplash.com/photo-1611284446314-60a58ac0deb9?auto=format&fit=crop&w=640&q=80", # 废塑料与杂质堆
    "scenario_2": "https://images.unsplash.com/photo-1542601906990-b4d3fb778b09?auto=format&fit=crop&w=640&q=80", # 泥泞与脏塑料瓶
    "scenario_3": "https://images.unsplash.com/photo-1528190336454-13cd56b45b5a?auto=format&fit=crop&w=640&q=80"  # 撕标、捏扁的完美PET塑料瓶堆
}

# 本地缓存路径
CACHE_DIR = "demo_assets"
if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

# 3段式 Demo 剧情定义
DEMO_SCENARIOS = [
    {
        "item_name": "Mixed Plastics with Organic Waste",
        "purity": 0,
        "is_anomaly": True,
        "hud_color": (0, 0, 255),  # 红色 BGR
        "msg": "❌ [AI REJECTED] Organic waste detected (Banana Peel). Lock engaged. Please remove the anomaly.",
        "purity_coefficient": 0.0,
        "img_path": os.path.join(CACHE_DIR, "scene1.jpg"),
        "img_url": IMAGE_URLS["scenario_1"]
    },
    {
        "item_name": "Contaminated PET Bottles",
        "purity": 50,
        "is_anomaly": False,
        "hud_color": (0, 140, 255),  # 黄色 BGR
        "msg": "⚠️ [AI WARNED] Contaminated PET (Liquid Residual detected). Shute unlocked with 50% payout penalty.",
        "purity_coefficient": 0.5,
        "img_path": os.path.join(CACHE_DIR, "scene2.jpg"),
        "img_url": IMAGE_URLS["scenario_2"]
    },
    {
        "item_name": "Premium PET Bottles",
        "purity": 98,
        "is_anomaly": False,
        "hud_color": (38, 192, 28),  # 绿色 BGR
        "msg": "✅ [AI VERIFIED] Premium Clean PET. 98% purity. Lock disengaged. Payout processing...",
        "purity_coefficient": 1.0,
        "img_path": os.path.join(CACHE_DIR, "scene3.jpg"),
        "img_url": IMAGE_URLS["scenario_3"]
    }
]

def download_assets():
    """静默下载高清实物演示图片"""
    print("📦 [Asset Preloader] Pre-loading high-resolution industrial waste imagery for Demo...")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for sc in DEMO_SCENARIOS:
        if not os.path.exists(sc["img_path"]):
            print(f"  -> Downloading {os.path.basename(sc['img_path'])}...")
            try:
                req = urllib.request.Request(sc["img_url"], headers=headers)
                with urllib.request.urlopen(req) as response, open(sc["img_path"], 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"  ⚠️ Download failed for {os.path.basename(sc['img_path'])}: {e}. Generating fallback canvas.")

# 一键预载
download_assets()

def run_ai_camera_inspection(stage_index):
    """
    启动边缘 AI 摄像头：
    - 🟢 【方案 C】：直接在 OpenCV 画面中载入真实的工业废塑料现场照片，并在上方绘制精准的目标检测红/黄/绿框！
    """
    scenario = DEMO_SCENARIOS[stage_index]
    print(f"\n[AI Edge Vision] Running Demo Stage {stage_index+1}/3: Scan Item...")
    
    # 尝试加载下载好的高清实景照片
    frame = cv2.imread(scenario["img_path"])
    
    # 如果图片未能成功加载，生成一张优雅的暗色背景做兜底
    if frame is None:
        frame = np.ones((480, 640, 3), dtype="uint8") * 24
    else:
        # 将图片裁剪/缩放到标准的 640x480 分辨率，以便铺满窗口
        frame = cv2.resize(frame, (640, 480))

    h, w, _ = frame.shape
    box_x1, box_y1 = int(w * 0.12), int(h * 0.12)
    box_x2, box_y2 = int(w * 0.88), int(h * 0.88)

    # 制作暗色科技半透明滤镜，突出中间的 AI 检测框
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (w, h), (10, 10, 10), -1)
    # 局部还原亮色区域（即扫描框内部保留原图亮度）
    cv2.rectangle(overlay, (box_x1, box_y1), (box_x2, box_y2), (0, 0, 0), -1)
    frame = cv2.addWeighted(overlay, 0.45, frame, 0.55, 0)

    # ==================== 🌟 方案 C：在实物照片上精准叠加 AI 检测框 🌟 ====================
    
    # 剧情 1：在真实的塑料瓶堆照片里，用重红方框圈出隐藏的有机香蕉皮异常
    if stage_index == 0:
        # 给周围的背景塑料废弃物框上细绿框
        cv2.rectangle(frame, (box_x1 + 25, box_y1 + 40), (box_x1 + 160, box_y1 + 180), (38, 192, 28), 1)
        cv2.putText(frame, "PET Plastic (89%)", (box_x1 + 25, box_y1 + 32), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (38, 192, 28), 1, cv2.LINE_AA)
        
        cv2.rectangle(frame, (box_x1 + 280, box_y1 + 100), (box_x1 + 440, box_y1 + 240), (38, 192, 28), 1)
        cv2.putText(frame, "Mixed Plastic (91%)", (box_x1 + 280, box_y1 + 92), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (38, 192, 28), 1, cv2.LINE_AA)

        # 在实景中央最显眼的地方，精准绘制香蕉皮红框（模拟 AI 在大堆塑料中提取异常）
        peel_x1, peel_y1, peel_x2, peel_y2 = box_x1 + 110, box_y1 + 120, box_x1 + 310, box_y1 + 280
        cv2.rectangle(frame, (peel_x1, peel_y1), (peel_x2, peel_y2), (0, 0, 255), 2) # 红色异常框
        cv2.putText(frame, "ANOMALY: Banana Peel (Organic)", (peel_x1, peel_y1 - 18), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "System Lock Engaged (98.4%)", (peel_x1, peel_y2 + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1, cv2.LINE_AA)

    # 剧情 2：在污水/泥泞脏瓶堆照片里，红绿框并存，黄框圈出并警告带残留液体的脏瓶
    elif stage_index == 1:
        # 周边其他普通瓶
        cv2.rectangle(frame, (box_x1 + 30, box_y1 + 50), (box_x1 + 180, box_y1 + 170), (38, 192, 28), 1)
        cv2.putText(frame, "PET Bottle (94%)", (box_x1 + 30, box_y1 + 42), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (38, 192, 28), 1, cv2.LINE_AA)

        # 核心脏瓶目标，圈出黄框
        dirty_x1, dirty_y1, dirty_x2, dirty_y2 = box_x1 + 150, box_y1 + 90, box_x1 + 380, box_y1 + 290
        cv2.rectangle(frame, (dirty_x1, dirty_y1), (dirty_x2, dirty_y2), (0, 140, 255), 2) # 黄色警告框
        cv2.putText(frame, "ALERT: Dirty PET (Residual Liquid)", (dirty_x1, dirty_y1 - 18), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 140, 255), 1, cv2.LINE_AA)
        cv2.putText(frame, "Purity Penalty Applied: 50% Credit", (dirty_x1, dirty_y2 + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 140, 255), 1, cv2.LINE_AA)

    # 剧情 3：在完美的洗净捏扁瓶堆实物图上，全线拉满绿色检测框，展现顶级分类
    elif stage_index == 2:
        # 对画面中多个被识别到的完美可回收物叠加上错落有致的绿色目标框
        targets = [
            (30, 40, 180, 160, "#1"),
            (190, 50, 310, 200, "#2"),
            (60, 180, 250, 320, "#3"),
            (260, 190, 430, 330, "#4")
        ]
        for tx1, ty1, tx2, ty2, idx in targets:
            cv2.rectangle(frame, (box_x1 + tx1, box_y1 + ty1), (box_x1 + tx2, box_y1 + ty2), (38, 192, 28), 2)
            cv2.putText(frame, f"Premium PET {idx} (98%)", (box_x1 + tx1, box_y1 + ty1 - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (38, 192, 28), 1, cv2.LINE_AA)

    # ==============================================================================

    # 绘制边缘 AI 外部定位大框
    cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), scenario["hud_color"], 2)
    
    # 绘制高大上的工业中控流 HUD
    cv2.putText(frame, "ECOLOOP-FLOW EDGE AI CLASSIFIER v2.5", (20, 35), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, scenario["hud_color"], 2, cv2.LINE_AA)
    cv2.putText(frame, f"STATUS: {scenario['item_name'].upper()}", (20, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, scenario["hud_color"], 1, cv2.LINE_AA)
    cv2.putText(frame, "PRESS [SPACE] TO CONFIRM AI ANALYSIS", (20, 85), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (180, 180, 180), 1, cv2.LINE_AA)
    
    cv2.imshow("EcoLoop Smart Bin - Single-Camera AI Inspector", frame)
    
    while True:
        key = cv2.waitKey(1) & 0xFF
        if key == 32: # 按空格确定扫描并执行结算
            # 镜头曝光闪烁效果
            flash = np.ones(frame.shape, dtype="uint8") * 255
            cv2.imshow("EcoLoop Smart Bin - Single-Camera AI Inspector", flash)
            cv2.waitKey(80)
            
            print(f"\n[AI INFERENCE] Analyzing textures, volume, and material specs...")
            time.sleep(1.0)
            print(scenario["msg"])
            break
            
    cv2.destroyAllWindows()
    return scenario["item_name"], scenario["purity"], scenario["is_anomaly"]


def main():
    print("====================================================")
    print("      EcoLoop-Flow IoT Smart Bin Console v2.5       ")
    print("====================================================")
    
    for i in range(3):
        print(f"\n🚀 Ready for Deposit Scenario {i+1}/3...")
        input("Press Enter to activate the smart bin lid scanning...")
        
        item_name, purity, is_anomaly = run_ai_camera_inspection(i)
        
        if is_anomaly:
            print("🚫 Deposit canceled. Shute remains locked.")
            continue
            
        weight_input = input(f"Enter simulated weight for {item_name} (in kg, e.g., 0.45): ")
        try:
            weight = float(weight_input)
        except ValueError:
            weight = 0.35
            
        scenario = DEMO_SCENARIOS[i]
        final_purity = purity / 100.0
        
        payload = {
            "weight": weight,
            "purity": final_purity,
            "item_type": item_name
        }
        
        print("📡 Sending telemetry to central server...")
        try:
            res = requests.post(BACKEND_API_URL, json=payload, timeout=2.0)
            if res.status_code == 200:
                print("✅ Telemetry synced successfully!")
                print(f"💰 Payout calculated: RM {weight * 10 * final_purity:.2f} (Purity Coefficient: {final_purity})")
            else:
                print("⚠️ Server returned an error, check backend connection.")
        except Exception as e:
            print(f"⚠️ Failed to connect to backend server: {e}")
            
    print("\n🎉 Demo walk-through finished successfully!")

if __name__ == "__main__":
    main()
