"""
Comprehensive system test for PRATIRAKSHA
"""

print('='*60)
print('COMPREHENSIVE SYSTEM TEST')
print('='*60)

# Test 1: Database
print('\n[1/4] TESTING DATABASE...')
from database import init_db, log_threat, get_stats
try:
    init_db()
    log_threat({'source_ip': '192.168.1.100', 'dest_ip': '192.168.1.1', 'threat_type': 'Ransomware', 'confidence': 0.95, 'status': 'BLOCKED'})
    stats = get_stats()
    print(f'✓ Database OK')
    print(f'  Threats Detected: {stats["threats_detected"]}')
    print(f'  Threats Blocked: {stats["threats_blocked"]}')
except Exception as e:
    print(f'✗ Database Error: {e}')

# Test 2: Model
print('\n[2/4] TESTING MODEL...')
try:
    from utils import load_model
    model = load_model('models/trained_model.pth')
    if model:
        print(f'✓ Model Loaded Successfully')
    else:
        print(f'✗ Model Loading Failed')
except Exception as e:
    print(f'✗ Model Error: {e}')

# Test 3: Backend API
print('\n[3/4] TESTING FLASK API...')
try:
    from app import app
    client = app.test_client()
    response = client.get('/health')
    if response.status_code == 200:
        print(f'✓ Health Check: {response.get_json()}')
    response = client.get('/api/stats')
    if response.status_code == 200:
        print(f'✓ Stats Endpoint Working')
except Exception as e:
    print(f'✗ Flask Error: {e}')

# Test 4: Threat Detection
print('\n[4/4] TESTING THREAT DETECTION...')
try:
    from utils import detect_threat, load_model
    model = load_model('models/trained_model.pth')
    if model:
        test_flow = {
            'src_ip': '192.168.1.50',
            'dst_ip': '192.168.1.1',
            'duration': 25.0,
            'protocol': 6,
            'src_bytes': 5000.0,
            'dst_bytes': 8000.0,
            'packets': 50,
            'tcp_flags': 24,
            'active_time': 15.0,
            'idle_time': 5.0
        }
        threat = detect_threat(model, test_flow)
        if threat:
            print(f'✓ Threat Detection Working')
            print(f'  Detected: {threat["threat_type"]} (Confidence: {threat["confidence"]:.4f})')
        else:
            print(f'✗ Threat Detection Failed')
except Exception as e:
    print(f'✗ Detection Error: {e}')

print('\n' + '='*60)
print('✓ SYSTEM TEST COMPLETE')
print('='*60)
