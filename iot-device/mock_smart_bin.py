import requests
import json
import time
import random

# 配置后端同学的服务器地址（本地测试一般是 localhost）
BACKEND_API = "http://localhost:5000/api/v1/iot/disposal"

def start_smart_bin():
    print("==================================================")
    print("        EcoLoop-Flow - Smart Bin IoT Simulator    ")
    print("==================================================")
    
    while True:
        print("\n[SYSTEM IDLE] Waiting for resident to scan QR code...")
        user_id = input("Enter User ID (e.g., user_tang_01) to simulate scan: ").strip()
        if not user_id:
            continue
            
        print("\nSelect Bin Type:")
        print("1. Paper (🟢 Paper Chute)")
        print("2. Aluminum (🔴 Metal Chute)")
        print("3. Plastic (🔵 Plastic Chute)")
        choice = input("Choose (1-3): ").strip()
        
        material_map = {"1": "Paper", "2": "Aluminum", "3": "Plastic"}
        if choice not in material_map:
            print("[ERROR] Invalid choice. Try again.")
            continue
        material = material_map[choice]
        
        print(f"\n[HATCH UNLOCKED] {material} Bin Hatch is OPEN.")
        raw_weight_input = input("Enter Simulated Garbage Weight in kg (e.g., 0.85): ").strip()
        
        try:
            raw_weight = float(raw_weight_input)
        except ValueError:
            print("[ERROR] Weight must be a number!")
            continue
            
        print("\n[AI SCANNING] Camera running Edge AI Image and Purity Inspection...")
        time.sleep(1.5)  # 模拟 AI 计算时间
        
        # ================== 核心：你的防作弊/纯度校验算法 ==================
        purity = 1.0
        is_anomaly = False
        
        if material == "Plastic":
            # 异常判定：一个塑料袋里如果塑料超过 1.8kg，大概率是灌水或塞了石头
            if raw_weight > 1.8:
                print("🚨 [WARNING] Anomaly Detected: Plastic volume-to-weight ratio is suspicious!")
                print("🚨 [WARNING] Possible water/impurity injection detected.")
                purity = 0.1
                is_anomaly = True
            elif 0.8 < raw_weight <= 1.8:
                purity = 0.85  # 微瑕（含少量杂质或未清空瓶子）
                print("⚠️ [NOTICE] Minor impurity detected. Purity factor adjusted to 0.85.")
            else:
                purity = 1.0   # 完美干净的塑料瓶
                print("✅ [AI PASS] Clean Plastic Bottles detected.")
                
        elif material == "Paper":
            if raw_weight > 5.0:  # 纸箱异常重，可能打湿了水骗秤
                purity = 0.3
                is_anomaly = True
                print("🚨 [WARNING] Anomaly Detected: Paper density is too high. Suspected wet paper!")
            else:
                print("✅ [AI PASS] Clean cardboard cardboard detected.")
        
        # ================== 构建发送的 IoT 报文 ==================
        payload = {
            "user_id": user_id,
            "bin_id": f"ELMINA_CONDO_{material.upper()}_BIN",
            "material_type": material,
            "measured_weight_kg": raw_weight,
            "purity_factor": purity,
            "is_anomaly": is_anomaly
        }
        
        # ================== 发送数据至云端/后端 ==================
        print(f"\n[IoT Sync] Transmitting data to backend server...")
        try:
            response = requests.post(BACKEND_API, json=payload)
            if response.status_code == 200:
                result = response.json()
                print("--------------------------------------------------")
                print(f"🎉 [SUCCESS] Cloud Sync Completed!")
                print(f"🔑 Transaction Status: {result.get('status')}")
                print(f"💰 Payout Disbursed: RM {result.get('payout_amount')}")
                print("--------------------------------------------------")
            else:
                print(f"❌ [SERVER ERROR] Cloud rejected data. Response: {response.text}")
        except requests.exceptions.ConnectionError:
            print("\n❌ [CONNECTION ERROR] Could not connect to backend server.")
            print(f"   Make sure your teammate's backend server is running and BACKEND_API matches!")
            print(f"   Payload we tried to send: {json.dumps(payload, indent=2)}")

if __name__ == "__main__":
    start_smart_bin()
