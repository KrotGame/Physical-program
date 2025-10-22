import streamlit as st
import numpy as np

st.title("💥 Калькулятор 1D зіткнень")
st.write("Розраховує кінцеві швидкості для двох тіл після зіткнення.")

# Використовуємо форму для групування вводу
with st.form(key='collision_form'):
    st.subheader("Тіло 1 (ліве)")
    col1, col2 = st.columns(2)
    m1 = col1.number_input("Маса (m₁), кг", min_value=0.1, value=1.0)
    v1 = col2.number_input("Початкова швидкість (v₁), м/с", value=10.0, format="%.2f")

    st.subheader("Тіло 2 (праве)")
    col3, col4 = st.columns(2)
    m2 = col3.number_input("Маса (m₂), кг", min_value=0.1, value=2.0)
    v2 = col4.number_input("Початкова швидкість (v₂), м/с", value=0.0, format="%.2f")

    st.subheader("Тип зіткнення")
    collision_type = st.radio(
        "Оберіть тип зіткнення:",
        ('Абсолютно пружне', 'Абсолютно непружне (тіла злипаються)')
    )
    
    # Кнопка для відправки форми
    submit_button = st.form_submit_button(label='Розрахувати!')

# --- Розрахункова частина (виконується після натискання кнопки) ---
if submit_button:
    # Початковий імпульс та енергія
    p_initial = m1 * v1 + m2 * v2
    ke_initial = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2

    if collision_type == 'Абсолютно пружне':
        # Формули для пружного зіткнення
        u1 = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
        u2 = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
        
        # Кінцевий імпульс та енергія
        p_final = m1 * u1 + m2 * u2
        ke_final = 0.5 * m1 * u1**2 + 0.5 * m2 * u2**2

        st.header("Результати (Пружне зіткнення)")
        st.metric("Кінцева швидкість Тіла 1 (u₁)", f"{u1:.3f} м/с")
        st.metric("Кінцева швидкість Тіла 2 (u₂)", f"{u2:.3f} м/с")
        
    elif collision_type == 'Абсолютно непружне (тіла злипаються)':
        # Тіла злипаються, кінцева швидкість однакова (u)
        u = (m1 * v1 + m2 * v2) / (m1 + m2)
        u1 = u
        u2 = u
        
        # Кінцевий імпульс та енергія
        p_final = (m1 + m2) * u
        ke_final = 0.5 * (m1 + m2) * u**2
        
        st.header("Результати (Непружне зіткнення)")
        st.metric("Кінцева швидкість обох тіл (u)", f"{u:.3f} м/с")

    st.subheader("Перевірка законів збереження")
    st.info(f"Початковий імпульс: {p_initial:.2f} кг·м/с\n\n"
            f"Кінцевий імпульс: {p_final:.2f} кг·м/с")

    st.warning(f"Початкова кінетична енергія: {ke_initial:.2f} Дж\n\n"
               f"Кінцева кінетична енергія: {ke_final:.2f} Дж")
    
    if collision_type == 'Абсолютно непружне (тіла злипаються)':
        st.write(f"Втрата енергії (перейшла в тепло): {ke_initial - ke_final:.2f} Дж")