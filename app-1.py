import streamlit as st
from streamlit_js_eval import get_geolocation
from datetime import datetime
import os

st.set_page_config(page_title="Photo & Location Capture", page_icon="📍")
st.title("📸 Capture Photo & Live Location")
st.markdown(
    "This app grabs a photo from your camera and your current GPS location. "
    "Your browser will ask for camera and location permissions — allow both."
)

# ---------------- Location ----------------
st.subheader("📍 Your Location")
location = get_geolocation()

lat = lon = accuracy = None
if location and "coords" in location:
    lat = location["coords"]["latitude"]
    lon = location["coords"]["longitude"]
    accuracy = location["coords"]["accuracy"]
    st.success(f"Location: {lat:.6f}, {lon:.6f}  (±{accuracy:.0f} m)")
    st.map(data={"lat": [lat], "lon": [lon]})
else:
    st.info("Waiting for location permission… allow access in the browser prompt.")

# ---------------- Photo ----------------
st.subheader("📷 Capture Photo")
photo = st.camera_input("Take a photo")

if photo is not None:
    st.image(photo, caption="Captured photo")

# ---------------- Save ----------------
st.subheader("💾 Save")
if st.button("Save photo + location"):
    if photo is None:
        st.error("Please take a photo first.")
    elif lat is None:
        st.error("Location not available yet — allow location access and wait a moment, then try again.")
    else:
        os.makedirs("captures", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_path = f"captures/photo_{timestamp}.jpg"
        with open(img_path, "wb") as f:
            f.write(photo.getbuffer())

        log_path = "captures/log.csv"
        write_header = not os.path.exists(log_path)
        with open(log_path, "a") as f:
            if write_header:
                f.write("timestamp,latitude,longitude,accuracy_m,image_path\n")
            f.write(f"{timestamp},{lat},{lon},{accuracy},{img_path}\n")

        st.success(f"Saved: {img_path} (logged in {log_path})")
