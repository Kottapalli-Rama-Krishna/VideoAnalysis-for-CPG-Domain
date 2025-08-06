# app.py

import streamlit as st
import tempfile
import os
from video_utils import extract_keyframes, describe_frame
from prompts import build_planogram_prompt
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(page_title="📦 Shelf Compliance Auditor", layout="wide")
st.title("📊 Pawdrift Pet Product Planogram Compliance Checker")

uploaded_video = st.file_uploader("📤 Upload a shelf video (MP4 format)", type=["mp4"])

if uploaded_video:
    st.video(uploaded_video)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
        temp_video.write(uploaded_video.read())
        video_path = temp_video.name

    st.info("🔍 Extracting frames...")
    frames = extract_keyframes(video_path, timestamp_sec=5)

    if not frames:
        st.error("⚠️ No frames could be extracted from the video.")
    else:
        st.success(f"✅ Key frame extracted. Generating compliance report...")

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-pro",
            google_api_key=st.secrets["GOOGLE_API_KEY"],  # ✅ secure key usage
            temperature=0.3,
        )

        with st.spinner("🧠 Analyzing the key frame..."):
            frame_description = describe_frame(frames[0])
            prompt = build_planogram_prompt(frame_description)
            response = llm.invoke(prompt)
            full_report = response.content

        st.markdown("## 📝 Final Compliance Report")
        st.text_area("Full Report", full_report, height=500)
