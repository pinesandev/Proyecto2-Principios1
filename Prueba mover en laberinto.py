import tkinter as tk

# laberinto: 0 = camino, 1 = pared, -1 = inicio y 2 = meta

laberinto = [
    [0,0,1,1,1,1,0,0],
    [1,0,0,0,1,0,0,1],
    [1,0,1,0,1,0,1,1],
    [-1,0,0,0,0,0,0,1],
    [1,1,0,0,0,1,0,1],
    [1,0,0,1,0,0,0,1],
    [1,0,1,0,0,1,0,0],
    [1,1,1,1,1,1,1,2]
]

#Para localizar la posicion de inicio en -1
posicion_inicial = None

for i in range(len(laberinto)):
    for j in range(len(laberinto[i])):
        if laberinto[i][j] == -1:
            posicion_inicial = [i,j]
            break
    if posicion_inicial:
        break

#Para Crear la ventana
root = tk.Tk()
root.title("Laberinto")

#Para Crear la etiqueta de posicion inicial
label = tk.Label(root, text=f"Jugador en: {posicion_inicial}")
label.pack()

#Funcion para los movimientos del jugador
def move(dx, dy):
    new_x = posicion_inicial[0] + dx
    new_y = posicion_inicial[1] + dy
    if 0 <= new_x < len(laberinto) and 0 <= new_y < len(laberinto[0]):
        celda = laberinto[new_x][new_y]
        if celda == 0:
            posicion_inicial[0], posicion_inicial[1] = new_x, new_y
            label.config(text=f"Jugador en: {posicion_inicial}")
        elif celda == 2:
            posicion_inicial[0], posicion_inicial[1] = new_x, new_y
            label.config(text=f"¡Meta!")       
        else:
            label.config(text="Pared")
    
    
#Botones para movimiento
tk.Button(root, text="Arriba", command=lambda: move(-1, 0)).pack()
tk.Button(root, text="Abajo", command=lambda: move(1, 0)).pack()
tk.Button(root, text="Izquierda", command=lambda: move(0, -1)).pack()
tk.Button(root, text="Derecha", command=lambda: move(0, 1)).pack()

#Ejecutar la interfaz
root.mainloop()


posicion_final = False



