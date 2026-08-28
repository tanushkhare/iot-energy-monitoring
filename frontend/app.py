import streamlit as st
import requests
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="IoT Energy Monitoring", layout="wide")

st.title("⚡ Smart Factory & IoT Grid Energy Telemetry")
st.markdown("Real-time power quality ingestion, load curve analytics, and electrical grid anomaly detection.")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Smart Meter Ingest Console")
    device_id = st.text_input("Meter Node ID", value="GRID-NODE-402")
    voltage = st.slider("RMS Voltage (V)", 180.0, 280.0, 230.5, step=0.5)
    current = st.slider("Load Current (A)", 0.0, 60.0, 14.8, step=0.2)
    freq = st.number_input("Grid Frequency (Hz)", value=50.0, step=0.1)

    if st.button("Transmit Ingestion Packet", type="primary"):
        with st.spinner("Computing active power and evaluating harmonics..."):
            try:
                res = requests.post(
                    "http://localhost:8000/api/v1/iot/telemetry",
                    json={"device_id": device_id, "voltage_v": voltage, "current_a": current, "frequency_hz": freq},
                    timeout=5
                )
                if res.status_code == 200:
                    st.session_state["p20_result"] = res.json()
                    st.success("Telemetry Logged!")
                else:
                    st.error(f"Ingest Error: {res.text}")
            except Exception:
                st.warning("Backend offline. Running client-side simulation.")
                is_anomaly = voltage > 250.0 or voltage < 205.0 or current > 45.0
                st.session_state["p20_result"] = {
                    "device_id": device_id,
                    "voltage_v": voltage,
                    "current_a": current,
                    "active_power_kw": round((voltage * current * 0.92) / 1000.0, 3),
                    "power_factor": 0.92,
                    "grid_status": "SURGE_OVERVOLTAGE_ALARM" if voltage > 250.0 else "GRID_STABLE_NOMINAL",
                    "anomaly_detected": is_anomaly,
                    "timestamp": "2026-08-28T08:30:00Z"
                }

with col2:
    if "p20_result" in st.session_state:
        res = st.session_state["p20_result"]
        st.subheader(f"Grid Status: {res['device_id']}")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Active Power", f"{res['active_power_kw']} kW")
        m2.metric("Power Factor", f"{res['power_factor']}")
        m3.metric("Grid Status", "ALARM" if res["anomaly_detected"] else "NOMINAL", delta=res["grid_status"])
        
        if res["anomaly_detected"]:
            st.error(f"⚠️ Anomaly Alarm: {res['grid_status']}")
        else:
            st.success("✅ Power quality within acceptable grid tolerances.")
            
        # Gauge chart for voltage
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=res["voltage_v"],
            title={'text': "RMS Voltage (V)"},
            gauge={
                'axis': {'range': [180, 280]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [180, 205], 'color': "lightcoral"},
                    {'range': [205, 250], 'color': "lightgreen"},
                    {'range': [250, 280], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 250
                }
            }
        ))
        st.plotly_chart(fig, use_container_width=True)
