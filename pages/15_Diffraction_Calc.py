import streamlit as st
import numpy as np

st.title("🔬 Калькулятори рентгенівської дифракції")

# --- Створюємо дві вкладки ---
tab1, tab2 = st.tabs(["Закон Брегга", "Індекси Міллера (для куб. ґраток)"])

# --- Вкладка 1: Закон Брегга ---
with tab1:
    st.header("Закон Вульфа-Брегга")
    st.latex(r"n\lambda = 2d \sin(\theta)")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Bragg_diffraction.svg/600px-Bragg_diffraction.svg.png", 
             caption="Схема дифракції Брегга", width=400)
    
    st.subheader("Що розрахувати?")
    calc_option = st.radio(
        "Оберіть невідому величину:",
        ('Кут (θ)', 'Довжина хвилі (λ)', 'Міжплощинна відстань (d)'), 
        horizontal=True
    )
    
    st.divider()
    
    if calc_option == 'Кут (θ)':
        n = st.number_input("Порядок дифракції (n)", min_value=1, value=1, step=1)
        lam = st.number_input("Довжина хвилі (λ), Å (Ангстрем)", min_value=0.1, value=1.54)
        d = st.number_input("Міжплощинна відстань (d), Å", min_value=0.1, value=3.0)
        
        sin_theta = (n * lam) / (2 * d)
        if sin_theta > 1 or sin_theta < -1:
            st.error("Дифракція неможлива (sin(θ) > 1). Змініть параметри.")
        else:
            theta_rad = np.arcsin(sin_theta)
            theta_deg = np.rad2deg(theta_rad)
            st.metric("Кут Брегга (θ)", f"{theta_deg:.3f}°")
            
    elif calc_option == 'Довжина хвилі (λ)':
        n = st.number_input("Порядок дифракції (n)", min_value=1, value=1, step=1)
        d = st.number_input("Міжплощинна відстань (d), Å", min_value=0.1, value=3.0)
        theta_deg = st.number_input("Кут Брегга (θ), градуси", min_value=0.1, max_value=90.0, value=15.0)
        
        theta_rad = np.deg2rad(theta_deg)
        lam = (2 * d * np.sin(theta_rad)) / n
        st.metric("Довжина хвилі (λ)", f"{lam:.4f} Å")
        
    elif calc_option == 'Міжплощинна відстань (d)':
        n = st.number_input("Порядок дифракції (n)", min_value=1, value=1, step=1)
        lam = st.number_input("Довжина хвилі (λ), Å", min_value=0.1, value=1.54)
        theta_deg = st.number_input("Кут Брегга (θ), градуси", min_value=0.1, max_value=90.0, value=15.0)

        theta_rad = np.deg2rad(theta_deg)
        d = (n * lam) / (2 * np.sin(theta_rad))
        st.metric("Міжплощинна відстань (d)", f"{d:.4f} Å")

# --- Вкладка 2: Індекси Міллера ---
with tab2:
    st.header("Індекси Міллера та відстань (d_hkl)")
    st.write("Розраховує міжплощинну відстань 'd' для кубічної системи за індексами Міллера (h, k, l).")
    st.latex(r"d_{hkl} = \frac{a}{\sqrt{h^2 + k^2 + l^2}}")
    
    st.subheader("Вхідні дані")
    a = st.number_input("Параметр ґратки (a), Å", min_value=0.1, value=4.0)
    
    col_h, col_k, col_l = st.columns(3)
    h = col_h.number_input("h", min_value=0, value=1, step=1)
    k = col_k.number_input("k", min_value=0, value=1, step=1)
    l = col_l.number_input("l", min_value=0, value=0, step=1)
    
    if h == 0 and k == 0 and l == 0:
        st.error("Індекси (0, 0, 0) не визначають площину. Введіть інші значення.")
    else:
        d_hkl = a / np.sqrt(h**2 + k**2 + l**2)
        st.metric(f"Відстань d_({h}{k}{l})", f"{d_hkl:.4f} Å")
        
    st.divider()
    
    st.subheader("Бонус: Калькулятор індексів Міллера")
    st.write("Знаходить (hkl) за перетинами з осями. Введіть 'inf' для нескінченності.")
    
    col1, col2, col3 = st.columns(3)
    # МІНЯЄМО number_input НА text_input
    int_a_str = col1.text_input("Перетин по 'a'", value="1.0")
    int_b_str = col2.text_input("Перетин по 'b'", value="inf")
    int_c_str = col3.text_input("Перетин по 'c'", value="inf")
    
    if st.button("Розрахувати (hkl)"):
        try:
            # Функція для перетворення тексту в число або inf
            def parse_intercept(s):
                s_low = s.strip().lower()
                if s_low == 'inf' or s_low == 'infinity':
                    return np.inf
                val = float(s)
                if val == 0:
                    # Викидаємо помилку, яку перехопить 'try'
                    raise ValueError("Перетин 0") 
                return val
            
            int_a = parse_intercept(int_a_str)
            int_b = parse_intercept(int_b_str)
            int_c = parse_intercept(int_c_str)

            # 1. Беремо обернені значення
            with np.errstate(divide='ignore'): # Ігноруємо ділення на inf (1/inf = 0)
                inv_a = 1.0 / int_a
                inv_b = 1.0 / int_b
                inv_c = 1.0 / int_c
            
            # 2. Зводимо до найменших цілих чисел
            # Знаходимо макс. значення для нормалізації
            max_val = max(abs(inv_a), abs(inv_b), abs(inv_c))
            if max_val == 0:
                 st.error("Неможливо розрахувати. Потрібен хоча б один скінченний перетин.")
            else:
                norm = np.array([inv_a, inv_b, inv_c]) / max_val
                
                # Шукаємо множник, щоб зробити їх цілими (до 10)
                multiplier = 1
                for i in range(1, 11):
                    # Порівнюємо з допуском 1e-5
                    if np.allclose((norm * i) % 1, 0, atol=1e-5) or np.allclose((norm * i) % 1, 1, atol=1e-5):
                        multiplier = i
                        break
                
                # Округлюємо, щоб позбутися малих похибок (напр., 2.9999 -> 3)
                h, k, l = np.round(norm * multiplier).astype(int)
                st.success(f"### Індекси Міллера: ({h}, {k}, {l})")

        except ValueError as e:
            if "Перетин 0" in str(e):
                st.error("Перетин не може бути 0 (площина проходить через початок координат).")
            else:
                st.error(f"Неправильний ввід. Введіть число (напр., '1.5') або 'inf'.")