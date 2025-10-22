import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp

st.title("📈 Вимушені коливання та Резонанс")
st.write("Модель осцилятора з затуханням та зовнішньою синусоїдальною силою.")
st.latex(r"m \ddot{x} + b \dot{x} + k x = F_0 \cos(\omega_d t)")

# --- Бічна панель ---
st.sidebar.header("Параметри осцилятора")
m = st.sidebar.slider("Маса (m), кг", 0.1, 10.0, 1.0, key="m_res")
k = st.sidebar.slider("Жорсткість пружини (k), Н/м", 0.1, 50.0, 10.0, key="k_res")
b = st.sidebar.slider("Коефіцієнт затухання (b)", 0.0, 5.0, 0.5, key="b_res")

st.sidebar.header("Зовнішня сила")
F0 = st.sidebar.slider("Амплітуда сили (F₀), Н", 0.0, 50.0, 10.0)
omega_d = st.sidebar.slider("Частота сили (ω_d), рад/с", 0.1, 10.0, 3.0, 0.1)

t_max = st.sidebar.slider("Час симуляції (T), с", 10.0, 200.0, 50.0)

# --- Розрахункова частина ---

# 1. Власна частота
omega0 = np.sqrt(k / m)
# 2. Резонансна частота (трохи зміщується через затухання)
omega_res = np.sqrt(omega0**2 - (b/(2*m))**2) if (b/(2*m)) < omega0 else 0

st.subheader("Ключові частоти системи")
col1, col2 = st.columns(2)
col1.metric("Власна частота (ω₀)", f"{omega0:.3f} рад/с")
col2.metric("Резонансна частота (ω_res)", f"{omega_res:.3f} рад/с", 
            help="Частота, на якій амплітуда буде максимальною. Трохи менша за ω₀ через затухання.")

if np.isclose(omega_d, omega_res, atol=0.1):
    st.success("Ви близько до резонансу! Амплітуда має бути великою.")

# --- Розв'язок ДР ---
# m*x'' + b*x' + k*x = F0*cos(w_d*t)
# y[0] = x
# y[1] = x' (швидкість)
# y[0]' = y[1]
# y[1]' = (F0*cos(w_d*t) - b*y[1] - k*y[0]) / m
def model(t, y):
    x, v = y
    dxdt = v
    dvdt = (F0 * np.cos(omega_d * t) - b * v - k * x) / m
    return [dxdt, dvdt]

# Початкові умови (зі стану спокою)
y0 = [0, 0]
t_span = [0, t_max]
t_eval = np.linspace(t_span[0], t_span[1], 1000)

sol = solve_ivp(model, t_span, y0, t_eval=t_eval)
x_values = sol.y[0]
t_values = sol.t

# --- Графік ---
st.header("Графік руху x(t)")
st.write("Спробуйте встановити 'Частоту сили' (ω_d) рівною 'Резонансній частоті' (ω_res).")

fig = go.Figure()
fig.add_trace(go.Scatter(x=t_values, y=x_values, mode='lines', name='Зміщення (x)'))
fig.update_layout(
    title="Залежність зміщення від часу x(t)",
    xaxis_title="Час (t), с",
    yaxis_title="Зміщення (x), м"
)

# Знаходимо "сталу" амплітуду (після перехідного процесу)
# Беремо останню третину симуляції
steady_state_amplitude = np.max(np.abs(x_values[int(len(x_values) * 2/3):]))
st.metric("Усталена амплітуда", f"{steady_state_amplitude:.3f} м")