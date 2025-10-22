import streamlit as st
import numpy as np

st.title("☢️ Калькулятор радіоактивного розпаду")
st.write("Розраховує кількість речовини та активність, що залишились.")

st.info("Переконайтеся, що 'Період напіврозпаду' і 'Час, що минув' в однакових одиницях (напр., обидва в роках або обидва в секундах).")

# --- Введення даних ---
col1, col2 = st.columns(2)
n0 = col1.number_input("Початкова кількість ядер (N₀)", min_value=1.0, value=1e20, format="%e")
t_half = col2.number_input("Період напіврозпаду (T₁/₂)", min_value=0.001, value=10.0)
t = st.number_input("Час, що минув (t)", min_value=0.0, value=5.0)

# --- Розрахункова частина ---
if t_half > 0:
    # 1. Знаходимо сталу розпаду (lambda)
    lambda_const = np.log(2) / t_half
    
    # 2. Знаходимо кількість ядер, що залишились (N(t))
    # N(t) = N₀ * e^(-λ * t)
    n_t = n0 * np.exp(-lambda_const * t)
    
    # 3. Знаходимо початкову активність (A₀)
    # A(t) = λ * N(t)
    a0 = lambda_const * n0
    
    # 4. Знаходимо кінцеву активність (A(t))
    a_t = lambda_const * n_t

    st.header("Результати розрахунку")
    
    col_res1, col_res2 = st.columns(2)
    col_res1.metric("Ядер залишилось (N(t))", f"{n_t:.3e} ядер")
    col_res2.metric("Ядер розпалось", f"{n0 - n_t:.3e} ядер")
    
    st.divider()

    col_res3, col_res4 = st.columns(2)
    col_res3.metric("Початкова активність (A₀)", f"{a0:.3e} Бк (розпадів/одиницю часу)")
    col_res4.metric("Кінцева активність (A(t))", f"{a_t:.3e} Бк (розпадів/одиницю часу)")
    
    st.subheader("Додаткові параметри")
    st.latex(f"\\lambda = \\frac{{\\ln(2)}}{{T_{{1/2}}}} = \\frac{{0.693}}{{{t_half:.2f}}} \\approx {lambda_const:.3e} \\text{{ (одиниць часу) }}^{{-1}}")
    st.latex(f"N(t) = N_0 \\cdot e^{{-\\lambda t}} = {n0:.2e} \\cdot e^{{-{lambda_const:.2e} \\cdot {t:.2f}}}")

else:
    st.error("Період напіврозпаду має бути > 0")