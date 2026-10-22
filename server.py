from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

STATE = {
    "bin_id": "BIN EC-04",
    "machine_state": "IDLE",  # IDLE | SCANNED | ALARM | DROPPING
    "latch_open": False,
    "shaker_active": False,
    "speaker_msg": "EcoScan Bin Standby. Ready for drop-off.",
    "speaker_mode": "NORMAL", # NORMAL | WARNING | ALARM | SUCCESS
    "load_cell_weight": 0.0,
    "purity": 100,
    "is_anomaly": False,
    "tray_items": [],
    "wallet_balance": 42.60,
    "month_earned": 15.35,
    "total_recycled_kg": 40.2,
    "container_fill": 82.5, # 🌟 与 Developer Portal 绑定的集装箱容量 (%)
    "co2_avoided": 12.8,
    "water_saved": 284.0,
    "materials_kg": { "Plastic": 22.4, "Paper": 11.2, "Glass": 6.6 },
    "activities": [],
    "last_updated": time.time(),
    "trigger_id": 0
}

@app.route('/api/state', methods=['GET'])
def get_state():
    if STATE["machine_state"] == "DROPPING" and (time.time() - STATE["last_updated"] > 4.5):
        STATE["machine_state"] = "IDLE"
        STATE["latch_open"] = False
        STATE["shaker_active"] = False
        STATE["load_cell_weight"] = 0.0
        STATE["tray_items"] = []
        STATE["is_anomaly"] = False
        STATE["speaker_msg"] = "Hatch closed and locked. Ready for next drop-off."
        STATE["speaker_mode"] = "NORMAL"
    return jsonify(STATE), 200

@app.route('/api/resident/link', methods=['POST', 'OPTIONS'])
def resident_link():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    STATE["speaker_msg"] = "Account linked via NFC. Tray unlocked. Please place recyclables."
    STATE["speaker_mode"] = "NORMAL"
    STATE["trigger_id"] += 1
    return jsonify({"status": "linked", "state": STATE}), 200

@app.route('/api/vision/scan', methods=['POST', 'OPTIONS'])
def vision_scan():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    data = request.json or {}
    STATE["tray_items"] = data.get("tray_items", [])
    STATE["load_cell_weight"] = float(data.get("weight", 0.0))
    STATE["purity"] = int(data.get("purity", 100))
    STATE["is_anomaly"] = bool(data.get("is_anomaly", False))
    STATE["last_updated"] = time.time()
    STATE["trigger_id"] += 1

    if STATE["is_anomaly"] and STATE["purity"] == 0:
        STATE["machine_state"] = "ALARM"
        STATE["latch_open"] = False
        STATE["shaker_active"] = False
        STATE["speaker_msg"] = "ALERT! Organic contamination detected on tray. Chute latch locked!"
        STATE["speaker_mode"] = "ALARM"
    elif STATE["purity"] <= 50:
        STATE["machine_state"] = "ALARM"
        STATE["latch_open"] = False
        STATE["shaker_active"] = False
        STATE["speaker_msg"] = "WARNING! Liquid residue detected (Purity <= 50%). Bin locked. Please empty liquid!"
        STATE["speaker_mode"] = "ALARM"
    else:
        STATE["machine_state"] = "SCANNED"
        STATE["latch_open"] = False
        STATE["shaker_active"] = True
        STATE["speaker_msg"] = f"Scan complete. Verified clean PET. Weight {STATE['load_cell_weight']} kg. Please confirm deposit on app."
        STATE["speaker_mode"] = "NORMAL"

    return jsonify({"status": "ok", "state": STATE}), 200

@app.route('/api/resident/confirm', methods=['POST', 'OPTIONS'])
def resident_confirm():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if not STATE["tray_items"] or STATE["is_anomaly"] or STATE["purity"] <= 50:
        return jsonify({"status": "rejected", "state": STATE}), 400

    w = STATE["load_cell_weight"]
    payout = round(w * 10.0 * (STATE["purity"] / 100.0), 2)

    # 🌟 数据累加并同步更新集装箱容量
    STATE["wallet_balance"] = round(STATE["wallet_balance"] + payout, 2)
    STATE["month_earned"] = round(STATE["month_earned"] + payout, 2)
    STATE["total_recycled_kg"] = round(STATE["total_recycled_kg"] + w, 1)
    STATE["co2_avoided"] = round(STATE["co2_avoided"] + w * 1.5, 1)
    STATE["water_saved"] = round(STATE["water_saved"] + w * 12.0, 0)
    
    # 模拟塑料增加
    STATE["materials_kg"]["Plastic"] = round(STATE["materials_kg"]["Plastic"] + w, 1)
    # 集装箱容量根据新增重量相应递增，上限 100%
    STATE["container_fill"] = min(100.0, round(STATE["container_fill"] + (w * 3.5), 1))

    new_activity = {
        "date": "Just now",
        "place": "Bin EC-04 · Park Lobby",
        "detail": f"Plastic ({STATE['purity']}% Purity)",
        "weight": f"{w:.2f} kg",
        "amount": f"+ RM {payout:.2f}",
        "icon": "bottle",
        "color": "mint",
    }
    STATE["activities"].insert(0, new_activity)

    STATE["machine_state"] = "DROPPING"
    STATE["latch_open"] = True
    STATE["shaker_active"] = True
    STATE["speaker_msg"] = f"Deposit confirmed! Hatch open. Dropping items to chute. RM {payout:.2f} added to EcoWallet!"
    STATE["speaker_mode"] = "SUCCESS"
    STATE["last_updated"] = time.time()
    STATE["trigger_id"] += 1

    return jsonify({"status": "confirmed", "payout": payout, "state": STATE}), 200

# 🌟 新增：Developer 清空底层集装箱接口
@app.route('/api/developer/clear', methods=['POST', 'OPTIONS'])
def developer_clear():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    STATE["container_fill"] = 0.0
    STATE["speaker_msg"] = "Basement storage cleared by facility dispatch team. Telemetry reset."
    STATE["speaker_mode"] = "NORMAL"
    STATE["last_updated"] = time.time()
    STATE["trigger_id"] += 1
    return jsonify({"status": "cleared", "state": STATE}), 200

@app.route('/api/reset', methods=['POST', 'OPTIONS'])
def reset_tray():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    STATE["machine_state"] = "IDLE"
    STATE["latch_open"] = False
    STATE["shaker_active"] = False
    STATE["load_cell_weight"] = 0.0
    STATE["purity"] = 100
    STATE["is_anomaly"] = False
    STATE["tray_items"] = []
    STATE["speaker_msg"] = "Tray cleared. EcoScan Bin Standby."
    STATE["speaker_mode"] = "NORMAL"
    STATE["last_updated"] = time.time()
    STATE["trigger_id"] += 1
    return jsonify({"status": "reset", "state": STATE}), 200

if __name__ == '__main__':
    print("🌐 EcoScan Shared Bridge Server running on http://127.0.0.1:5000")
    app.run(host='127.0.0.1', port=5000, debug=False)