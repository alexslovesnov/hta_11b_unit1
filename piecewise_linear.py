import streamlit as st
import matplotlib.pyplot as plt

st.title("Separate Polyline Plotter (Two Columns)")

# Функция для парсинга точек
def parse_points(text):
    return [tuple(map(float, p.strip(" ()").split(",")))
            for p in text.split("),") if p.strip()]

# Создаём два столбца
col1, col2 = st.columns(2)

# ---- Левая колонка: Landscape ----
with col1:
    landscape_input = st.text_area(
        "Landscape (points in format (x, y), (x, y), ...)",
        "(0, 0), (1, 2), (2, 1), (3, 3)",
        key="landscape"
    )
    if st.button("Run Landscape"):
        try:
            points = parse_points(landscape_input)
            fig, ax = plt.subplots()
            x_vals, y_vals = zip(*points)
            ax.plot(x_vals, y_vals, marker="o")
            ax.set_title("Landscape Polyline")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error: {e}")

# ---- Правая колонка: Color ----
with col2:
    color_input = st.text_area(
        "Color (points in format (x, y), (x, y), ...)",
        "(0, 1), (1, 1.5), (2, 0.5), (3, 2.5)",
        key="color"
    )
    if st.button("Run Color"):
        try:
            points = parse_points(color_input)
            fig, ax = plt.subplots()
            x_vals, y_vals = zip(*points)
            ax.plot(x_vals, y_vals, marker="o", linestyle="--")
            ax.set_title("Color Polyline")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error: {e}")
