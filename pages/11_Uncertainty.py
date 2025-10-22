import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.fft import fft, fftfreq, fftshift
import scipy.constants as const

st.title("🌊 Візуалізатор принципу невизначеності")
st.write("Показує зв'язок між положенням (Δx) та імпульсом (Δp) частинки.")
st.latex(r"\Delta x \cdot \Delta p \geq \frac{\hbar}{2}")

# --- Введення даних ---
st.sidebar.header("Параметри хвильового пакету")
st.write("Хвильовий пакет моделюється Гауссовою функцією.")

delta_x_pm = st.sidebar.slider("Невизначеність положення (Δx), пм", 1.0, 100.0, 20.0, 1.0)
delta_x = delta_x_pm * 1e-12 # Переводимо в метри

# --- Розрахункова частина ---

# 1. Створюємо простір x
# Чим ширший діапазон, тим кращий Фур'є-аналіз
N = 2048 # Кількість точок (краще степінь 2)
x_max = delta_x * 50 # Беремо великий діапазон
x = np.linspace(-x_max, x_max, N)

# 2. Хвильова функція в x-просторі (Гауссів пакет)
# Psi(x) ~ exp(-x² / (4 * delta_x²))
# Ми будемо малювати |Psi(x)|²
psi_x_sq = np.exp(-x**2 / (2 * delta_x**2))
psi_x_sq = psi_x_sq / np.sum(psi_x_sq) # Нормуємо (для вигляду)

# 3. Хвильова функція в k-просторі (Фур'є-образ)
# Фур'є-образ Гауссової функції - це теж Гауссова функція
# Використовуємо Швидке перетворення Фур'є (FFT)
psi_k = fft(psi_x_sq)
psi_k_sq = np.abs(psi_k)**2
psi_k_sq = psi_k_sq / np.sum(psi_k_sq) # Нормуємо

# 4. Створюємо простір k (хвильове число)
# k = 2*pi / L
dx = x[1] - x[0]
k = fftfreq(N, d=dx) * 2 * np.pi

# 5. Створюємо простір p (імпульс)
# p = hbar * k
p = const.hbar * k

# Важливо! Відцентрувати k і p для графіка
k_shifted = fftshift(k)
p_shifted = fftshift(p)
psi_k_sq_shifted = fftshift(psi_k_sq)

# 6. Розрахунок невизначеностей
# Для Гауссового пакету: delta_x (задано)
# delta_k = 1 / (2 * delta_x)
delta_k_calc = 1 / (2 * delta_x)
# delta_p = hbar * delta_k
delta_p_calc = const.hbar * delta_k_calc
product = delta_x * delta_p_calc
hbar_2 = const.hbar / 2

# --- Відображення ---
st.header("Теоретичні невизначеності")
col1, col2 = st.columns(2)
col1.metric("Задана невизначеність (Δx)", f"{delta_x_pm:.1f} пм")
col2.metric("Розрахункова (Δp)", f"{delta_p_calc:.2e} кг·м/с")

st.subheader("Перевірка співвідношення")
st.metric(f"Добуток (Δx · Δp)", f"{product:.2e}")
st.metric(f"Теоретичний мінімум (ħ/2)", f"{hbar_2:.2e}")
if product < hbar_2:
     st.error("Щось пішло не так!")
else:
     st.success("Співвідношення виконується!")

st.info("Спробуйте змінити Δx: якщо пакет 'вузький' у просторі (мале Δx), він стає 'широким' в імпульсі (велике Δp), і навпаки.")

# --- Графіки ---
x_plot_pm = x * 1e12 # x в пікометрах

# Графік 1: Простір положень
st.subheader("Густина ймовірності в просторі положень |Ψ(x)|²")
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=x_plot_pm, y=psi_x_sq, mode='lines', name='|Ψ(x)|²'))
fig1.update_layout(
    xaxis_title="Положення (x), пм",
    yaxis_title="Ймовірність"
)
fig1.update_xaxes(range=[-delta_x_pm * 5, delta_x_pm * 5])
st.plotly_chart(fig1, use_container_width=True)


# Графік 2: Простір імпульсів
st.subheader("Густина ймовірності в просторі імпульсів |Φ(p)|²")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=p_shifted, y=psi_k_sq_shifted, mode='lines', 
                         line=dict(color='red'), name='|Φ(p)|²'))
fig2.update_layout(
    xaxis_title="Імпульс (p), кг·м/с",
    yaxis_title="Ймовірність"
)
# Обмежуємо діапазон для гарного вигляду
p_plot_range = delta_p_calc * 5
fig2.update_xaxes(range=[-p_plot_range, p_plot_range])
st.plotly_chart(fig2, use_container_width=True)