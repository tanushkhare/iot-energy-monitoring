import streamlit as st
import requests

st.title("🚀 Project 20: GitOps CI/CD Pipeline Automation")
if st.button("Check Pipeline Status"):
    res = requests.get("http://127.0.0.1:8000/api/pipeline-status")
    if res.status_code == 200:
        data = res.json()
        st.success(f"Pipeline Run: {data['pipeline_id']}")
        st.metric("Build Status", data["build_status"])
        st.write(f"**Target Branch:** `{data['branch']}`")
        st.info(f"**Latest Commit:** {data['last_commit']}")