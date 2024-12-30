import numpy as np
import plotly.graph_objs as go
from scipy.integrate import solve_ivp
import streamlit as st

# Constantes
G = 6.67430e-11  # Constante de gravitación universal (m^3 kg^-1 s^-2)
M = 1.989e30     # Masa del Sol (kg)

# Datos iniciales aproximados para los primeros cuatro planetas [x0, y0, vx0, vy0]
planets = {
    'Mercurio': [5.79e10, 0, 0, 47400],
    'Venus': [1.082e11, 0, 0, 35000],
    'Tierra': [1.496e11, 0, 0, 29780],
    'Marte': [2.279e11, 0, 0, 24100]
}

colors = {
    'Mercurio': 'brown',
    'Venus': 'yellow',
    'Tierra': 'blue',
    'Marte': 'red'
}

# Función para resolver el sistema de ecuaciones diferenciales en 2D
def equations(t, Y):
    x, y, vx, vy = Y
    r = np.sqrt(x**2 + y**2)
    
    dxdt = vx
    dydt = vy
    dvxdt = -G * M * x / r**3
    dvydt = -G * M * y / r**3
    
    return [dxdt, dydt, dvxdt, dvydt]


# Tiempo de simulación
t_span = (0, 3.154e7)  # Un año en segundos (aproximadamente)
t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Puntos de evaluación

# Crear la visualización animada usando Plotly
fig = go.Figure()

# Añadir el Sol en el origen
fig.add_trace(go.Scatter(
    x=[0], y=[0], mode='markers', marker=dict(size=10, color='yellow'), name='Sol'
))

# Simular cada planeta
frames = []
for planet, initial_conditions in planets.items():
    solution = solve_ivp(equations, t_span, initial_conditions, t_eval=t_eval)
    # Añadir la trayectoria del planeta
    fig.add_trace(go.Scatter(
        x=solution.y[0], y=solution.y[1], mode='lines', name=f'Trayectoria de {planet}',
        line=dict(color=colors[planet])
    ))

    # Crear la animación del movimiento del planeta
    planet_frames = [go.Frame(
        data=[
            go.Scatter(
                x=[solution.y[0][i]], y=[solution.y[1][i]],
                mode='markers', marker=dict(size=5, color=colors[planet])
            )
        ],
        name=f'{planet}_frame{i}'
    ) for i in range(len(solution.t))]
    frames.extend(planet_frames)

fig.frames = frames
fig.update_layout(
    updatemenus=[{
        'type': 'buttons',
        'buttons': [{
            'label': 'Play',
            'method': 'animate',
            'args': [None, {'frame': {'duration': 50, 'redraw': True}, 'fromcurrent': True}]
        }]
    }]
)

# Configuración del layout
fig.update_layout(
    title='Movimiento Planetario bajo Gravitación en 2D (Primeros 4 Planetas)',
    xaxis_title='Posición X (m)',
    yaxis_title='Posición Y (m)',
    showlegend=True,
    width=800,
    height=600,
    yaxis=dict(scaleanchor="x", scaleratio=1)  # Asegurar que los ejes tengan la misma escala
)

# Mostrar la figura en Streamlit
st.plotly_chart(fig)
