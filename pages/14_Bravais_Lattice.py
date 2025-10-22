import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("🧊 3D-Візуалізатор кубічних ґраток Браве")
st.write("Показує розташування атомів та розраховує коефіцієнт пакування.")

lattice_type = st.selectbox(
    "Оберіть тип кубічної ґратки:",
    ("Проста кубічна (ПК)", 
     "Об'ємно-центрована кубічна (ОЦК)", 
     "Гра не-центрована кубічна (ГЦК)")
)

# --- Розрахункова частина ---

# --- Розрахункова частина ---

# Атоми (x, y, z) в межах комірки [0, 1]
atoms = {
    'ПК': np.array([[0, 0, 0]]),
    'ОЦК': np.array([[0, 0, 0], [0.5, 0.5, 0.5]]),
    'ГЦК': np.array([
        [0, 0, 0], 
        [0.5, 0.5, 0], 
        [0.5, 0, 0.5], 
        [0, 0.5, 0.5]
    ])
}

# Атоми для візуалізації (включаючи сусідні комірки для повноти)
viz_atoms = {
    'ПК': np.array([
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
        [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]
    ]),
    'ОЦК': np.array([
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
        [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1],
        [0.5, 0.5, 0.5] # Центральний
    ]),
    'ГЦК': np.array([
        # Вершини
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
        [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1],
        # Грані
        [0.5, 0.5, 0], [0.5, 0.5, 1], # xy
        [0.5, 0, 0.5], [0.5, 1, 0.5], # xz
        [0, 0.5, 0.5], [1, 0.5, 0.5]  # yz
    ])
}

# Параметри ґраток
params = {
    'ПК': {
        'atoms_per_cell': 1, # 8 вершин * (1/8)
        'coord_num': 6,
        'a_R_relation': "a = 2R",
        'apf_formula': "(1 * 4/3 * pi * (a/2)³) / a³",
        'apf': (np.pi / 6)
    },
    'ОЦК': {
        'atoms_per_cell': 2, # (8 * 1/8) + 1 (центр)
        'coord_num': 8,
        'a_R_relation': "a√3 = 4R",
        'apf_formula': "(2 * 4/3 * pi * (a√3 / 4)³) / a³",
        'apf': (np.pi * np.sqrt(3) / 8)
    },
    'ГЦК': {
        'atoms_per_cell': 4, # (8 * 1/8) + (6 * 1/2)
        'coord_num': 12,
        'a_R_relation': "a√2 = 4R",
        'apf_formula': "(4 * 4/3 * pi * (a√2 / 4)³) / a³",
        'apf': (np.pi / (3 * np.sqrt(2)))
    }
}

# *** ЦЕ ВИПРАВЛЕННЯ ДЛЯ 'KeyError' ***
current_type = lattice_type.split(' ')[-1].strip("()")

# *** ЦІ РЯДКИ МАЮТЬ БУТИ, ВОНИ СТВОРЮЮТЬ ЗМІННІ ***
current_params = params[current_type]
current_atoms = viz_atoms[current_type]


# --- Відображення параметрів ---
st.header(f"Параметри для: {lattice_type}")

col1, col2, col3 = st.columns(3)
# Тепер цей рядок (line 84) має спрацювати
col1.metric("Атомів на комірку", current_params['atoms_per_cell'])
col2.metric("Координаційне число", current_params['coord_num'])
col3.metric("Коеф. пакування (APF)", f"{current_params['apf'] * 100:.1f} %")

st.subheader("Розрахунок APF")
# *** ЦЕ ВИПРАВЛЕННЯ ДЛЯ 'SyntaxError' (прибрано 'f') ***
st.latex("a \\text{ (параметр ґратки)}, R \\text{ (радіус атома)}")
# А тут 'f' залишаються, бо вони потрібні
st.latex(f"\\text{{Співвідношення: }} {current_params['a_R_relation']}")
st.latex(f"APF = \\frac{{N_{{atoms}} \\cdot V_{{atom}}}}{{V_{{cell}}}} = {current_params['apf_formula']} \\approx {current_params['apf']:.3f}")

# --- 3D Графік ---
st.header("3D Візуалізація")
fig = go.Figure()

# 1. Атоми
fig.add_trace(go.Scatter3d(
    x=current_atoms[:, 0],
    y=current_atoms[:, 1],
    z=current_atoms[:, 2],
    mode='markers',
    marker=dict(color='red', size=10, symbol='circle'),
    name='Атоми'
))

# 2. Ребра куба (комірки)
def add_cube_edges(fig):
    edges = [
        (0,1), (1,3), (3,2), (2,0), # bottom
        (4,5), (5,7), (7,6), (6,4), # top
        (0,4), (1,5), (2,6), (3,7)  # vertical
    ]
    vertices = np.array([
        [0,0,0], [1,0,0], [0,1,0], [1,1,0],
        [0,0,1], [1,0,1], [0,1,1], [1,1,1]
    ])
    for edge in edges:
        p1 = vertices[edge[0]]
        p2 = vertices[edge[1]]
        fig.add_trace(go.Scatter3d(
            x=[p1[0], p2[0]], y=[p1[1], p2[1]], z=[p1[2], p2[2]],
            mode='lines', line=dict(color='black', width=3),
            showlegend=False
        ))
add_cube_edges(fig)

fig.update_layout(
    title="Елементарна комірка",
    scene=dict(
        xaxis=dict(range=[-0.1, 1.1], title='a'),
        yaxis=dict(range=[-0.1, 1.1], title='b'),
        zaxis=dict(range=[-0.1, 1.1], title='c'),
        aspectratio=dict(x=1, y=1, z=1)
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)
st.plotly_chart(fig, use_container_width=True)