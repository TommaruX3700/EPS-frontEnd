# Questo script in python simula, attraverso un'interfaccia grafica, la visualizzazione di parallelepipedi all'interno
# di un contenitore, ed è utile per eseguire dei test sull'efficienza dell'algoritmo di nesting. Sarà successivamente
# aggiornato per collegarlo effettivamente all'algoritmo, per ora lo script è solo un prototipo che visualizza a
# schermo due parallelepipedi
 

import numpy as np # libreria per la gestione degli array e operazioni matematiche su di essi
import matplotlib.pyplot as plt # libreria per la visualizzazione grafica 3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


# Definisco la funzione di creazione dei parallelepipedi
def make_parallelepiped(center, size, direction, facecolor):
    # Calcola la metà delle dimensioni in ciascuna direzione
    half_size = np.array(size) / 2.0
    # Calcola i vettori di base del parallelepipedo
    v1, v2, v3 = np.array(direction) * half_size[:, np.newaxis]
    # Calcolo i vertici del parallelepipedo
    vertices = [center + v1 + v2 + v3,
                center + v1 - v2 + v3,
                center - v1 - v2 + v3,
                center - v1 + v2 + v3,
                center + v1 + v2 - v3,
                center + v1 - v2 - v3,
                center - v1 - v2 - v3,
                center - v1 + v2 - v3]
    # Definisco le facce del parallelepipedo
    faces = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4],
             [1, 2, 6, 5], [2, 3, 7, 6], [0, 3, 7, 4]]
    # Creo un oggetto Poly3DCollection per il parallelepipedo
    parallelepiped = Poly3DCollection([[vertices[i] for i in face] for face in faces], alpha=.25, facecolor=facecolor)
    return parallelepiped

# Definisco il grafico 3d
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Definisco costante di direzione (Utilizzo di versori di direzione, da valutare per l'implementazione anche nell'algoritmo)
const=1 # Se fosse 0.5, il pacco verrebbe dimezzato nelle sue dimensioni perchè vengono dimezzati i versori di direzione

# Definisco il primo parallelepipedo
center1 = np.array([50, 50, 50]) # coordinate del centro
size1 = np.array([50, 30, 100]) # dimensioni del pacco
direction = [const, const, const] # direzione
direction1 = np.diag(direction)
parallelepiped1 = make_parallelepiped(center1, size1, direction1, "r") # creazione parallelepipedo
ax.add_collection3d(parallelepiped1) # inserimento del parallelepipedo nel grafico

# Definisco il secondo parallelepipedo
center2 = np.array([40, 100, 25]) # coordinate del centro
size2 = np.array([60, 30, 50]) # dimensioni del pacco
direction2 = [const, const, const] # direzione
direction2 = np.diag(direction2) 
parallelepiped2 = make_parallelepiped(center2, size2, direction2, "b") # creazione parallelepipedo
ax.add_collection3d(parallelepiped2) # inserimento del parallelepipedo nel grafico


# Definisco i limiti del grafico
ax.set_xlim([0, 80])
ax.set_ylim([0, 120])
ax.set_zlim([0, 230])

# Definisco i nomi degli assi
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Definisco le proporzioni del grafico
ax.set_box_aspect([80,120,230])

# Visualizzo il grafico
plt.show()