import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# Definir el sistema de ecuaciones diferenciales
def sistema(y, t):
    x, z = y
    dxdt = z
    dzdt = -x
    return [dxdt, dzdt]

# Condiciones iniciales
y0 = [1.0, 0.0]

# Puntos de tiempo donde se evaluará la solución
t = np.linspace(0, 10, 100)

# Resolver el sistema de ecuaciones diferenciales
sol = odeint(sistema, y0, t)

# Graficar los resultados
plt.plot(t, sol[:, 0], label='x(t)')
plt.plot(t, sol[:, 1], label='z(t)')
plt.xlabel('Tiempo')
plt.ylabel('Soluciones')
plt.legend()
plt.show()
