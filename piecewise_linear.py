import streamlit as st
import matplotlib.pyplot as plt

st.title("Separate Polyline Plotter")

# Хранилище точек между нажатиями кнопок
if "landscape_points" not in st.session_state:
    st.session_state.landscape_points = []
if "color_points" not in st.session_state:
    st.session_state.color_points = []

# Функция для парсинга точек
def parse_points(text):
    return [tuple(map(float, p.strip(" ()").split(",")))
            for p in text.split("),") if p.strip()]

# ---- Поле для Landscape ----
landscape_input = st.text_area(
    "Landscape (points in format (x, y), (x, y), ...)",
    "(0, 0), (1, 2), (2, 1), (3, 3)"
)
if st.button("Run Landscape"):
    try:
        st.session_state.landscape_points = parse_points(landscape_input)
    except Exception as e:
        st.error(f"Error: {e}")

# ---- Поле для Color ----
color_input = st.text_area(
    "Color (points in format (x, y), (x, y), ...)",
    "(0, 1), (1, 1.5), (2, 0.5), (3, 2.5)"
)
if st.button("Run Color"):
    try:
        st.session_state.color_points = parse_points(color_input)
    except Exception as e:
        st.error(f"Error: {e}")

# ---- Построение графика, если есть данные ----
if st.session_state.landscape_points or st.session_state.color_points:
    fig, ax = plt.subplots()

    if st.session_state.landscape_points:
        x_vals, y_vals = zip(*st.session_state.landscape_points)
        ax.plot(x_vals, y_vals, marker="o", label="Landscape")

    if st.session_state.color_points:
        x_vals_c, y_vals_c = zip(*st.session_state.color_points)
        ax.plot(x_vals_c, y_vals_c, marker="o", label="Color", linestyle="--")

    ax.set_title("Polyline Plot")
    ax.legend()
    st.pyplot(fig)
