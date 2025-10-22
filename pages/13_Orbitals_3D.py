import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.special import sph_harm, genlaguerre

st.set_page_config(layout="wide") # Потрібно більше місця для 3D
st.title("⚛️ 3D-Візуалізатор орбіталей атома Водню")
st.write("Показує поверхню постійної густини ймовірності ($|\Psi_{n,l,m}|^2$)")

# --- Введення квантових чисел ---
st.sidebar.header("Квантові числа")

n_max = 7
n = st.sidebar.slider("Головне (n)", 1, n_max, 3)

# 'l' може бути від 0 до n-1
l_options = list(range(n))
l_options_str = [f"{i} ({'s' if i==0 else 'p' if i==1 else 'd' if i==2 else 'f'})" for i in l_options]
l_selection = st.sidebar.selectbox(
    "Орбітальне (l)", 
    options=l_options,
    format_func=lambda x: f"{x} ({'s' if x==0 else 'p' if x==1 else 'd' if x==2 else 'f'})"
)
l = int(l_selection) # type: ignore

# 'm' може бути від -l до +l
m_options = list(range(-l, l + 1))
m = st.sidebar.selectbox("Магнітне (m)", m_options, index=len(m_options) // 2)

st.sidebar.header("Параметри візуалізації")
N_grid = st.sidebar.slider("Точність сітки (N)", 30, 60, 40, 
                           help="Більше = чіткіше, але повільніше. 40 - добре.")
prob_level = st.sidebar.slider("Рівень ймовірності (%)", 1, 50, 10,
                               help="Який % від макс. ймовірності показати.")

# --- Розрахункова частина ---

@st.cache_data(ttl=3600) # Кешуємо важкі розрахунки
def calculate_orbital_data(n, l, m, N):
    # 1. Створюємо 3D сітку
    # Розмір сітки залежить від 'n', бо орбіталі ростуть (як n²)
    plot_range = 15 * n # Емпірично підібраний діапазон
    x = np.linspace(-plot_range, plot_range, N)
    y = np.linspace(-plot_range, plot_range, N)
    z = np.linspace(-plot_range, plot_range, N)
    X, Y, Z = np.meshgrid(x, y, z)

    # 2. Конвертуємо в сферичні координати
    R = np.sqrt(X**2 + Y**2 + Z**2)
    Theta = np.arccos(np.nan_to_num(Z / R)) # colatitude
    Phi = np.arctan2(Y, X)                 # azimuth
    
    # Запобігаємо діленню на нуль в центрі
    R[R == 0] = 1e-10 # Дуже мале число

    # 3. Радіальна частина R(r)
    # (використовуємо спрощені одиниці, a₀=1, Z=1)
    rho = (2.0 * R) / n
    laguerre_poly = genlaguerre(n - l - 1, 2 * l + 1)(rho)
    
    # Викидаємо нормувальні константи, вони не впливають на форму
    R_nl = np.exp(-rho / 2.0) * (rho**l) * laguerre_poly
    
    # 4. Кутова частина Y(θ, φ)
    Y_lm = sph_harm(m, l, Phi, Theta)
    
    # 5. Хвильова функція (комплексна)
    Psi = R_nl * Y_lm
    
    # 6. Густина ймовірності (дійсна)
    ProbDensity = np.abs(Psi)**2
    
    return X, Y, Z, ProbDensity

st.write(f"### Відображення орбіталі: n={n}, l={l}, m={m}")
with st.spinner(f"Розрахунок {N_grid}³ точок для орбіталі... Це може зайняти хвилину."):
    X, Y, Z, ProbDensity = calculate_orbital_data(n, l, m, N_grid)

    # --- Графік ---
    fig = go.Figure(data=go.Isosurface(
        x=X.flatten(),
        y=Y.flatten(),
        z=Z.flatten(),
        value=ProbDensity.flatten(),
        
        # Ми показуємо поверхню, де P = X% від максимуму
        isomin=(prob_level/100) * ProbDensity.max(),
        isomax=ProbDensity.max(),
        
        surface_count=1,
        caps=dict(x_show=False, y_show=False, z_show=False), # Вимикаємо "зрізи"
        colorscale='balance', # 'RdBu', 'balance'
        reversescale=True
    ))

    fig.update_layout(
        title=f"Орбіталь (n={n}, l={l}, m={m})",
        scene=dict(
            xaxis_title='x (a₀)',
            yaxis_title='y (a₀)',
            zaxis_title='z (a₀)',
            aspectratio=dict(x=1, y=1, z=1) # Робимо куб
        ),
        margin=dict(l=0, r=0, b=0, t=40) # Займаємо весь простір
    )

    st.plotly_chart(fig, use_container_width=True, config={'toImageButtonOptions': {'height': None, 'width': None}})

st.info("""
**Як це читати:**
* **s-орбіталі ($l=0, m=0$)** - сферичні.
* **p-орбіталі ($l=1$)**:
    * $m=0$ дає "гантелю" вздовж осі $z$.
    * $m=\pm 1$ дають "тороїд" (бублик). *Примітка: звичні $p_x$ та $p_y$ орбіталі є **суперпозицією** $m=1$ та $m=-1$.*
* **d-орбіталі ($l=2$)** дають ще складніші "пелюсткові" та "кільцеві" форми.
""")