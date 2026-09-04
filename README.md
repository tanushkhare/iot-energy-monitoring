# ⚡ IoT Energy & Smart Grid Monitoring

[![Live Web Demo](https://img.shields.io/badge/Live_App-Vercel-black?style=for-the-badge&logo=vercel)](https://iot-energy-monitoring.vercel.app)
[![Portfolio Hub](https://img.shields.io/badge/Portfolio_Hub-Live-blue?style=for-the-badge)](https://portfolio-showcase-hub-web11.vercel.app)

🔗 **Production URL:** [https://iot-energy-monitoring.vercel.app](https://iot-energy-monitoring.vercel.app)  
🌐 **Showcase Hub:** [https://portfolio-showcase-hub-web11.vercel.app](https://portfolio-showcase-hub-web11.vercel.app)

---

## 📌 Architectural Overview
Smart-grid telemetry aggregator monitoring voltage sag, current draw, power factor efficiency, and operational tariffs from MQTT edge streams.

---

## 🛠️ Technology Ecosystem
* **Core Architecture:** FastAPI, MQTT Broker, Pandas, SQLite
* **Testing & Quality:** PyTest, Automated GitHub Actions CI
* **Deployment:** Vercel Edge Runtime

---

## 🛡️ Production Standards
* **Purged Misfiled Code:** Removed misplaced GitOps and summarizer code.
* **Threshold Alerting:** Real-time voltage surge and sag detection (210V - 245V nominal range).
* **Cost Rate Calculation:** Maps active kilowatt usage directly to hourly tariff expenses.

---

## 🚀 API Contracts
```http
POST /api/v1/energy/telemetry
Request:
{
  "voltage": 230.5,
  "current": 14.2,
  "power_factor": 0.95
}

Response (200 OK):
{
  "active_power_kw": 3.109,
  "grid_status": "OPTIMAL",
  "anomaly": false,
  "cost_per_hour_usd": 0.42
}

GET /health
Response: {"status": "healthy"}

💻 Local Quickstart
B
ash

pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
pytest tests/ -v