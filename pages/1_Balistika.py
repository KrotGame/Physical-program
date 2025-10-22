import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Заголовок та опис програми ---
st.set_page_config(layout="wide") # Робимо сторінку ширшою
st.title("🚀 Інтерактивний симулятор балістики")
st.write("Дозволяє змоделювати траєкторію тіла, кинутого під кутом до горизонту. Змінюйте параметри на бічній панелі!")

# --- Бічна панель (сайдбар) для вводу даних ---
st.sidebar.header("Параметри запуску")

# Створюємо слайдери для зміни параметрів
v0 = st.sidebar.slider(
    "Початкова швидкість (v₀), м/с", 
    min_value=1.0, 
    max_value=100.0, 
    value=50.0, 
    step=1.0
)

angle_degrees = st.sidebar.slider(
    "Кут кидка (α), градуси", 
    min_value=0.0, 
    max_value=90.0, 
    value=45.0, 
    step=1.0
)

h0 = st.sidebar.slider(
    "Початкова висота (h₀), м", 
    min_value=0.0, 
    max_value=50.0, 
    value=0.0, 
    step=1.0
)

# Гравітаційна стала
g = 9.81

# --- Розрахункова частина ---

# Переводимо кут в радіани
angle_rad = np.deg2rad(angle_degrees)

# Розрахунок часу польоту (розв'язуємо квадратне рівняння y(t) = 0)
# y(t) = h0 + v0*sin(a)*t - g*t^2 / 2
# a*t^2 + b*t + c = 0, де a = -g/2, b = v0*sin(a), c = h0
a = -g / 2
b = v0 * np.sin(angle_rad)
c = h0
discriminant = b**2 - 4*a*c
t_flight = (-b - np.sqrt(discriminant)) / (2 * a) # Беремо додатний корінь

# Розрахунок максимальної дальності
x_max = v0 * np.cos(angle_rad) * t_flight

# Розрахунок максимальної висоти
t_peak = v0 * np.sin(angle_rad) / g
y_max = h0 + v0 * np.sin(angle_rad) * t_peak - g * t_peak**2 / 2

# --- Відображення розрахункових даних ---
st.header("Результати симуляції")
col1, col2, col3 = st.columns(3) # Розділяємо на 3 колонки
col1.metric("Макс. дальність (L)", f"{x_max:.2f} м")
col2.metric("Макс. висота (H)", f"{y_max:.2f} м")
col3.metric("Час польоту (T)", f"{t_flight:.2f} с")

# --- Графік траєкторії (з Plotly) ---
st.header("Графік траєкторії")

# Генеруємо 100 точок для плавної кривої
t_values = np.linspace(0, t_flight, 100)
x_values = v0 * np.cos(angle_rad) * t_values
y_values = h0 + v0 * np.sin(angle_rad) * t_values - (g * t_values**2) / 2

# Створюємо інтерактивний графік Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x_values, 
    y=y_values, 
    mode='lines', 
    name='Траєкторія',
    line=dict(color='royalblue', width=4)
))

# Додаємо точку старту і фінішу
fig.add_trace(go.Scatter(
    x=[0, x_max], 
    y=[h0, 0], 
    mode='markers', 
    name='Старт/Фініш',
    marker=dict(color='red', size=10)
))

# Налаштовуємо вигляд графіка
fig.update_layout(
    xaxis_title="Дальність (x), м",
    yaxis_title="Висота (y), м",
    xaxis=dict(range=[0, x_max * 1.1]), # Даємо трохи місця
    yaxis=dict(range=[0, y_max * 1.1]),
    title="Траєкторія польоту",
    height=500 # Висота графіка
)

# ВАЖЛИВО: робимо осі рівномасштабними
fig.update_yaxes(scaleanchor="x", scaleratio=1)

# Відображаємо графік у Streamlit
st.plotly_chart(fig, use_container_width=True)
