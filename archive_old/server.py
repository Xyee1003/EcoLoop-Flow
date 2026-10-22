from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import json
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}) # 允许任何源跨域联调

DB_FILE = "db_store.json"

# 默认演示初始数据
DEFAULT_DB = {
    "balance": 24.50,
    "total_weight": 15.4,
    "container_fill": 82.5,
    "history": [
        {"date": "2026-10-18", "type": "Aluminum Cans", "weight": 1.2, "earn": 3.60},
        {"date": "2026-10-19", "type": "PET Plastic Bottles", "weight": 2.5, "earn": 2.00},
        {"date": "2026-10-20", "type": "Paper & Cardboard", "weight": 5.4, "earn": 2.16}
    ]
}

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_DB.copy()
    return DEFAULT_DB.copy()

def save_db(data):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# 初始化数据库
db = load_db()

@app.route('/api/v1/resident/data', methods=['GET'])
def get_resident_data():
    global db
    db = load_db()
    return jsonify(db)

@app.route('/api/v1/resident/cashout', methods=['POST'])
def cashout():
    global db
    db = load_db()
    db["balance"] = 0.00
    save_db(db)
    return jsonify({"status": "success", "message": "Balance cashed out successfully"})

@app.route('/api/v1/developer/clear-container', methods=['POST'])
def clear_container():
    global db
    db = load_db()
    db["container_fill"] = 0.0 # 清空底楼集装箱
    save_db(db)
    return jsonify({"status": "success", "message": "Basement containers cleared successfully"})

@app.route('/api/v1/iot/disposal', methods=['POST'])
def receive_disposal():
    global db
    db = load_db()
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    
    user_id = data.get("user_id", "anonymous")
    measured_weight = float(data.get("measured_weight_kg", 0.0))
    purity_factor = float(data.get("purity_factor", 1.0))
    material_type = data.get("material_type", "PET Plastic Bottles")
    
    rate = 0.80
    earnings = round(measured_weight * rate * purity_factor, 2)
    
    db["balance"] = round(db["balance"] + earnings, 2)
    db["total_weight"] = round(db["total_weight"] + measured_weight, 2)
    db["container_fill"] = min(100.0, round(db["container_fill"] + (measured_weight * 0.5), 1))
    
    new_entry = {
        "date": datetime.date.today().strftime("%Y-%m-%d"),
        "type": material_type,
        "weight": measured_weight,
        "earn": earnings
    }
    db["history"].append(new_entry)
    save_db(db)
    
    print(f"[SERVER IoT] Synchronized: {measured_weight}kg of {material_type} from {user_id}. Earned: RM {earnings}")
    return jsonify({
        "status": "success",
        "payout_amount": earnings,
        "new_balance": db["balance"]
    })

# 供演示前初始化重置的接口
@app.route('/api/v1/system/reset', methods=['POST'])
def reset_system():
    global db
    db = DEFAULT_DB.copy()
    save_db(db)
    return jsonify({"status": "success", "message": "System database reset to initial demo state"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
