import numpy as np
import plotly.graph_objs as go
from scipy.integrate import solve_ivp
import streamlit as st

# Constantes
G = 6.67430e-11  # Constante de gravitación universal (m^3 kg^-1 s^-2)
M = 1.989e30     # Masa del Sol (kg)

# Datos iniciales aproximados para cada planeta [x0, y0, z0, vx0, vy0, vz0]
planets = {
    'Mercurio': [5.79e10, 0, 0, 0, 47400, 0],
    'Venus': [1.082e11, 0, 0, 0, 35000, 0],
    'Tierra': [1.496e11, 0, 0, 0, 29780, 0],
    'Marte': [2.279e11, 0, 0, 0, 24100, 0],
    'Júpiter': [7.785e11, 0, 0, 0, 13070, 0],
    'Saturno': [1.429e12, 0, 0, 0, 9680, 0],
    'Urano': [2.871e12, 0, 0, 0, 6800, 0],
    'Neptuno': [4.495e12, 0, 0, 0, 5400, 0]
}

colors = {
    'Mercurio': 'brown',
    'Venus': 'orange',
    'Tierra': 'blue',
    'Marte': 'red',
    'Júpiter': 'purple',
    'Saturno': 'yellow',
    'Urano': 'cyan',
    'Neptuno': 'navy'
}

# Función para resolver el sistema de ecuaciones diferenciales en 3D
def equations(t, Y):
    x, y, z, vx, vy, vz = Y
    r = np.sqrt(x**2 + y**2 + z**2)
    
    dxdt = vx
    dydt = vy
    dzdt = vz
    dvxdt = -G * M * x / r**3
    dvydt = -G * M * y / r**3
    dvzdt = -G * M * z / r**3
    
    return [dxdt, dydt, dzdt, dvxdt, dvydt, dvzdt]

# Interfaz de usuario con Streamlit
st.title("Simulador de Movimiento Planetario en 3D")

# Tiempo de simulación
t_span = (0, 3.154e7)  # Un año en segundos (aproximadamente)
t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Puntos de evaluación

# Crear la visualización animada usando Plotly
fig = go.Figure()

# Añadir el Sol en el origen
fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers', marker=dict(size=10, color='yellow'), name='Sol'))

# Simular cada planeta
for planet, initial_conditions in planets.items():
    solution = solve_ivp(equations, t_span, initial_conditions, t_eval=t_eval)
    # Añadir la trayectoria del planeta
    fig.add_trace(go.Scatter3d(
        x=solution.y[0], y=solution.y[1], z=solution.y[2], 
        mode='lines', name=f'Trayectoria de {planet}', 
        line=dict(color=colors[planet])
    ))

# Configuración del layout
fig.update_layout(
    title='Movimiento Planetario bajo Gravitación',
    scene=dict(
        xaxis_title='Posición X (m)',
        yaxis_title='Posición Y (m)',
        zaxis_title='Posición Z (m)',
    ),
    showlegend=True,
    legend=dict(y=-0.3),  # Posición de la leyenda debajo del gráfico
    width=1000,
    height=800,
)

# Mostrar la figura en Streamlit
st.markdown('## Movimiento Planetario bajo Gravitación')
st.plotly_chart(fig)

# Crear una tabla con los datos iniciales de los planetas
st.write("### Datos Iniciales de los Planetas")
initial_data = {
    'Planeta': list(planets.keys()),
    'x0 (m)': [v[0] for v in planets.values()],
    'y0 (m)': [v[1] for v in planets.values()],
    'z0 (m)': [v[2] for v in planets.values()],
    'vx0 (m/s)': [v[3] for v in planets.values()],
    'vy0 (m/s)': [v[4] for v in planets.values()],
    'vz0 (m/s)': [v[5] for v in planets.values()],
}
st.table(initial_data)

# === Segunda parte del gráfico para la Tierra ===

# Parámetros de entrada del usuario
st.sidebar.header("Configuraciones Iniciales - Tierra")
x0 = st.sidebar.number_input("Posición inicial X (m)", value=1.496e11)  # Tierra
y0 = st.sidebar.number_input("Posición inicial Y (m)", value=0.0)
z0 = st.sidebar.number_input("Posición inicial Z (m)", value=0.0)
vx0 = st.sidebar.number_input("Velocidad inicial X (m/s)", value=0.0)
vy0 = st.sidebar.number_input("Velocidad inicial Y (m/s)", value=29780.0)  # Velocidad orbital
vz0 = st.sidebar.number_input("Velocidad inicial Z (m/s)", value=0.0)

# Resolver el sistema de EDOs
Y0 = [x0, y0, z0, vx0, vy0, vz0]  # Vector de condiciones iniciales
solution = solve_ivp(equations, t_span, Y0, t_eval=t_eval)

# Crear la visualización animada usando Plotly
fig = go.Figure()

# Añadir la trayectoria del planeta
fig.add_trace(go.Scatter3d(
    x=solution.y[0], 
    y=solution.y[1], 
    z=solution.y[2], 
    mode='lines', 
    name='Trayectoria', 
    line=dict(color='blue'),
    hoverinfo='x+y+z'  # Añadir información de coordenadas al pasar el ratón
))

# Añadir el Sol en el origen
fig.add_trace(go.Scatter3d(
    x=[0], 
    y=[0], 
    z=[0], 
    mode='markers', 
    marker=dict(size=10, color='yellow'), 
    name='Sol'
))

# Configuración del layout
fig.update_layout(
    title='Movimiento Planetario bajo Gravitación en 3D',
    scene=dict(
        xaxis_title='Posición X (m)',
        yaxis_title='Posición Y (m)',
        zaxis_title='Posición Z (m)',
    ),
    showlegend=True,
    width=800,
    height=600,
)

# Crear la animación del movimiento del planeta
for i in range(len(solution.t)):
    fig.add_trace(go.Scatter3d(
        x=[solution.y[0][i]], 
        y=[solution.y[1][i]], 
        z=[solution.y[2][i]], 
        mode='markers', 
        marker=dict(size=5, color='red'),
        name='Planeta',
        showlegend=False,
        hoverinfo='x+y+z'  # Añadir información de coordenadas al pasar el ratón
    ))

# Mostrar la figura en Streamlit
st.plotly_chart(fig)
