import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.integrate import solve_ivp
import scipy.constants as const

st.title("🎯 Симулятор Резерфордівського розсіяння")
st.write("Моделює траєкторію α-частинки, що налітає на важке ядро.")
st.latex(r"F(r) = \frac{1}{4\pi\epsilon_0} \frac{(Z_1 e)(Z_2 e)}{r^2}")

# --- Бічна панель ---
st.sidebar.header("Параметри")
E_MeV = st.sidebar.slider("Енергія α-частинки (E), МеВ", 1.0, 10.0, 5.0, 0.1)
Z1 = 2 # Заряд α-частинки
Z2 = st.sidebar.slider("Заряд ядра мішені (Z₂)", 10, 100, 79, 1, 
                       help="79 - Золото (Au)")

# 'b' - прицільний параметр
b_fm = st.sidebar.slider("Прицільний параметр (b), фм", 0.0, 100.0, 10.0, 1.0,
                         help="фм = 10⁻¹⁵ м. b=0 - лобове зіткнення.")

# --- Константи та переведення в СІ ---
E = E_MeV * 1e6 * const.electron_volt # Енергія в Джоулях
b = b_fm * 1e-15 # Прицільний параметр в метрах
m = 4 * const.proton_mass # Маса α-частинки (приблизно)
k_e = 1 / (4 * np.pi * const.epsilon_0) # Кулонівська стала
ZeZ = (Z1 * const.e) * (Z2 * const.e) # Добуток зарядів

# Початкова швидкість v₀ (з E = mv²/2)
v0 = np.sqrt(2 * E / m)

# --- Розрахункова частина (Розв'язок ДР) ---

# Система координат: ядро в (0,0)
# Початкове положення частинки: (-x_start, b)
# Початкова швидкість: (v0, 0)
x_start = 20 * b if b > 1e-15 else 2e-13 # Починаємо "здалеку"

# y[0] = x (позиція x)
# y[1] = y (позиція y)
# y[2] = vx (швидкість по x)
# y[3] = vy (швидкість по y)
def model(t, y):
    x, y_pos, vx, vy = y
    r = np.sqrt(x**2 + y_pos**2)
    
    # Кулонівська сила F = k_e * ZeZ / r²
    # F_vec = F * (r_vec / r) = (F/r) * r_vec
    F_over_r = k_e * ZeZ / (r**3)
    
    # Fx = (F/r) * x, Fy = (F/r) * y
    # ax = Fx / m, ay = Fy / m
    ax = F_over_r * x / m
    ay = F_over_r * y_pos / m
    
    return [vx, vy, ax, ay]

# Початкові умови
y0 = [-x_start, b, v0, 0]
# Час симуляції (поки не пролетить повз)
t_span = [0, 2 * x_start / v0]

sol = solve_ivp(model, t_span, y0, method='RK45', 
                rtol=1e-6, atol=1e-9)

x_traj = sol.y[0] * 1e15 # в фемтометри
y_traj = sol.y[1] * 1e15 # в фемтометри

# --- Розрахунок кута розсіяння (теоретичний) ---
# b = (k_e * ZeZ) / (2 * E) * cot(theta/2)
cot_theta_half = (2 * E * b) / (k_e * ZeZ)
theta_rad = 2 * np.arctan(1 / cot_theta_half)
theta_deg = np.rad2deg(theta_rad)

st.header("Результати")
st.metric("Теоретичний кут розсіяння (θ)", f"{theta_deg:.2f}°")
if b_fm == 0:
    st.info("При b=0 (лобове зіткнення) частинка відбивається назад (θ = 180°).")

# --- Графік ---
st.header("Траєкторія α-частинки")

fig = go.Figure()

# Ядро мішені
fig.add_trace(go.Scatter(
    x=[0], y=[0], mode='markers',
    marker=dict(color='red', size=20, symbol='circle'),
    name=f'Ядро (Z={Z2})'
))

# Траєкторія частинки
fig.add_trace(go.Scatter(
    x=x_traj, y=y_traj, mode='lines',
    line=dict(color='blue', width=3),
    name='Траєкторія α-частинки'
))

# Початкова асимптота
fig.add_trace(go.Scatter(
    x=[-x_start*1e15, x_start*1e15], y=[b_fm, b_fm], mode='lines',
    line=dict(color='gray', width=1, dash='dot'),
    name='Прицільна лінія'
))

max_range = np.max(np.abs(np.concatenate([x_traj, y_traj]))) * 1.1
fig.update_layout(
    xaxis_title="x, фм",
    yaxis_title="y, фм",
    xaxis=dict(range=[-max_range, max_range]),
    yaxis=dict(range=[-max_range, max_range]),
    height=600
)
fig.update_yaxes(scaleanchor="x", scaleratio=1)
st.plotly_chart(fig, use_container_width=True)