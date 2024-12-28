import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Constantes
G = 6.67430e-11  # Constante de gravitación universal (m^3 kg^-1 s^-2)
M = 1.989e30     # Masa del sol (kg)

# Sistema de ecuaciones diferenciales
def equations(t, Y):
    x, y, vx, vy = Y
    r = np.sqrt(x**2 + y**2)
    
    # Ecuaciones de movimiento
    dxdt = vx
    dydt = vy
    dvxdt = -G * M * x / r**3
    dvydt = -G * M * y / r**3
    
    return [dxdt, dydt, dvxdt, dvydt]

# Condiciones iniciales: posición (x0, y0) y velocidad (vx0, vy0)
x0 = 1.496e11   # Distancia media de la Tierra al Sol (m)
y0 = 0          # Posición inicial en el eje Y
vx0 = 0         # Velocidad inicial en el eje X (m/s)
vy0 = 29780     # Velocidad inicial en el eje Y (m/s)

Y0 = [x0, y0, vx0, vy0]  # Vector de condiciones iniciales

# Tiempo de simulación
t_span = (0, 3.154e7)  # Un año en segundos (aproximadamente)
t_eval = np.linspace(t_span[0], t_span[1], 1000)  # Puntos de evaluación

# Resolver el sistema de EDOs
solution = solve_ivp(equations, t_span, Y0, t_eval=t_eval)

# Graficar los resultados
plt.figure(figsize=(10, 6))
plt.plot(solution.y[0], solution.y[1], label='Trayectoria del planeta', color='blue')
plt.scatter(0, 0, color='yellow', s=100, label='Sol')  # Representar el Sol
plt.title('Movimiento Planetario bajo Gravitación')
plt.xlabel('Posición X (m)')
plt.ylabel('Posición Y (m)')
plt.axis('equal')
plt.grid()
plt.legend()
plt.show()
