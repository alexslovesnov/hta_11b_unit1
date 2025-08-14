import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Separate Polyline Plotter (Two Columns + Combine)")

# --- Функция для парсинга точек ---
def parse_points(text):
    return [tuple(map(float, p.strip(" ()").split(",")))
            for p in text.split("),") if p.strip()]

# --- Инициализация session_state ---
if "landscape_fig" not in st.session_state:
    st.session_state.landscape_fig = None
if "color_fig" not in st.session_state:
    st.session_state.color_fig = None
if "landscape_points" not in st.session_state:
    st.session_state.landscape_points = None
if "color_points" not in st.session_state:
    st.session_state.color_points = None
if "combine_fig" not in st.session_state:
    st.session_state.combine_fig = None

# --- Две колонки ---
col1, col2 = st.columns(2)

# ====== Левая колонка: Landscape ======
with col1:
    landscape_input = st.text_area(
        "Landscape (points in format (x, y), (x, y), ...)",
        "(0, 0), (1, 2), (2, 1), (3, 3)",
        key="landscape"
    )

    if st.button("Run Landscape"):
        try:
            points = parse_points(landscape_input)
            st.session_state.landscape_points = points
            fig, ax = plt.subplots()
            x_vals, y_vals = zip(*points)
            ax.plot(x_vals, y_vals, marker="o")
            ax.set_title("Landscape Polyline")
            st.session_state.landscape_fig = fig
        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state.landscape_fig:
        st.pyplot(st.session_state.landscape_fig)

# ====== Правая колонка: Color ======
with col2:
    color_input = st.text_area(
        "Color (points in format (x, y), (x, y), ...)",
        "(0, 1), (1, 1.5), (2, 0.5), (3, 2.5)",
        key="color"
    )

    if st.button("Run Color"):
        try:
            points = parse_points(color_input)
            st.session_state.color_points = points
            fig, ax = plt.subplots()
            x_vals, y_vals = zip(*points)
            ax.plot(x_vals, y_vals, marker="o", linestyle="--")
            ax.set_title("Color Polyline")
            st.session_state.color_fig = fig
        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state.color_fig:
        st.pyplot(st.session_state.color_fig)

# ====== Кнопка Combine ======
st.markdown("---")
if st.button("Combine"):
    if st.session_state.landscape_points and st.session_state.color_points:
        try:
            # Берём точки Landscape
            x_vals, y_vals = zip(*st.session_state.landscape_points)

            # Берём значения Y из Color как интенсивность
            _, color_vals = zip(*st.session_state.color_points)
            color_vals = np.array(color_vals)

            # Нормируем интенсивности в диапазон [0, 1]
            norm_colors = (color_vals - color_vals.min()) / (color_vals.max() - color_vals.min())

            fig, ax = plt.subplots()
            for i in range(len(x_vals) - 1):
                ax.plot(x_vals[i:i+2], y_vals[i:i+2],
                        color=plt.cm.viridis(norm_colors[i]),
                        linewidth=2)

            ax.set_title("Landscape Colored by Color Intensity")
            st.session_state.combine_fig = fig
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Сначала постройте оба графика (Landscape и Color).")

if st.session_state.combine_fig:
    st.pyplot(st.session_state.combine_fig)
