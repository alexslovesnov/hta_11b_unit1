import streamlit as st
import matplotlib.pyplot as plt
import re

st.title("Polyline Plotter")

# Поле для ввода точек
coords_text = st.text_input(
    "Enter coordinates like (1, 2), (3, 4), (5, 6):",
    "(0, 0), (1, 2), (3, 1), (4, 3)"
)

# Кнопка запуска
if st.button("Run"):
    try:
        # Находим все пары чисел в скобках
        matches = re.findall(r"\(\s*([-+]?\d*\.?\d+)\s*,\s*([-+]?\d*\.?\d+)\s*\)", coords_text)
        
        if not matches:
            st.error("No valid coordinates found. Please use format: (x, y), (x, y)")
        else:
            # Преобразуем в списки X и Y
            x_values = [float(x) for x, _ in matches]
            y_values = [float(y) for _, y in matches]
            
            # Строим график
            fig, ax = plt.subplots()
            ax.plot(x_values, y_values, marker="o")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
            ax.set_title("Polyline")
            ax.grid(True)
            
            st.pyplot(fig)
    except Exception as e:
        st.error(f"Error: {e}")
