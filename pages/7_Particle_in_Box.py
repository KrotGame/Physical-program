import streamlit as st
import numpy as np
import plotly.graph_objects as go
import scipy.constants as const

st.title("🔳 Частинка у 1D потенціальному ящику")
st.write("Візуалізація хвильових функцій (Ψ) та густини ймовірності (Ψ²) для стаціонарного рівняння Шредінгера (тема Л.5).")

# --- Бічна панель ---
st.sidebar.header("Параметри ящика")
L_pm = st.sidebar.slider("Ширина ящика (L), пікометри", 50, 1000, 100, step=10)
L = L_pm * 1e-12 # Переводимо в метри

n = st.sidebar.slider("Квантове число (n)", 1, 10, 1, step=1, 
                      help="Основний (n=1), перший збуджений (n=2), ...")

# Використовуємо масу електрона
m = const.electron_mass
hbar = const.hbar

# --- Розрахункова частина ---

# 1. Розрахунок енергії
# E_n = (n^2 * pi^2 * hbar^2) / (2 * m * L^2)
E_joules = (n**2 * np.pi**2 * hbar**2) / (2 * m * L**2)
E_eV = E_joules / const.electron_volt # Переводимо в електрон-вольти

st.header(f"Рівень n = {n}")
st.metric("Енергія рівня (Eₙ)", f"{E_eV:.3f} еВ (електрон-вольт)")

# 2. Розрахунок для графіка
x = np.linspace(0, L, 500) # 500 точок всередині ящика

# Хвильова функція: Psi(x) = sqrt(2/L) * sin(n * pi * x / L)
psi = np.sqrt(2/L) * np.sin(n * np.pi * x / L)

# Густина ймовірності: |Psi(x)|^2
prob_density = psi**2

# --- Графіки ---

# Конвертуємо x в пікометри для гарного відображення
x_pm = x * 1e12

# Графік 1: Хвильова функція
st.subheader("Хвильова функція (Ψ)")
fig_psi = go.Figure()

# Потенціальні стінки (для візуалізації)
fig_psi.add_trace(go.Scatter(x=[0, 0], y=[-np.max(np.abs(psi))*1.2, np.max(np.abs(psi))*1.2], 
                            mode='lines', line=dict(color='black', width=3), name='Стінка'))
fig_psi.add_trace(go.Scatter(x=[L_pm, L_pm], y=[-np.max(np.abs(psi))*1.2, np.max(np.abs(psi))*1.2], 
                            mode='lines', line=dict(color='black', width=3), name='Стінка'))

# Сама хвильова функція
fig_psi.add_trace(go.Scatter(x=x_pm, y=psi, mode='lines', 
                            line=dict(color='blue', width=3), name=f"Ψ (n={n})"))
# Нульова лінія
fig_psi.add_trace(go.Scatter(x=x_pm, y=np.zeros_like(x_pm), mode='lines', 
                            line=dict(color='gray', width=1, dash='dot'), name='y=0'))

fig_psi.update_layout(
    xaxis_title="Позиція (x), пм",
    yaxis_title="Амплітуда (Ψ)",
    showlegend=False
)
st.plotly_chart(fig_psi, use_container_width=True)

# Графік 2: Густина ймовірності
st.subheader("Густина ймовірності (Ψ²)")
st.write("Показує, де найімовірніше знайти частинку.")
fig_prob = go.Figure()

# Стінки
fig_prob.add_trace(go.Scatter(x=[0, 0], y=[0, np.max(prob_density)*1.2], 
                             mode='lines', line=dict(color='black', width=3), name='Стінка'))
fig_prob.add_trace(go.Scatter(x=[L_pm, L_pm], y=[0, np.max(prob_density)*1.2], 
                             mode='lines', line=dict(color='black', width=3), name='Стінка'))

# Густина ймовірності
fig_prob.add_trace(go.Scatter(x=x_pm, y=prob_density, mode='lines', 
                             line=dict(color='red', width=3), name=f"|Ψ|² (n={n})"))

fig_prob.update_layout(
    xaxis_title="Позиція (x), пм",
    yaxis_title="Ймовірність (|Ψ|²)",
    showlegend=False
)
st.plotly_chart(fig_prob, use_container_width=True)