# IMPORTS / LIBRARIES
import tkinter as tk
from tkinter import ttk

# VARIABLES GLOBALES __________________________________________________________________________________________________
configuraciones_de_juego = {"tipo_partida":None, "tiempo":None, "dificultad":None, "dimensiones":None}

# FUNCIONES ___________________________________________________________________________________________________________
# CLICK
def click():
    global configuraciones_de_juego
    print(configuraciones_de_juego)
    print("click")
    print(combo_partida.get())
    configuraciones_de_juego["tipo_partida"] = combo_partida.get()
    if combo_partida.get() == "Contra Tiempo":
        print(combo_tiempo.get())
        configuraciones_de_juego["tiempo"] = combo_tiempo.get()
    print(combo_dificultad.get())
    configuraciones_de_juego["dificultad"] = combo_dificultad.get()
    print(combo_dimensiones.get())
    configuraciones_de_juego["dimensiones"] = combo_dimensiones.get()
    print(configuraciones_de_juego)


# DIMENSIONES_DINAMICAS
# E: estaa funcion se suple por un evento creado a la hora de seleccionar una opcion en el combobox de 'dificultad'
# S: no tiene salidas; el proposito de esta funcion es cambiar los valores disponibles en el combobox de 'dimensiones' en base a la dificultad seleccionada
# R: no tiene restricciones; es una funcion de uso estrictamente interno
def dimensiones_dinamicas(evento):
    global dimension_opciones
    dificultad_seleccionada = dificultad_default.get()
    if dificultad_seleccionada == "Fácil":
        dimension_opciones = ["8x8", "9x9", "10x0"] # dimensiones faciles
    elif dificultad_seleccionada == "Medio":
        dimension_opciones = ["11x11", "12x12", "13x13"] # dimensiones medias
    elif dificultad_seleccionada == "Difícil":
        dimension_opciones = ["14x14", "15x15", "16x16"] # dimensiones dificiles
    else:
        dimension_opciones = ["selección"] # seleccion default
    # se asignan los valores en base a las condicionales
    combo_dimensiones["values"] = dimension_opciones
    combo_dimensiones.set(dimension_opciones[0])


# TIEMPO_PARTIDA_DINAMICO
# E: 
# S: 
# R: 
def tiempo_partida_dinamico(evento):
    selected_type = tipo_partida_default.get()
    
    # Hide all additional widgets initially
    etiqueta_tiempo.grid_forget()
    combo_tiempo.grid_forget()
    
    # Check the selection and display widgets if needed
    if selected_type == "Contra Tiempo":
        # Place the widgets in the correct row
        etiqueta_tiempo.grid(row=3, column=0, sticky='w')
        combo_tiempo.grid(row=4, column=0, pady=0, sticky='w')
        
    return


# CONFIGURACION DE VENTANA PRINCIPAL __________________________________________________________________________________
ventana_principal = tk.Tk()
ventana_principal.title("Laberinto")
ventana_principal.geometry("1000x600")
ventana_principal.resizable(False, False) # ventana de tamano inmutable
ventana_principal.columnconfigure(0, weight=1) # 10% for the menu
ventana_principal.columnconfigure(1, weight=9) # 90% for the main game area
ventana_principal.rowconfigure(0, weight=1) # la unica fila de la columna 0 cubre todo el espacio vertical


# CUADRO | MENU DE JUEGO ______________________________________________________________________________________________
cuadro_menu = ttk.Frame(ventana_principal, padding=15, relief="raised")
cuadro_menu.grid(row=0, column=0, sticky='nsew')
cuadro_menu.columnconfigure(0, weight=1)

# WIDGETS | MENU
# etiqueta menu
menu = ttk.Label(cuadro_menu, text="Menu", font=("Courier", 20, "bold"))
menu.grid(row=0, column=0, pady=(0, 15))

# etiqueta tipo de partida
etiqueta_tipo_partida = ttk.Label(cuadro_menu, text="Tipo de Partida", font=("Courier", 14, "bold"))
etiqueta_tipo_partida.grid(row=1, column=0, sticky='w')

# variable string default para los combobox de seleccion de configuraciones
tipo_partida_default = tk.StringVar()
tipo_partida_default.set("selección")
# combobox para seleccionar el tipo de partida
combo_partida = ttk.Combobox(cuadro_menu, values=["Normal", "Contra Tiempo"], textvariable=tipo_partida_default)
combo_partida.grid(row=2, column=0, pady=0, sticky='w')
combo_partida.bind("<<ComboboxSelected>>", tiempo_partida_dinamico)

# etiqueta tiempo de partida
etiqueta_tiempo = ttk.Label(cuadro_menu, text="Tiempo de Juego", font=("Courier", 14, "bold"))

# variable string default para los combobox de seleccion de tiempo de partida
tiempo_partida_default = tk.StringVar()
tiempo_partida_default.set("selección")
# combobox tiempo de partida
opciones_tiempo = [2,5,7]
combo_tiempo = ttk.Combobox(cuadro_menu, values=opciones_tiempo, textvariable=tiempo_partida_default)
combo_tiempo.set(opciones_tiempo[0])

# etiqueta dificultad
etiqueta_dificultad = ttk.Label(cuadro_menu, text="Dificultad", font=("Courier", 14, "bold"))
etiqueta_dificultad.grid(row=5, column=0, sticky='w')

# variable string default para los combobox de seleccion de dimensiones
dificultad_default = tk.StringVar()
dificultad_default.set("selección")
# combobx para seleccionar la dificultad
combo_dificultad = ttk.Combobox(cuadro_menu, values=["Fácil", "Medio", "Difícil"], textvariable=dificultad_default)
combo_dificultad.grid(row=6, column=0, pady=0, sticky='w')
combo_dificultad.bind("<<ComboboxSelected>>", dimensiones_dinamicas)

# etiqueta dimesiones
etiqueta_dimensiones = ttk.Label(cuadro_menu, text="Dimensiones", font=("Courier", 14, "bold"))
etiqueta_dimensiones.grid(row=7, column=0, sticky='w')

# variable string default para los combobox de seleccion de dimensiones
dimension_opciones = ["selección"]
# combobox para seleccionar las dimensiones en base a la dificultad
combo_dimensiones = ttk.Combobox(cuadro_menu)
combo_dimensiones.grid(row=8, column=0, pady=0, sticky='w')
combo_dimensiones.set(dimension_opciones[0])

# boton para guardar las configuraciones
boton_guardar_juego = ttk.Button(cuadro_menu, text="Guardar Configuracion", command=click)
boton_guardar_juego.grid(row=9, column=0, pady=0, sticky='w')


# CUADRO | CONTENEDOR DE AREA DE JUEGO ________________________________________________________________________________
container_juego = ttk.Frame(ventana_principal)
container_juego.grid(row=0, column=1, sticky='nsew')
container_juego.columnconfigure(0, weight=1) # La unica columna del area de juego general se extiende a lo largo

# Configure this parent frame's rows for the vertical split.
# Row 0 will be 20% (weight=2) for the stats/config.
# Row 1 will be 80% (weight=8) for the game canvas.
container_juego.rowconfigure(0, weight=2)
container_juego.rowconfigure(1, weight=8)



# CUADRO | AREA DE JUEGO 1 ____________________________________________________________________________________________
# Place this frame inside the new container.
cuadro_juego1 = ttk.Frame(container_juego, relief="sunken")
cuadro_juego1.grid(row=0, column=0, sticky='nsew')
cuadro_juego1.columnconfigure(0, weight=1) # Configure for internal widgets

ttk.Label(cuadro_juego1, text="Área de Juego", font=("Courier", 16, "bold")).grid(row=0, column=0, pady=10)



# CUADRO | AREA DE JUEGO 2 ____________________________________________________________________________________________
# Place this frame inside the new container.
cuadro_juego2 = ttk.Frame(container_juego, padding=10, relief="sunken")
cuadro_juego2.grid(row=1, column=0, sticky='nsew')
cuadro_juego2.columnconfigure(0, weight=1) # Configure for internal widgets

# Placeholder for the maze display
maze_canvas = tk.Canvas(cuadro_juego2, bg="white", highlightthickness=1, highlightbackground="black")
maze_canvas.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
cuadro_juego2.rowconfigure(0, weight=1) # The canvas takes up all available vertical space

ventana_principal.mainloop()