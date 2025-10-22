import streamlit as st
import numpy as np
import plotly.graph_objects as go
import scipy.constants as const

st.title("👻 Квантове тунелювання через бар'єр")
st.write("Візуалізація хвильової функції частинки, що налітає на потенційний бар'єр.")

# --- Введення даних ---
st.sidebar.header("Параметри")
E_eV = st.sidebar.slider("Енергія частинки (E), еВ", 0.1, 10.0, 5.0, 0.1)
V0_eV = st.sidebar.slider("Висота бар'єру (V₀), еВ", E_eV + 0.1, 20.0, 10.0, 0.1,
                          help="V₀ має бути більшим за E для тунелювання.")
L_pm = st.sidebar.slider("Ширина бар'єру (L), пм", 10, 200, 50, 5)

m = const.electron_mass # Маса електрона

# Переводимо все в СІ
E = E_eV * const.electron_volt
V0 = V0_eV * const.electron_volt
L = L_pm * 1e-12
hbar = const.hbar

# --- Розрахункова частина ---

# 1. Хвильові числа
k1 = np.sqrt(2 * m * E) / hbar             # Область I (зліва, x < 0)
k2 = np.sqrt(2 * m * (V0 - E)) / hbar    # Область II (бар'єр, 0 < x < L)
k3 = k1                                    # Область III (справа, x > L)

# 2. Розрахунок коефіцієнта проходження (T)
# Формула Гріфітса для T
numerator = (2 * k1 * k2)**2
denominator = (k2**2 - k1**2)**2 * np.sinh(k2 * L)**2 + (2 * k1 * k2)**2 * np.cosh(k2 * L)**2
T = numerator / denominator

st.header("Ймовірність тунелювання")
st.metric("Коефіцієнт проходження (T)", f"{T:.3e}",
          help="Ймовірність того, що частинка пройде крізь бар'єр.")

# --- Графік ---
st.header("Візуалізація хвильової функції (Re[Ψ])")

# 3. Розрахунок амплітуд для графіка (дуже спрощено, лише для візуалізації!)
# Ми не будемо точно розв'язувати систему, а покажемо загальний вигляд:
# A * e^(ik1*x) + B * e^(-ik1*x) | C * e^(-k2*x) + D * e^(k2*x) | F * e^(ik1*x)
# Це складно. Для візуалізації ми просто покажемо затухаючу експоненту та синусоїди
x_left = np.linspace(-L*2, 0, 100)
x_barrier = np.linspace(0, L, 50)
x_right = np.linspace(L, L*3, 100)

# Амплітуди (приблизні, для красивої картинки)
A = 1 # Вхідна хвиля
F = np.sqrt(T) # Хвиля, що пройшла
R = np.sqrt(1 - T) # Відбита хвиля

psi_left = A * np.cos(k1 * x_left) + R * np.cos(-k1 * x_left + np.pi) # Стояча хвиля
psi_barrier = (A+R)/2 * np.exp(-k2 * x_barrier) # Затухання (дуже грубе спрощення)
psi_right = F * np.cos(k1 * (x_right - L)) # Біжуча хвиля

# Переводимо x в пікометри
x_plot = np.concatenate((x_left, x_barrier, x_right)) * 1e12
psi_plot = np.concatenate((psi_left, psi_barrier, psi_right))

fig = go.Figure()

# Хвильова функція
fig.add_trace(go.Scatter(x=x_plot, y=psi_plot, mode='lines', name='Re[Ψ(x)]',
                         line=dict(color='blue', width=3)))

# Потенційний бар'єр
fig.add_trace(go.Scatter(
    x=[0, 0, L_pm, L_pm],
    y=[0, V0_eV, V0_eV, 0],
    fill="tozeroy",
    fillcolor="rgba(255, 0, 0, 0.2)",
    line=dict(color="red", width=2, dash='dot'),
    name='Бар\'єр (V₀)'
))

# Енергія частинки
fig.add_trace(go.Scatter(x=[np.min(x_plot), np.max(x_plot)], y=[E_eV, E_eV],
                         mode='lines', line=dict(color='green', width=2, dash='dash'),
                         name='Енергія (E)'))

fig.update_layout(
    title="Реальна частина хвильової функції",
    xaxis_title="Позиція (x), пм",
    yaxis_title="Енергія (умовні одиниці)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)
st.info("Примітка: Графік хвильової функції є спрощеною візуалізацією і не є точним розв'язком рівняння Шредінгера, але якісно показує ефект затухання та проходження.")