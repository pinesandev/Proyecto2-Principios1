# IMPORTS / LIBRARIES
import tkinter as tk
from tkinter import ttk

# VARIABLES GLOBALES __________________________________________________________________________________________________
configuraciones_de_juego = {"tipo_partida":None, "tiempo":None, "dificultad":None, "dimensiones":None}
laberinto_cargado = []

# FUNCIONES ___________________________________________________________________________________________________________
# CARGAR LABERINTO
# E: Ruta al archivo de texto que contiene el laberinto seleccionada por el usuario en el UI
# S: Devuelve una matriz que representa el laberinto seleccionado
# R: El archivo debe existir
def cargar_laberinto(ruta): 
    laberinto = []
    with open(ruta, 'r') as archivo: # with abre y cierra el archivo automaticamente
        for linea in archivo:
            # Ignorar líneas que comienzan con '#' o espacio en blanco
            linea = linea.strip()
            if linea.startswith('#'):
                continue
            if linea == '': 
                continue
            fila = [int(celda) for celda in linea.strip().split(',')]
            laberinto.append(fila)
    return laberinto

# DIMENSIONES_DINAMICAS
# E: esta funcion se suple de un evento creado a la hora de seleccionar una opcion en el combobox de 'dificultad'
# S: no tiene salidas; el proposito de esta funcion es cambiar los valores disponibles en el combobox de 'dimensiones' en base a la dificultad seleccionada
# R: no tiene restricciones; es una funcion de uso estrictamente para el GUI
def dimensiones_dinamicas(evento):
    global dimension_opciones
    dificultad_seleccionada = dificultad_default.get()
    if dificultad_seleccionada == "Fácil":
        dimension_opciones = ["8x8", "9x9", "10x10"] # dimensiones faciles
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
# E: esta funcion se suple de un evento creado a la hora de seleccionar una opcion en el combobox de 'partida'
# S: no tiene salidas; el proposito de esta funcion es mostrar en pantalla la etiqueta y el combobox para la seleccion del tiempo de partida en caso de que el modo de partida seleccionado sea 'Contra Tiempo'
# R: no tiene restricciones; esta funcion es de uso estrictamente para el GUI
def tiempo_partida_dinamico(evento):
    selected_type = modo_partida_default.get()
    if selected_type == "Contra Tiempo":
        # Place the widgets in the correct row
        etiqueta_tiempo.grid(row=3, column=0, sticky='w')
        combo_tiempo.grid(row=4, column=0, pady=(0, 5), sticky='w')
    else:
        etiqueta_tiempo.grid_forget()
        combo_tiempo.grid_forget()
    
    # Check the selection and display widgets if needed
    
        
    return

# CALCULAR CELDA
# E: toma un strign representativo del tamaño de la cuadricula / laberinto
# S: retorna el tamaño que debe tener cada celda para que se pueda crear un laberinto de todas las dimensiones en el mismo cuadro
# R: TBD
def calcular_celda(dimension):
    numbers = dimension.split('x')
    tamaño_celda = min(cuadro_juego2.winfo_width() // int(numbers[0]), cuadro_juego2.winfo_height() // int(numbers[1]))
    return tamaño_celda

# LIMPIAR CUADRO JUEGO 2
def limpiar_laberinto():
    cuadro_juego2 = ttk.Frame(container_juego, padding=10, relief="sunken")
    cuadro_juego2.grid(row=1, column=0, sticky='nsew')
    cuadro_juego2.columnconfigure(0, weight=1) # Configure for internal widgets

# VISUALIZAR LABERINTO
# E:
# S:
# R:
def visualizar_laberinto(matriz):
    print(configuraciones_de_juego["dimensiones"])
    tamaño_celda = calcular_celda(configuraciones_de_juego["dimensiones"])
    print(tamaño_celda)
    filas = len(matriz)
    columnas = len(matriz[0])
    canvas = tk.Canvas(cuadro_juego2, width=columnas*tamaño_celda, height=filas*tamaño_celda, bg="red")
    for r in range(filas):
        for c in range(columnas):
            x1 = c * tamaño_celda
            y1 = r * tamaño_celda
            x2 = x1 + tamaño_celda
            y2 = y1 + tamaño_celda
            if matriz[r][c] == 1:
                color = "brown"
            elif matriz[r][c] == 0:
                color = "white"
            elif matriz[r][c] == -1:
                color = "green"
            elif matriz[r][c] == 2:
                color = "yellow"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
            canvas.pack()
            print (matriz[r][c], end=" ")
    input("waiting to")

# CLICK | Para pruebas boton 'guardar configuracion'
def click():
    global laberinto_cargado
    global configuraciones_de_juego
    print(configuraciones_de_juego)
    print("click")
    configuraciones_de_juego["tipo_partida"] = combo_partida.get()
    if combo_partida.get() == "Contra Tiempo":
        configuraciones_de_juego["tiempo"] = combo_tiempo.get()
    configuraciones_de_juego["dificultad"] = combo_dificultad.get()
    configuraciones_de_juego["dimensiones"] = combo_dimensiones.get()

    # cargar laberinto
    laberinto_cargado = cargar_laberinto(f"archivos/laberintos/{combo_dificultad.get()}/{combo_dimensiones.get()}.txt")
    print(laberinto_cargado)
    # limpiar_laberinto()
    visualizar_laberinto(laberinto_cargado)
    
    # paso de valores al area de juego1
    modo_seleccionado.set(configuraciones_de_juego["tipo_partida"])
    dificultad_seleccionada.set(configuraciones_de_juego["dificultad"])
    dimensiones_seleccionadas.set(configuraciones_de_juego["dimensiones"])
    # cambiar los valores de las variables default para todos los comboboxes
    # modo_partida_default.set("selección")
    # tiempo_partida_default.set("selección")
    # dificultad_default.set("selección")
    # dimension_default.set("selección")
    # # esconder los widgets de tiempo luego del reset
    # etiqueta_tiempo.grid_forget()
    # combo_tiempo.grid_forget()
    print("reset completado")
    print(configuraciones_de_juego)

    width = cuadro_juego2.winfo_width()
    height = cuadro_juego2.winfo_height()
    print(f"Canvas size: {width}x{height} pixels")

    calcular_celda(combo_dimensiones.get())


# CONFIGURACION DE VENTANA PRINCIPAL __________________________________________________________________________________
ventana_principal = tk.Tk()
ventana_principal.title("Laberinto")
ventana_principal.geometry("1000x750")
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
etiqueta_modo_juego = ttk.Label(cuadro_menu, text="Modo de Juego", font=("Courier", 14, "bold", "italic"))
etiqueta_modo_juego.grid(row=1, column=0, sticky='w', pady=(0, 0))
# variable string default para los combobox de seleccion de configuraciones
modo_partida_default = tk.StringVar()
modo_partida_default.set("selección")
# combobox para seleccionar el tipo de partida
combo_partida = ttk.Combobox(cuadro_menu, values=["Normal", "Contra Tiempo"], textvariable=modo_partida_default)
combo_partida.grid(row=2, column=0, sticky='w', pady=(0, 5))
combo_partida.bind("<<ComboboxSelected>>", tiempo_partida_dinamico)

# etiqueta tiempo de partida
etiqueta_tiempo = ttk.Label(cuadro_menu, text="Minutos de Juego", font=("Courier", 14, "bold", "italic"))
# variable string default para los combobox de seleccion de tiempo de partida
tiempo_partida_default = tk.StringVar()
tiempo_partida_default.set("selección")
# combobox tiempo de partida
opciones_tiempo = [2,5,7]
combo_tiempo = ttk.Combobox(cuadro_menu, values=opciones_tiempo, textvariable=tiempo_partida_default)
combo_tiempo.set(opciones_tiempo[0])

# etiqueta dificultad
etiqueta_dificultad = ttk.Label(cuadro_menu, text="Dificultad", font=("Courier", 14, "bold", "italic"))
etiqueta_dificultad.grid(row=5, column=0, sticky='w', pady=(0, 0))
# variable string default para los combobox de seleccion de dimensiones
dificultad_default = tk.StringVar()
dificultad_default.set("selección")
# combobx para seleccionar la dificultad
combo_dificultad = ttk.Combobox(cuadro_menu, values=["Fácil", "Medio", "Difícil"], textvariable=dificultad_default)
combo_dificultad.grid(row=6, column=0, sticky='w', pady=(0, 5))
combo_dificultad.bind("<<ComboboxSelected>>", dimensiones_dinamicas)

# etiqueta dimesiones
etiqueta_dimensiones = ttk.Label(cuadro_menu, text="Dimensiones", font=("Courier", 14, "bold", "italic"))
etiqueta_dimensiones.grid(row=7, column=0, sticky='w', pady=(0, 0))
# variable string default para los combobox de seleccion de dimensiones
dimension_default = tk.StringVar()
dimension_default.set("selección")
# combobox para seleccionar las dimensiones en base a la dificultad
combo_dimensiones = ttk.Combobox(cuadro_menu, textvariable=dimension_default)
combo_dimensiones.grid(row=8, column=0, sticky='w', pady=(0, 5))

# boton para guardar las configuraciones
boton_guardar_juego = ttk.Button(cuadro_menu, text="Guardar Configuracion", command=click)
boton_guardar_juego.grid(row=9, column=0, sticky='nsew', pady=(10, 10))

# etiqueta ranking
menu = ttk.Label(cuadro_menu, text="Ranking", font=("Courier", 20, "bold"))
menu.grid(row=10, column=0, pady=(25, 15))


# CUADRO | CONTENEDOR DE AREA DE JUEGO ________________________________________________________________________________
# un cuadro para contener los 2 cuadros que se van a incluir
container_juego = ttk.Frame(ventana_principal)
container_juego.grid(row=0, column=1, sticky='nsew')
container_juego.columnconfigure(0, weight=1) # La unica columna del area de juego general se extiende a lo largo
container_juego.rowconfigure(0, weight=1)
container_juego.rowconfigure(1, weight=9)


# CUADRO | AREA DE JUEGO 1 ____________________________________________________________________________________________
# Place this frame inside the new container.
cuadro_juego1 = ttk.Frame(container_juego)
cuadro_juego1.grid(row=0, column=0, sticky='nsew')

# variable para actualizar el modo de juego seleccionado y mostrarlo en el area de juego
modo_seleccionado = tk.StringVar()
# etiqueta para mostrar el modo de juego seleccionado
etiqueta_modo_area1 = ttk.Label(cuadro_juego1, text=f"Modalidad de Partida:", font=("Courier", 16, "bold"), padding=5)
etiqueta_modo_area1.grid(row=0, column=0, sticky='w')
# etiqueta para mostrar el valor del modo de juego seleccionado
etiqueta_modo_valor = ttk.Label(cuadro_juego1, textvariable=modo_seleccionado, font=("Courier", 14,), padding=5)
etiqueta_modo_valor.grid(row=0, column=1, sticky='w')

# variable para actualizar la dificultad de juego seleccionada y mostrarla en el area de juego
dificultad_seleccionada = tk.StringVar()
# etiqueta para mostrar el modo de juego seleccionado
etiqueta_dificultad_area1 = ttk.Label(cuadro_juego1, text=f"Dificultad de Partida:", font=("Courier", 16, "bold"), padding=5)
etiqueta_dificultad_area1.grid(row=1, column=0, sticky='w')
# etiqueta para mostrar el valor del modo de juego seleccionado
etiqueta_dificultad_valor = ttk.Label(cuadro_juego1, textvariable=dificultad_seleccionada, font=("Courier", 14,), padding=5)
etiqueta_dificultad_valor.grid(row=1, column=1, sticky='w')

# variable para actualizar la dificultad de juego seleccionada y mostrarla en el area de juego
dimensiones_seleccionadas = tk.StringVar()
# etiqueta para mostrar el modo de juego seleccionado
etiqueta_dimension_area1 = ttk.Label(cuadro_juego1, text=f"Tamaño del Laberinto:", font=("Courier", 16, "bold"), padding=5)
etiqueta_dimension_area1.grid(row=0, column=2, sticky='w')
# etiqueta para mostrar el valor del modo de juego seleccionado
etiqueta_dimension_valor = ttk.Label(cuadro_juego1, textvariable=dimensiones_seleccionadas, font=("Courier", 14,), padding=5)
etiqueta_dimension_valor.grid(row=0, column=3, sticky='w')

# variable para actualizar el tiempo de juego y mostrarlo en el area de juego
contador_tiempo = tk.IntVar()
# etiqueta para mostrar el modo de juego seleccionado
etiqueta_tiempo_area1 = ttk.Label(cuadro_juego1, text=f"Tiempo de Juego:", font=("Courier", 16, "bold"), padding=5)
etiqueta_tiempo_area1.grid(row=1, column=2, sticky='w')
# etiqueta para mostrar el valor del modo de juego seleccionado
etiqueta_dimension_valor = ttk.Label(cuadro_juego1, textvariable=contador_tiempo, font=("Courier", 14,), padding=5)
etiqueta_dimension_valor.grid(row=1, column=3, sticky='w')


# CUADRO | AREA DE JUEGO 2 ____________________________________________________________________________________________
# Place this frame inside the new container.
cuadro_juego2 = ttk.Frame(container_juego, padding=10, relief="sunken")
cuadro_juego2.grid(row=1, column=0, sticky='nsew')
cuadro_juego2.columnconfigure(0, weight=1) # Configure for internal widgets

ventana_principal.mainloop()