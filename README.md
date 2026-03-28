# Pulse — Mumbai Train Delay Predictor

Pulse predicts minute-level delays for the Mumbai suburban train network using a lightweight machine learning model and exposes predictions via a simple API and a mobile app.

**Key features**
- Predicts delay (minutes) per station/time using a trained Random Forest model.
- Lightweight training pipeline in Python (scikit-learn).
- Mobile client (React Native) for commuters.

**Tech stack**
- Backend / ML: Python, scikit-learn
- Mobile: React Native
- Packaging: `requirements.txt`

**Repository layout**
- [ai-engine/train.py](ai-engine/train.py) — training script and model save
- [ai-engine/main.py](ai-engine/main.py) — API / inference entrypoint
- [mobile-app/App.js](mobile-app/App.js) — mobile app entry
- [requirements.txt](requirements.txt) — Python dependencies

**Quick start (development)**
1. Install Python deps:

```bash
pip install -r requirements.txt
```

2. Train the model (saves to `models/mumbai_model.pkl`):

```bash
python ai-engine/train.py
# or, if you use the root helper script:
python train_model.py
```

3. Run the API (if available in `ai-engine/main.py`):

```bash
uvicorn ai-engine.main:app --reload
```

4. Run the mobile app:

```bash
cd mobile-app
npm install
npm start
```

**Notes**
- Model file: `models/mumbai_model.pkl`.
- If `joblib` is not installed, the training script will fall back to `pickle` but installing dependencies is recommended for best compatibility.



