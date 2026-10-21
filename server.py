from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)  # 允许跨域请求，防止 Streamlit 无法读取

# 模拟本地内存数据库（实际黑客松中，重启后会重置，但对于演示完全足够）
db = {
    "balance": 24.50,
    "total_weight": 15.4,
    "container_fill": 82.5,
    "history": [
        {"date": "2026-10-18", "type": "Aluminum Cans", "weight": 1.2, "earn": 3.60},
        {"date": "2026-10-19", "type": "PET Plastic Bottles", "weight": 2.5, "earn": 2.00},
        {"date": "2026-10-20", "type": "Paper & Cardboard", "weight": 5.4, "earn": 2.16}
    ]
}

# 📢 接口一：供 App 读取当前最新的钱包余额、累计重量和投递历史
@app.route('/api/v1/resident/data', methods=['GET'])
def get_resident_data():
    return jsonify(db)

# 📢 接口二：供 App 进行提现操作时重置余额
@app.route('/api/v1/resident/cashout', methods=['POST'])
def cashout():
    db["balance"] = 0.00
    return jsonify({"status": "success", "message": "Balance cashed out successfully"})

# 📢 接口三：供 mock_smart_bin.py (IoT 垃圾桶) 投递成功后，上传物理重量与 AI 纯度数据
@app.route('/api/v1/iot/disposal', methods=['POST'])
def receive_disposal():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    
    # 解析数据
    user_id = data.get("user_id")
    measured_weight = float(data.get("measured_weight_kg", 0.0))
    purity_factor = float(data.get("purity_factor", 1.0))
    
    # 核心商业逻辑计算：最终收益 = 重量 * 基础单价 (塑料 RM0.80/kg) * AI 纯度系数
    rate = 0.80
    earnings = round(measured_weight * rate * purity_factor, 2)
    
    # 实时更新共享内存数据库
    db["balance"] = round(db["balance"] + earnings, 2)
    db["total_weight"] = round(db["total_weight"] + measured_weight, 2)
    # 垃圾扔下去后，底楼集装箱容量增加
    db["container_fill"] = min(100.0, round(db["container_fill"] + (measured_weight * 0.5), 1))
    
    # 追加一条历史记录
    new_entry = {
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "type": "PET Plastic Bottles",
        "weight": measured_weight,
        "earn": earnings
    }
    db["history"].append(new_entry)
    
    print(f"📥 [SERVER] Received IoT Telemetry: {measured_weight}kg from {user_id}. Earnings: RM {earnings}")
    
    return jsonify({
        "status": "success",
        "payout_amount": earnings,
        "new_balance": db["balance"]
    })

if __name__ == '__main__':
    # 运行在 5000 端口
    app.run(host='0.0.0.0', port=5000, debug=True)
