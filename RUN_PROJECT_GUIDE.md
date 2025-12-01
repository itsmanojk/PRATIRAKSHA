# 🚀 PRATIRAKSHA - Project Execution Guide

## Project Overview
- **Backend**: Flask REST API with PyTorch ML Model (Python)
- **Frontend**: React Dashboard (Node.js/JavaScript)
- **Port Configuration**: 
  - Backend: `http://localhost:5000`
  - Frontend: `http://localhost:3000`

---

## ✅ STEP 1: Backend Setup (Terminal 1)

### 1.1 Navigate to Backend
```bash
cd c:\Desktop\PRATIRAKSHA-Production\backend
```

### 1.2 Install Core Dependencies
```bash
pip install Flask==2.3.2 flask-cors==3.0.10 flask-socketio==5.3.4
pip install python-dotenv SQLAlchemy numpy pandas scikit-learn
```

### 1.3 Start Backend Server
```bash
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

✅ **Backend is now running on `http://localhost:5000`**

---

## ✅ STEP 2: Frontend Setup (Terminal 2)

### 2.1 Navigate to Frontend
```bash
cd c:\Desktop\PRATIRAKSHA-Production\frontend
```

### 2.2 Install Node.js Dependencies
```bash
npm install
```

(This downloads ~500MB of node_modules, may take 2-5 minutes)

### 2.3 Start Frontend Server
```bash
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view pratiraksha-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

✅ **Frontend is now running on `http://localhost:3000`**

---

## ✅ STEP 3: Access the Application

1. **Open Browser**: Go to `http://localhost:3000`
2. **Dashboard loads**: You should see:
   - Real-time threat detection statistics
   - Network analysis charts
   - Threat logs
   - Model status information

---

## 📊 Project Structure

```
PRATIRAKSHA/
├── backend/
│   ├── app.py                 ← Main Flask server
│   ├── utils.py               ← ML model utilities
│   ├── database.py            ← Database handlers
│   ├── models/
│   │   ├── trained_model.pth  ← Pre-trained PyTorch model
│   │   └── model_info.json    ← Model metadata
│   └── requirements.txt        ← Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.js             ← Main React component
│   │   ├── components/        ← React components
│   │   │   ├── Dashboard.js
│   │   │   ├── ModelStatus.js
│   │   │   ├── NetworkChart.js
│   │   │   ├── ThreatLog.js
│   │   │   └── ...
│   │   └── index.js           ← Entry point
│   ├── package.json           ← Node.js dependencies
│   └── public/
│       └── index.html         ← HTML template
│
├── data/
│   └── PRATIRAKSHA_ransomware_dataset.csv ← Training data
│
└── models/
    └── trained_model.pth      ← Global model copy
```

---

## 🔧 Common Issues & Solutions

### Issue 1: Backend won't start - ImportError
**Solution**: 
```bash
pip install --upgrade setuptools wheel
pip install torch scikit-learn pandas numpy
```

### Issue 2: Frontend npm packages fail
**Solution**:
```bash
cd frontend
npm cache clean --force
npm install
```

### Issue 3: Port 5000 or 3000 already in use
**Solution**:
- Stop the conflicting application
- Or modify port in `app.py` (line ~50): `app.run(port=5001)`

### Issue 4: CORS errors in browser console
**Solution**: Backend CORS is already configured in `app.py` line 19

---

## 📱 API Endpoints (Backend)

- `GET  /api/stats` - Get threat statistics
- `GET  /api/model-status` - Get model information
- `POST /api/detect` - Analyze network traffic
- `GET  /api/threats` - Get threat log
- WebSocket `/socket.io` - Real-time updates

---

## 🎯 Features

✅ Real-time ransomware threat detection  
✅ Machine Learning powered (Graph Convolutional Network)  
✅ Network behavior analysis  
✅ Interactive dashboard with charts  
✅ Threat logging & statistics  
✅ WebSocket for live updates  

---

## 📝 Notes

- The model (`trained_model.pth`) is pre-trained and ready to use
- Database is initialized on first run
- Logs are stored in `logs/` directory
- Threat data is persisted in SQLite database

