import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

st.title("Landscape + Color Animation")

def parse_points(text):
    return [tuple(map(float, p.strip(" ()").split(",")))
            for p in text.split("),") if p.strip()]

# Session state
if "landscape_points" not in st.session_state:
    st.session_state.landscape_points = None
if "color_points" not in st.session_state:
    st.session_state.color_points = None

# --- Input fields ---
landscape_input = st.text_area(
    "Landscape (points: (x, y), ...)",
    "(0, 0), (1, 2), (2, 1), (3, 3)",
    key="landscape"
)

color_input = st.text_area(
    "Color (time, intensity):",
    "(0, 0.1), (1, 0.5), (2, 0.8), (3, 1.0)",
    key="color"
)

# --- Buttons ---
if st.button("Run Landscape"):
    st.session_state.landscape_points = parse_points(landscape_input)
    st.success("Landscape points saved.")

if st.button("Run Color"):
    st.session_state.color_points = parse_points(color_input)
    st.success("Color points saved.")

# --- Combine with animation ---
if st.button("Combine Animation"):
    if st.session_state.landscape_points and st.session_state.color_points:
        landscape = np.array(st.session_state.landscape_points)
        color_data = np.array(st.session_state.color_points)

        x_land, y_land = landscape[:, 0], landscape[:, 1]
        t_color, intensity = color_data[:, 0], color_data[:, 1]

        # Normalize intensity between 0 and 1
        norm_intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min())

        # Animation placeholder
        placeholder = st.empty()

        for i in range(len(t_color)):
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 6))

            # --- Upper plot: Color chart ---
            ax1.plot(t_color, norm_intensity, marker="o", color="black")
            ax1.set_title("Color Intensity over Time")
            ax1.set_xlabel("Time (s)")
            ax1.set_ylabel("Intensity (0=white, 1=black)")
            ax1.set_ylim(0, 1)

            # Highlight current time step
            ax1.scatter(t_color[i], norm_intensity[i], color="red", zorder=5)

            # --- Lower plot: Landscape colored ---
            color_val = norm_intensity[i]
            gray_shade = str(1 - color_val)  # 1=white, 0=black
            ax2.plot(x_land, y_land, marker="o", color=gray_shade, linewidth=2)
            ax2.set_title(f"Landscape at t={t_color[i]:.1f}s")
            ax2.set_xlabel("X")
            ax2.set_ylabel("Y")

            placeholder.pyplot(fig)
            time.sleep(0.5)

    else:
        st.warning("Сначала введите точки для Landscape и Color и нажмите их кнопки.")
