import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import time

st.title("Landscape + Color Animation")

def parse_points(text):
    return [tuple(map(float, p.strip(" ()").split(",")))
            for p in text.split("),") if p.strip()]

# Сохраняем данные между нажатиями
if "landscape_points" not in st.session_state:
    st.session_state.landscape_points = None
if "color_points" not in st.session_state:
    st.session_state.color_points = None

# --- Ввод ---
col1, col2 = st.columns(2)

with col1:
    landscape_input = st.text_area(
        "Landscape (points: (x, y), ...)",
        "(0, 0), (1, 2), (2, 1), (3, 3)",
        key="landscape"
    )
    if st.button("Run Landscape"):
        st.session_state.landscape_points = parse_points(landscape_input)
        st.success("Landscape points saved.")

with col2:
    color_input = st.text_area(
        "Color (time, intensity):",
        "(0, 0.1), (1, 0.5), (2, 0.8), (3, 1.0)",
        key="color"
    )
    if st.button("Run Color"):
        st.session_state.color_points = parse_points(color_input)
        st.success("Color points saved.")

# --- Отображение графиков ---
col1, col2 = st.columns(2)

with col1:
    if st.session_state.landscape_points:
        fig1, ax1 = plt.subplots()
        lp = np.array(st.session_state.landscape_points)
        ax1.plot(lp[:, 0], lp[:, 1], marker="o", color="blue")
        ax1.set_title("Landscape")
        st.pyplot(fig1)

with col2:
    if st.session_state.color_points:
        fig2, ax2 = plt.subplots()
        cp = np.array(st.session_state.color_points)
        ax2.plot(cp[:, 0], cp[:, 1], marker="o", color="black")
        ax2.set_title("Color Intensity")
        ax2.set_xlabel("Time (s)")
        ax2.set_ylabel("Intensity (0=white, 1=black)")
        ax2.set_ylim(0, 1)
        st.pyplot(fig2)

# --- Combine Animation ---
if st.button("Combine Animation"):
    if st.session_state.landscape_points and st.session_state.color_points:
        landscape = np.array(st.session_state.landscape_points)
        color_data = np.array(st.session_state.color_points)

        x_land, y_land = landscape[:, 0], landscape[:, 1]
        t_color, intensity = color_data[:, 0], color_data[:, 1]

        # нормируем интенсивность
        norm_intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min())

        placeholder = st.empty()  # третье окно

        for i in range(len(t_color)):
            fig3, ax3 = plt.subplots()
            gray_shade = str(1 - norm_intensity[i])  # 1=white, 0=black
            ax3.plot(x_land, y_land, marker="o", color=gray_shade, linewidth=2)
            ax3.set_title(f"Landscape at t={t_color[i]:.1f}s")
            ax3.set_xlabel("X")
            ax3.set_ylabel("Y")
            placeholder.pyplot(fig3)
            time.sleep(0.2)
    else:
        st.warning("Сначала заполните и запустите Landscape и Color.")
