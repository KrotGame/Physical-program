import streamlit as st
import numpy as np
import scipy.constants as const # Використовуємо наукові константи з SciPy

st.title("⚛️ Атомні калькулятори")
st.write("Розрахунки за формулами з вступу до квантової механіки.")

# Створюємо дві вкладки
tab1, tab2 = st.tabs(["Формула Рідберга (Л.1)", "Хвиля де Бройля (Л.2)"])

# --- Вкладка 1: Формула Рідберга ---
with tab1:
    st.header("Формула Рідберга (серія Бальмера, etc.)")
    st.write("Розраховує довжину хвилі фотона, що випромінюється при переході електрона в атомі водню.")
    st.latex(r"\frac{1}{\lambda} = R \left( \frac{1}{n_f^2} - \frac{1}{n_i^2} \right)")
    
    col1, col2 = st.columns(2)
    n_i = col1.number_input("Початковий рівень (n_i)", min_value=2, value=3, step=1, 
                             help="Вищий енергетичний рівень")
    n_f = col2.number_input("Кінцевий рівень (n_f)", min_value=1, value=2, step=1,
                             help="Нижчий енергетичний рівень")

    if n_i <= n_f:
        st.error("Початковий рівень (n_i) має бути більшим за кінцевий (n_f) для випромінювання.")
    else:
        # R = 1.097373e7 1/m (стала Рідберга)
        R = const.Rydberg
        
        # Розрахунок
        inv_lambda = R * (1/n_f**2 - 1/n_i**2)
        lambda_meters = 1 / inv_lambda
        lambda_nm = lambda_meters * 1e9 # Переводимо в нанометри
        
        st.metric("Довжина хвилі (λ)", f"{lambda_nm:.2f} нм")
        
        if lambda_nm >= 380 and lambda_nm <= 750:
            st.success("Ця хвиля знаходиться у видимому діапазоні!")
        else:
            st.info("Ця хвиля знаходиться поза видимим діапазоном (УФ або ІЧ).")

# --- Вкладка 2: Хвиля де Бройля ---
with tab2:
    st.header("Довжина хвилі де Бройля")
    st.write("Розраховує довжину хвилі, асоційовану з частинкою, що рухається.")
    st.latex(r"\lambda = \frac{h}{p} = \frac{h}{m \cdot v}")
    
    st.subheader("Оберіть частинку")
    particle = st.selectbox("Тип частинки", 
                            ("Електрон", "Протон", "Нейтрон", "Інша (ввести масу)"))
    
    if particle == "Електрон":
        m = const.electron_mass
    elif particle == "Протон":
        m = const.proton_mass
    elif particle == "Нейтрон":
        m = const.neutron_mass
    else:
        m = st.number_input("Маса частинки (m), кг", min_value=1e-31, value=1.0, format="%e")
    
    st.write(f"Маса (m) = {m:.2e} кг")
    
    v = st.number_input("Швидкість частинки (v), м/с", min_value=0.01, value=1e6)
    
    # Розрахунок
    h = const.h # Стала Планка
    p = m * v
    lambda_de_broglie = h / p
    lambda_pm = lambda_de_broglie * 1e12 # Переводимо в пікометри
    
    st.metric("Імпульс (p)", f"{p:.3e} кг·м/с")
    st.metric("Довжина хвилі де Бройля (λ)", f"{lambda_pm:.3f} пм (пікометрів)")