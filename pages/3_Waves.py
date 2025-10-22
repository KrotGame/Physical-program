import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("🌊 Суперпозиція хвиль")
st.write("Демонструє, як дві біжучі хвилі додаються, створюючи інтерференційну картину.")

# --- Бічна панель ---
st.sidebar.header("Параметри")
L = 10.0 # Довжина простору
x = np.linspace(0, L, 500)

st.sidebar.subheader("Хвиля 1 (Синя)")
A1 = st.sidebar.slider("Амплітуда (A₁)", 0.0, 5.0, 1.0)
lambda1 = st.sidebar.slider("Довжина хвилі (λ₁)", 0.1, 5.0, 2.0)
v1 = st.sidebar.slider("Швидкість (v₁)", -2.0, 2.0, 1.0)

st.sidebar.subheader("Хвиля 2 (Червона)")
A2 = st.sidebar.slider("Амплітуда (A₂)", 0.0, 5.0, 1.0)
lambda2 = st.sidebar.slider("Довжина хвилі (λ₂)", 0.1, 5.0, 2.0)
v2 = st.sidebar.slider("Швидкість (v₂)", -2.0, 2.0, -1.0)

# Слайдер для часу
t = st.slider("Час (t)", 0.0, 10.0, 0.0, 0.1)

# --- Розрахункова частина ---

# Функція хвилі: y = A * sin(k*x - w*t)
# k = 2*pi / lambda (хвильове число)
# w = k * v (кутова частота)

def wave_function(x, t, A, lambda_val, v):
    k = 2 * np.pi / lambda_val
    omega = k * v
    return A * np.sin(k * x - omega * t)

y1 = wave_function(x, t, A1, lambda1, v1)
y2 = wave_function(x, t, A2, lambda2, v2)
y_sum = y1 + y2

# --- Графік ---
st.header("Результат суперпозиції")

fig = go.Figure()

# Сумарна хвиля (головна)
fig.add_trace(go.Scatter(
    x=x, y=y_sum, 
    mode='lines', 
    name='Сума (Y₁ + Y₂)',
    line=dict(color='black', width=4)
))

# Індивідуальні хвилі (напівпрозорі)
fig.add_trace(go.Scatter(
    x=x, y=y1, 
    mode='lines', 
    name='Хвиля 1',
    line=dict(color='blue', width=2, dash='dot')
))
fig.add_trace(go.Scatter(
    x=x, y=y2, 
    mode='lines', 
    name='Хвиля 2',
    line=dict(color='red', width=2, dash='dot')
))

fig.update_layout(
    title="Інтерференція хвиль у момент часу t",
    xaxis_title="Позиція (x), м",
    yaxis_title="Зміщення (y)",
    yaxis=dict(range=[- (A1+A2)*1.2, (A1+A2)*1.2]), # Фіксований діапазон Y
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)

st.plotly_chart(fig, use_container_width=True)

st.info("Спробуйте погратися зі слайдером 'Час (t)', щоб побачити рух хвиль, або змініть параметри, щоб побачити стоячі хвилі (v₁ = -v₂ та λ₁ = λ₂).")