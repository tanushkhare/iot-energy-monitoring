import streamlit as st

st.markdown("""
    <style>
        .stApp {
            background-color: #090d16;
            color: #f8fafc;
            font-family: 'Inter', sans-serif;
        }
        .sidebar .stSidebar {
            background-color: #0f172a;
            border-right: 1px solid #1e293b;
        }
        h1, h2, h3 {
            color: #f8fafc;
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        .stButton>button {
            background: linear-gradient(135deg, #38bdf8 0%, #0284c7 100%);
            color: #090d16;
            font-weight: 600;
            border: none;
            border-radius: 0.5rem;
            padding: 0.5rem 1rem;
        }
    </style>
""", unsafe_allow_html=True)

import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IoT Energy Monitoring", layout="wide")

st.title("⚡ Smart Grid Energy & Power Telemetry Hub")
st.markdown("Continuous IoT telemetry stream ingest, real-time power factor calculations, and over-voltage alarm processing.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Simulate Grid Sensor Ingest")
    meter_id = st.text_input("Smart Meter Node Identifier", value="GRID-NODE-101")
    voltage = st.slider("RMS Voltage (V)", 180.0, 270.0, 230.0, step=0.5)
    current = st.slider("Load Current (A)", 0.0, 60.0, 15.5, step=0.5)
    freq = st.slider("Grid AC Frequency (Hz)", 47.0, 53.0, 50.0, step=0.1)

    if st.button("Transmit Energy Telemetry Frame", type="primary"):
        payload = {
            "device_id": meter_id,
            "voltage_v": voltage,
            "current_a": current,
            "frequency_hz": freq
        }
        try:
            res = requests.post("http://localhost:8000/api/v1/energy/telemetry", json=payload, timeout=5)
            if res.status_code == 200:
                st.session_state["p20_res"] = res.json()
                st.success("Telemetry Frame Ingested!")
            else:
                st.error(f"Error: {res.text}")
        except Exception:
            st.warning("Backend offline. Simulating local power factor calculation.")
            apparent = (voltage * current) / 1000.0
            is_anomaly = voltage > 250.0 or voltage < 205.0
            st.session_state["p20_res"] = {
                "device_id": meter_id,
                "voltage_v": voltage,
                "current_a": current,
                "active_power_kw": round(apparent * 0.92, 3),
                "power_factor": 0.92,
                "grid_status": "SURGE_OVERVOLTAGE_ALARM" if voltage > 250 else ("BROWNOUT_UNDERVOLTAGE_ALARM" if voltage < 205 else "GRID_STABLE_NOMINAL"),
                "anomaly_detected": is_anomaly,
                "timestamp": "2026-08-28T10:00:00Z"
            }

with col2:
    if "p20_res" in st.session_state:
        r = st.session_state["p20_res"]
        st.subheader(f"Telemetry Status: {r['device_id']}")
        m1, m2, m3 = st.columns(3)
        m1.metric("Active Power", f"{r['active_power_kw']} kW")
        m2.metric("Power Factor", f"{r['power_factor']}")
        m3.metric("Grid Status", r["grid_status"], delta="ANOMALY" if r["anomaly_detected"] else "HEALTHY")

        if r["anomaly_detected"]:
            st.error(f"⚠️ GRID ALARM TRIGGERED: **{r['grid_status']}**")
        else:
            st.success("✅ Power Grid Phase & Voltage in Nominal Distribution")

