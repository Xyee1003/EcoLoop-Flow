import requests
import json
import time
import qrcode

# 配置后端同学的服务器地址（本地测试一般是 localhost）
BACKEND_API = "http://localhost:5000/api/v1/iot/disposal"

def generate_terminal_qr(data_text):
    """
    在终端里直接用字符画 (ASCII Art) 打印出一个可以被手机扫描的二维码！
    """
    print(f"\n[IoT Config] Generating Secure Entry QR Code for Bin: {data_text}...")
    qr = qrcode.QRCode(version=1, box_size=1, border=1)
    qr.add_data(data_text)
    qr.make(fit=True)
    
    # render_as_alias=True 会在终端里用黑白块把二维码渲染出来
    qr.print_tty()

def start_smart_bin():
    print("==================================================")
    print("        EcoLoop-Flow - Smart Bin IoT Simulator    ")
    print("==================================================")
    
    # 模拟我们这个桶是 15 楼的塑料回收桶
    BIN_ID = "ELMINA_CONDO_FL15_PLASTIC"
    
    # 💥 核心亮点：启动时直接把垃圾桶的专属二维码打印在终端！
    generate_terminal_qr(BIN_ID)
    
    while True:
        print("\n[SYSTEM IDLE] Waiting for resident to scan QR code above...")
        print("💡 TIP: Point your Resident App camera at the QR code printed in the terminal!")
        
        user_id = input("\nEnter User ID to simulate successful Scan (e.g., user_tang_01): ").strip()
        if not user_id:
            continue
            
        print(f"\n[HATCH UNLOCKED] 🔵 Plastic Chute Gate is OPEN for User: {user_id}.")
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
        
        # ================== 构建发送的 IoT 报文 ==================
        payload = {
            "user_id": user_id,
            "bin_id": BIN_ID,
            "material_type": "Plastic",
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
