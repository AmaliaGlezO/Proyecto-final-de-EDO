import numpy as np
import plotly.graph_objs as go
from scipy.integrate import solve_ivp
import streamlit as st

# Constantes
G = 6.67430e-11  # Constante de gravitación universal (m^3 kg^-1 s^-2)
M = 1.989e30     # Masa del sol (kg)

# Función para resolver el sistema de ecuaciones diferenciales
def equations(t, Y):
    x, y, vx, vy = Y
    r = np.sqrt(x**2 + y**2)
    
    dxdt = vx
    dydt = vy
    dvxdt = -G * M * x / r**3
    dvydt = -G * M * y / r**3
    
    return [dxdt, dydt, dvxdt, dvydt]

# Interfaz de usuario con Streamlit
st.title("Simulador de Movimiento Planetario")

# Parámetros de entrada del usuario
st.sidebar.header("Configuraciones Iniciales")
x0 = st.sidebar.number_input("Posición inicial X (m)", value=1.496e11)  # Tierra
y0 = st.sidebar.number_input("Posición inicial Y (m)", value=0.0)
vx0 = st.sidebar.number_input("Velocidad inicial X (m/s)", value=0.0)
vy0 = st.sidebar.number_input("Velocidad inicial Y (m/s)", value=29780.0)  # Velocidad orbital

# Tiempo de simulación
t_span = (0, 3.154e7)  # Un año en segundos (aproximadamente)
t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Puntos de evaluación

# Resolver el sistema de EDOs
Y0 = [x0, y0, vx0, vy0]  # Vector de condiciones iniciales
solution = solve_ivp(equations, t_span, Y0, t_eval=t_eval)

# Crear la visualización animada usando Plotly
fig = go.Figure()

# Añadir la trayectoria del planeta
fig.add_trace(go.Scatter(x=solution.y[0], y=solution.y[1], mode='lines', name='Trayectoria', line=dict(color='blue')))

# Añadir el Sol en el origen
fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=10, color='yellow'), name='Sol'))

# Configuración del layout
fig.update_layout(
    title='Movimiento Planetario bajo Gravitación',
    xaxis_title='Posición X (m)',
    yaxis_title='Posición Y (m)',
    showlegend=True,
    width=800,
    height=600,
)

# Crear la animación del movimiento del planeta
for i in range(len(solution.t)):
    fig.add_trace(go.Scatter(
        x=[solution.y[0][i]], 
        y=[solution.y[1][i]], 
        mode='markers', 
        marker=dict(size=5, color='red'),
        name='Planeta',
        showlegend=False,
        hoverinfo='none'
    ))

# Mostrar la figura en Streamlit
st.plotly_chart(fig)
