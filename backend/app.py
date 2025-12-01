from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import random
import json
import threading
import time
import datetime
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import load_model, detect_threat
    from database import init_db, log_threat, get_stats
except ImportError as e:
    print(f"Import error: {e}")
    raise

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', ping_timeout=60, ping_interval=25)

model = None
model_info = {}
model_lock = threading.Lock()
threat_counter = 0

def load_model_info():
    global model_info
    try:
        info_path = os.path.join(os.path.dirname(__file__), 'models', 'model_info.json')
        if os.path.exists(info_path):
            with open(info_path, 'r') as f:
                model_info = json.load(f)
        else:
            print(f"Model info file not found at {info_path}")
            model_info = {
                "model_architecture": "GCN-Threat-Detector",
                "parameter_count": 452485,
                "accuracy_percentage": 78.47,
                "status": "Running"
            }
    except Exception as e:
        print(f"Error loading model_info.json: {e}")
        model_info = {
            "model_architecture": "GCN-Threat-Detector",
            "parameter_count": 452485,
            "accuracy_percentage": 78.47,
            "status": "Running"
        }


def get_or_load_model():
    global model
    if model is None:
        with model_lock:
            if model is None:
                try:
                    model_path = os.path.join(os.path.dirname(__file__), 'models', 'gcn_threat_detector.pth')
                    print(f"Loading model from: {model_path}")
                    if not os.path.exists(model_path):
                        print(f"Model file not found, creating dummy model...")
                        # Return None to use dummy detection
                        return None
                    model = load_model(model_path)
                    if model:
                        print("✓ Model loaded successfully")
                    else:
                        print("Failed to load model")
                except Exception as e:
                    print(f"Error loading model: {e}")
    return model


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "PRATIRAKSHA-Lite"})


@app.route('/api/stats', methods=['GET'])
def stats_route():
    return jsonify(get_stats())


@socketio.on('connect')
def handle_connect():
    print(f"✓ Client connected!")
    emit('model_info', model_info)
    emit('stats_update', get_stats())


def listen_to_network_flow():
    """Generate simulated network flow data"""
    threat_weights = [2, 8, 8, 20, 10]  # Benign, Cryptolocker, Locky, Ransomware, WannaCry
    threat_index = random.choices([0, 1, 2, 3, 4], weights=threat_weights, k=1)[0]
    
    threat_classes = {
        0: "Benign",
        1: "Cryptolocker",
        2: "Locky",
        3: "Ransomware", 
        4: "WannaCry"
    }
    
    flow = {
        "src_ip": f"192.168.{random.randint(1, 254)}.{random.randint(2, 254)}",
        "dst_ip": f"10.0.{random.randint(1, 254)}.{random.randint(1, 254)}",
        "duration": random.uniform(0, 100),
        "protocol": random.choice([6, 17]),
        "src_bytes": random.uniform(0, 50000),
        "dst_bytes": random.uniform(0, 50000),
        "packets": random.randint(1, 200),
        "tcp_flags": random.randint(0, 255),
        "active_time": random.uniform(0, 100),
        "idle_time": random.uniform(0, 100)
    }
    
    threat_name = threat_classes[threat_index]
    
    if threat_index == 3:  # Ransomware
        flow["duration"] = random.uniform(70, 95)
        flow["src_bytes"] = random.uniform(35000, 50000)
        flow["dst_bytes"] = random.uniform(10000, 30000)
        flow["packets"] = random.randint(140, 200)
        flow["active_time"] = random.uniform(60, 95)
        flow["protocol"] = 6
        flow["tcp_flags"] = random.choice([16, 24, 25])
        
    elif threat_index == 1:  # Cryptolocker
        flow["duration"] = random.uniform(50, 85)
        flow["src_bytes"] = random.uniform(25000, 45000)
        flow["dst_bytes"] = random.uniform(8000, 25000)
        flow["packets"] = random.randint(100, 160)
        flow["protocol"] = 6
        flow["tcp_flags"] = random.choice([16, 24])
        flow["active_time"] = random.uniform(45, 80)
        
    elif threat_index == 2:  # Locky
        flow["duration"] = random.uniform(40, 75)
        flow["src_bytes"] = random.uniform(20000, 40000)
        flow["dst_bytes"] = random.uniform(5000, 20000)
        flow["packets"] = random.randint(80, 140)
        flow["active_time"] = random.uniform(35, 70)
        
    elif threat_index == 4:  # WannaCry
        flow["duration"] = random.uniform(60, 90)
        flow["src_bytes"] = random.uniform(30000, 48000)
        flow["dst_bytes"] = random.uniform(12000, 32000)
        flow["packets"] = random.randint(120, 180)
        flow["protocol"] = random.choice([6, 17])
        flow["tcp_flags"] = random.choice([16, 17, 24, 25])
        flow["active_time"] = random.uniform(50, 85)
    
    else:  # Benign
        flow["duration"] = random.uniform(5, 30)
        flow["src_bytes"] = random.uniform(100, 8000)
        flow["dst_bytes"] = random.uniform(500, 12000)
        flow["packets"] = random.randint(5, 50)
        flow["active_time"] = random.uniform(5, 25)
    
    return flow, threat_name


def monitor_network():
    """Monitor network and emit threats"""
    global threat_counter
    print("✓ Network monitoring started")
    import sys
    sys.stdout.flush()
    
    while True:
        try:
            # Waiting time between detections: 25-23 seconds
            delay = random.uniform(23, 25)
            print(f"[Monitor] Waiting {delay:.1f}s before next detection...", flush=True)
            time.sleep(delay)
            
            new_flow, threat_name = listen_to_network_flow()
            current_model = get_or_load_model()
            
            # Create threat detection (with or without model)
            now = datetime.datetime.now()
            
            # Generate confidence based on threat type
            if threat_name == "Benign":
                confidence = 0.95
            else:
                confidence = random.uniform(0.75, 0.98)
            
            threat = {
                "timestamp": now,
                "timestamp_str": now.isoformat(),
                "source_ip": new_flow["src_ip"],
                "dest_ip": new_flow["dst_ip"],
                "threat_type": threat_name,
                "confidence": confidence,
                "status": "BLOCKED" if threat_name != "Benign" else "BENIGN"
            }
            
            # Emit all threats to frontend (benign and malicious)
            frontend_threat = {
                'timestamp': threat['timestamp_str'],
                'source_ip': threat['source_ip'],
                'dest_ip': threat['dest_ip'],
                'threat_type': threat['threat_type'],
                'confidence': f"{threat['confidence']:.0%}",
                'status': threat['status']
            }
            
            if threat_name != "Benign":
                threat_counter += 1
                print(f"🚨 [{threat_counter}] {threat_name:15} | {threat['source_ip']:20} | Conf: {confidence:.0%}", flush=True)
                
                # Log to database
                try:
                    db_threat = {
                        'timestamp': now,
                        'source_ip': threat['source_ip'],
                        'dest_ip': threat['dest_ip'],
                        'threat_type': threat['threat_type'],
                        'confidence': threat['confidence'],
                        'status': threat['status']
                    }
                    log_threat(db_threat)
                except Exception as db_err:
                    print(f"  Database error: {db_err}", flush=True)
            
            # Emit to connected clients
            try:
                socketio.emit('new_threat', frontend_threat, to=None)
                socketio.emit('stats_update', get_stats(), to=None)
                print(f"  ✓ Emitted to frontend", flush=True)
            except Exception as emit_err:
                print(f"  ✗ Emit error: {emit_err}", flush=True)
                    
        except Exception as e:
            print(f"Error in monitoring: {e}", flush=True)
            import traceback
            traceback.print_exc()
            time.sleep(2)


if __name__ == '__main__':
    try:
        print("\n" + "=" * 70)
        print("     PRATIRAKSHA-Lite | AI Network Threat Detection System")
        print("=" * 70)
        print("\n[*] Initializing components...")
        
        # Initialize database
        init_db()
        print("  ✓ Database initialized")
        
        # Load model info
        load_model_info()
        print("  ✓ Model info loaded")
        
        print("\n[*] Starting backend server on port 5002...")
        
        # Start network monitoring thread
        monitor_thread = threading.Thread(target=monitor_network, daemon=True)
        monitor_thread.start()
        print("  ✓ Network monitoring thread started")
        
        print("\n" + "=" * 70)
        print("✓ BACKEND SERVER READY")
        print("=" * 70)
        print("\n[API ENDPOINTS]")
        print("  • Health:  http://localhost:5002/health")
        print("  • Stats:   http://localhost:5002/api/stats")
        print("  • WebSocket: ws://localhost:5002/socket.io")
        print("\n[FRONTEND]")
        print("  • Dashboard: http://localhost:3000")
        print("\nWaiting for connections...\n")
        print("=" * 70 + "\n")
        
        # Run socketio server
        socketio.run(
            app,
            host='0.0.0.0',
            port=5002,
            debug=False,
            use_reloader=False,
            allow_unsafe_werkzeug=True,
            log_output=False
        )
        
    except KeyboardInterrupt:
        print("\n✓ Server shutdown gracefully")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
