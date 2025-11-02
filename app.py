import os
import pandas as pd
import streamlit as st
from PIL import Image
import io
import datetime

# Import your modules
from modules.cleanscan import remove_sensitive_content
from modules.safeshare import generate_safe_preview
from modules.noiseguard import add_privacy_noise

st.set_page_config(page_title="ImageShield", layout="wide")
st.title("🛡️ ImageShield: Cyber Hygiene Toolkit")

# Sidebar controls
st.sidebar.markdown("### 🧭 Choose a Module")
if "selected_module" not in st.session_state:
    st.session_state["selected_module"] = None

if st.sidebar.button("🔍 CleanScan"):
    st.session_state["selected_module"] = "CleanScan"
if st.sidebar.button("🔐 SafeShare"):
    st.session_state["selected_module"] = "SafeShare"
if st.sidebar.button("🧊 NoiseGuard"):
    st.session_state["selected_module"] = "NoiseGuard"

st.sidebar.header("🧹 History Controls")
if st.sidebar.button("Clear History"):
    if os.path.exists("log.txt"):
        os.remove("log.txt")
    for key in ["cleanscan_run", "safeshare_run", "noiseguard_run"]:
        st.session_state[key] = False
    st.sidebar.success("History cleared.")

st.sidebar.header("🛠️ Settings")
uploaded_file = st.sidebar.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Logging functions
def log_event(event_type, details):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.markdown(f"📝 **{event_type}** at `{timestamp}`")
    st.sidebar.code(details)

def log_to_file(module, details):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as f:
        f.write(f"[{timestamp}] {module}: {details}\n")

# Main display
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Original Image", use_column_width=True)

    module = st.session_state.get("selected_module")
    if module == "CleanScan":
        st.subheader("🔍 CleanScan: Face Blurring")
        if st.button("Run CleanScan"):
            blurred = remove_sensitive_content(image)
            st.image(blurred, caption="CleanScan Output")
            buf = io.BytesIO()
            blurred.save(buf, format="PNG")
            st.download_button("Download Blurred Image", buf.getvalue(), "cleanscan.png", "image/png")
            log_event("CleanScan Run", "Face blurring applied")
            log_to_file("CleanScan", "Face blurring applied")
            st.session_state["cleanscan_run"] = True
            st.session_state["cleanscan_details"] = "Face blurring applied"

    elif module == "SafeShare":
        st.subheader("🔐 SafeShare: Metadata & Watermark")

        watermark_text = st.text_input("Watermark Text", value="SAFE SHARE")
        opacity = st.slider("Watermark Opacity", 50, 255, 100)
        angle = st.slider("Watermark Angle", 0, 90, 45)
        position = st.selectbox("Watermark Position", ["Bottom-Right", "Bottom-Left", "Top-Right", "Top-Left"])

        if st.button("Run SafeShare"):
            preview = generate_safe_preview(image, text=watermark_text, opacity=opacity, angle=angle,position=position)
            st.image(preview, caption="SafeShare Preview")
            buf = io.BytesIO()
            preview.save(buf, format="PNG")
            st.download_button("Download Safe Image", buf.getvalue(), "safeshare.png", "image/png")
            log_event("SafeShare Run", f"Watermark: '{watermark_text}', Opacity: {opacity}, Angle: {angle}")
            log_to_file("SafeShare", f"Watermark: '{watermark_text}', Opacity: {opacity}, Angle: {angle}")
            st.session_state["safeshare_run"] = True
            st.session_state["safeshare_text"] = watermark_text
            st.session_state["safeshare_opacity"] = opacity
            st.session_state["safeshare_angle"] = angle

    elif module == "NoiseGuard":
        st.subheader("🧊 NoiseGuard: Privacy Filters")

        mode = st.selectbox("Privacy Mode", ["pixelate", "noise", "blur"])
        intensity = st.slider("Intensity", 5, 50, 10)

        if st.button("Run NoiseGuard"):
            noisy = add_privacy_noise(image, mode=mode, intensity=intensity)
            st.image(noisy, caption=f"NoiseGuard Output ({mode})")
            buf = io.BytesIO()
            noisy.save(buf, format="PNG")
            st.download_button("Download Privacy-Protected Image", buf.getvalue(), f"noiseguard_{mode}.png", "image/png")
            log_event("NoiseGuard Run", f"Mode: {mode}, Intensity: {intensity}")
            log_to_file("NoiseGuard", f"Mode: {mode}, Intensity: {intensity}")
            st.session_state["noiseguard_run"] = True
            st.session_state["noiseguard_mode"] = mode
            st.session_state["noiseguard_intensity"] = intensity

    # 📊 Summary Panel
    st.divider()
    st.subheader("📊 Summary Panel")

    summary = []
    if st.session_state.get("cleanscan_run"):
        summary.append(f"✅ CleanScan: {st.session_state.get('cleanscan_details')}")
    if st.session_state.get("safeshare_run"):
        summary.append(
            f"✅ SafeShare: Watermark '{st.session_state.get('safeshare_text')}' "
            f"with opacity {st.session_state.get('safeshare_opacity')} and angle {st.session_state.get('safeshare_angle')}"
        )
    if st.session_state.get("noiseguard_run"):
        summary.append(
            f"✅ NoiseGuard: Mode '{st.session_state.get('noiseguard_mode')}' "
            f"with intensity {st.session_state.get('noiseguard_intensity')}"
        )

    if summary:
        for item in summary:
            st.markdown(item)
    else:
        st.info("No protections applied yet.")

    # 📄 Log Report Viewer + Download
    if os.path.exists("log.txt"):
        with open("log.txt", "rb") as f:
            st.download_button(
                label="📥 Download Log Report",
                data=f.read(),
                file_name="ImageShield_Log.txt",
                mime="text/plain"
            )

        with open("log.txt", "r") as f:
            lines = f.readlines()

        log_data = []
        for line in lines:
            if "]" in line and ":" in line:
                timestamp = line.split("]")[0][1:].strip()
                module = line.split("]")[1].split(":")[0].strip()
                details = line.split(":", 1)[1].strip()
                log_data.append({"Timestamp": timestamp, "Module": module, "Details": details})

        if log_data:
            st.markdown("### 📘 Log History")
            df = pd.DataFrame(log_data)
            st.dataframe(df, use_container_width=True)