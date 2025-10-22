import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("💡 Симулятор досліду Франка-Герца")
st.write("""
Демонструє, як струм (I) в трубці, наповненій парами ртуті, 
залежить від прискорюючої напруги (V).
Різкі падіння струму відбуваються, коли електрони досягають енергії, 
достатньої для непружного зіткнення з атомами ртуті (4.9 еВ).
""")

# --- Параметри ---
st.sidebar.header("Параметри симуляції")
V_ex_eV = st.sidebar.number_input(
    "Енергія збудження (E_ex), еВ", 
    min_value=1.0, max_value=10.0, value=4.9, step=0.1,
    help="Для ртуті (Hg) це 4.9 еВ. Для неону (Ne) - близько 18.7 еВ."
)

V_max = st.sidebar.slider(
    "Максимальна напруга (V_max), Вольт", 
    min_value=10.0, max_value=50.0, value=30.0, step=1.0
)

# --- Розрахункова модель ---
# Створюємо 500 точок напруги
V = np.linspace(0.01, V_max, 500)

# Спрощена модель струму.
# Це не є суворим фізичним розв'язком, а візуальною моделлю,
# що демонструє ефект.

# 1. Базовий струм, що повільно росте (як у вакуумній лампі)
I_base = V**0.1

# 2. "Коливання" струму, пов'язані з непружними зіткненнями.
# V % V_ex дає нам "залишкову" напругу після останнього зіткнення.
# Коли V = V_ex, 4.9 % 4.9 = 0 -> струм падає.
# Коли V = 4.8, 4.8 % 4.9 = 4.8 -> струм високий.
I_oscillation = (V % V_ex_eV)**1.5

# Сумарний струм (з коефіцієнтами для гарного вигляду)
I = I_base + I_oscillation / (V_ex_eV) # Нормуємо

# --- Графік ---
st.header("Графік залежності струму від напруги I(V)")
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=V, y=I, 
    mode='lines',
    name='Струм (I)',
    line=dict(color='royalblue', width=3)
))

# Додаємо вертикальні лінії, де очікуються піки
peak_voltages = np.arange(V_ex_eV, V_max + V_ex_eV, V_ex_eV)
for v_peak in peak_voltages:
    fig.add_vline(
        x=v_peak, 
        line_width=2, 
        line_dash="dash", 
        line_color="red",
        annotation_text=f"n={int(v_peak/V_ex_eV)} ({v_peak:.1f} V)",
        annotation_position="top left"
    )

fig.update_layout(
    title="Вольт-амперна характеристика (ВАХ)",
    xaxis_title="Прискорююча напруга (V), Вольт",
    yaxis_title="Струм (I), умовні одиниці",
    height=500
)
st.plotly_chart(fig, use_container_width=True)
st.info(f"Зверніть увагу, як струм різко падає **одразу після** кожної червоної лінії (кратних {V_ex_eV} В), де відбуваються масові непружні зіткнення.")