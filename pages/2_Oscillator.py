import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp # Нам потрібен розв'язувач диференціальних рівнянь

st.title("🌀 Симулятор гармонічного осцилятора")
st.write("Моделює рух пружинного маятника з можливим затуханням.")

# --- Бічна панель ---
st.sidebar.header("Параметри осцилятора")

m = st.sidebar.slider("Маса (m), кг", 0.1, 10.0, 1.0)
k = st.sidebar.slider("Жорсткість пружини (k), Н/м", 0.1, 50.0, 10.0)
b = st.sidebar.slider("Коефіцієнт затухання (b)", 0.0, 5.0, 0.5, 
                    help="b=0: немає затухання. b > 0: коливання затухають.")

st.sidebar.header("Початкові умови")
x0 = st.sidebar.slider("Початкове зміщення (x₀), м", -5.0, 5.0, 2.0)
v0 = st.sidebar.slider("Початкова швидкість (v₀), м/с", -5.0, 5.0, 0.0)

t_max = st.sidebar.slider("Час симуляції (T), с", 5.0, 100.0, 20.0)

# --- Розрахункова частина ---

# Диференціальне рівняння: m*x'' + b*x' + k*x = 0
# Перепишемо як систему:
# y[0] = x
# y[1] = x' (швидкість)
#
# y[0]' = y[1]
# y[1]' = (-b*y[1] - k*y[0]) / m

def model(t, y):
    x, v = y
    dxdt = v
    dvdt = (-b * v - k * x) / m
    return [dxdt, dvdt]

# Початкові умови
y0 = [x0, v0]

# Часові точки
t_span = [0, t_max]
t_eval = np.linspace(t_span[0], t_span[1], 500) # 500 точок для графіка

# Розв'язуємо ДР
sol = solve_ivp(model, t_span, y0, t_eval=t_eval)

x_values = sol.y[0]
v_values = sol.y[1]
t_values = sol.t

# --- Відображення результатів ---

# Розрахунок параметрів для відображення
omega0 = np.sqrt(k / m) # Власна частота
st.metric("Власна частота (ω₀)", f"{omega0:.2f} рад/с")

# --- Графіки ---
st.header("Графіки руху")

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=t_values, y=x_values, mode='lines', name='Зміщення (x)'))
fig1.update_layout(
    title="Залежність зміщення від часу x(t)",
    xaxis_title="Час (t), с",
    yaxis_title="Зміщення (x), м"
)
st.plotly_chart(fig1, use_container_width=True)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=x_values, y=v_values, mode='lines', name='Фазова траєкторія'))
fig2.update_layout(
    title="Фазовий портрет (v(x))",
    xaxis_title="Зміщення (x), м",
    yaxis_title="Швидкість (v), м/с"
)
fig2.update_yaxes(scaleanchor="x", scaleratio=1)
st.plotly_chart(fig2, use_container_width=True)