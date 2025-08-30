# IMPORTS / LIBRARIES
import tkinter as tk
from tkinter import ttk

# CLASSES _________________________________________________________________________________________________________________________________
# BLOQUE
class bloque:
    def __init__(self, cuadro_2_canvas, cuadro_bloque, fila, columna, valor_bloque):
        self.cuadro_2_canvas = cuadro_2_canvas # cuadro de juego conteniendo todos los bloques; tipo canvaws de tkinter
        self.cuadro_bloque = cuadro_bloque # informacion sobre el cuadro de bloque que se crea para cada celda del laberinto
        self.fila = fila
        self.columna = columna
        self.valor_bloque = valor_bloque  # -1: inicio, 0: camino abierto, 1: pared, 2: meta
        self.visitado = False # para modificar el bloque al ser visitado durante el juego

    def set_color(self, color, valor): # metodo para cambiar el valor y color del widget
        self.cuadro_2_canvas.itemconfigure(self.cuadro_bloque, fill=color)

    def get_color(self): # metodo para obtener el color del
        if self.value == 1:
            return "brown"  # Pared
        elif self.value == 2:
            return "yellow" # Final
        elif self.value == -1:
            return "green"  # Inicio
        else:
            return "white" # Camino
    



#######
# VARIABLES GLOBALES ______________________________________________________________________________________________________________________
configuraciones_de_juego = {"tipo_partida":None, "tiempo":None, "dificultad":None, "dimensiones":None}
ranking_en_memoria = []
laberinto_en_memoria = []
matriz_canvas = []

# OBJETOS / CLASES ________________________________________________________________________________________________________________________
class bloque:
    def __init__(self, celda):
        pass


# FUNCIONES _______________________________________________________________________________________________________________________________
# CARGAR LABERINTO ------------------------------------------------------------------------------------------------------------------------
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

# CARGAR RANKING --------------------------------------------------------------------------------------------------------------------------
# E: Ruta al archivo de texto que contiene el ranking guardado
# S: Devuelve una matriz que representa el ranking
# R: El archivo debe existir
def cargar_rankings(ruta):
    rankings = []
    with open(ruta, 'r') as archivo: 
        for linea in archivo:
            linea = linea.strip()
            if linea.startswith('#'):
                continue
            if linea == '':
                continue
            fila = [valor for valor in linea.split(',')]
            rankings+=[fila]            
    return rankings


# GUARDAR CONFIGURACIONES -----------------------------------------------------------------------------------------------------------------
# E: no tiene entradas; la funcion se encarga de guardar las selecciones del usuario en la variable global 'configuraciones_de_juego'
# S: no tiene salidas; el resultado de invocar la funcion es modificar la variable global donde se guardan las configuraciones de juego antes de comenzar
# R: TBD
def guardar_configuraciones():
    global configuraciones_de_juego
    global laberinto_en_memoria
    configuraciones_de_juego["tipo_partida"] = combo_partida.get()
    if combo_partida.get() == "Contra Tiempo":
        configuraciones_de_juego["tiempo"] = combo_tiempo.get()
    configuraciones_de_juego["dificultad"] = combo_dificultad.get()
    configuraciones_de_juego["dimensiones"] = combo_dimensiones.get()
    print("las siguientes configuraciones fueron cargadas:")
    print(configuraciones_de_juego)
    # cargar laberinto
    laberinto_en_memoria = cargar_laberinto(f"archivos/laberintos/{configuraciones_de_juego['dificultad']}/{configuraciones_de_juego['dimensiones']}.txt")
    # paso de valores al area de juego1
    modo_seleccionado.set(configuraciones_de_juego["tipo_partida"])
    dificultad_seleccionada.set(configuraciones_de_juego["dificultad"])
    dimensiones_seleccionadas.set(configuraciones_de_juego["dimensiones"])
    print("valores area 1 modificados")
    visualizar_laberinto(laberinto_en_memoria)
    print("laberinto cargado en la ventana")

# DIMENSIONES_DINAMICAS -------------------------------------------------------------------------------------------------------------------
# E: esta funcion se suple de un evento creado a la hora de seleccionar una opcion en el combobox de 'dificultad'
# S: no tiene salidas; el proposito de esta funcion es cambiar los valores disponibles en el combobox de 'dimensiones' en base a la dificultad seleccionada
# R: no tiene restricciones; es una funcion de uso estrictamente para el GUI
def dimensiones_dinamicas(evento):
    global dimension_opciones
    dificultad_seleccionada = combo_dificultad.get()
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

# TIEMPO_PARTIDA_DINAMICO -----------------------------------------------------------------------------------------------------------------
# E: esta funcion se suple de un evento creado a la hora de seleccionar una opcion en el combobox de 'partida'
# S: no tiene salidas; el proposito de esta funcion es mostrar en pantalla la etiqueta y el combobox para la seleccion del tiempo de partida en caso de que el modo de partida seleccionado sea 'Contra Tiempo'
# R: no tiene restricciones; esta funcion es de uso estrictamente para el GUI
def tiempo_partida_dinamico(evento):
    selected_type = combo_partida.get()
    if selected_type == "Contra Tiempo":
        # Place the widgets in the correct row
        etiqueta_tiempo.grid(row=3, column=0, sticky='w')
        combo_tiempo.grid(row=4, column=0, pady=(0, 5), sticky='nsew')
        combo_tiempo.set(2)
    else:
        etiqueta_tiempo.grid_forget()
        combo_tiempo.grid_forget()

# CALCULAR CELDA --------------------------------------------------------------------------------------------------------------------------
# E: toma un strign representativo del tamaño de la cuadricula / laberinto
# S: retorna el tamaño que debe tener cada celda para que se pueda crear un laberinto de todas las dimensiones en el mismo cuadro
# R: TBD
def calcular_celda(dimension):
    numbers = dimension.split('x')
    tamaño_celda = min(cuadro_juego2.winfo_width() // int(numbers[0]), cuadro_juego2.winfo_height() // int(numbers[1]))
    return tamaño_celda

# LIMPIAR CUADRO JUEGO 2 ------------------------------------------------------------------------------------------------------------------
# E: no tiene entradas; la funcion trabaja sobre los objetos (widgets) en el cuadro de juego donde se muestra el laberinto
# S: no tiene salidas; el proposito de la funcion es limpiar el cuadro donde se muestra el laberinto
# R: no tiene restricciones
def limpiar_laberinto():
    for objeto in cuadro_juego2.winfo_children():
        objeto.destroy()

# VISUALIZAR LABERINTO --------------------------------------------------------------------------------------------------------------------
# E:
# S:
# R:
def visualizar_laberinto(matriz):
    # Limpia el cuadro de juego antes de dibujar un nuevo laberinto
    limpiar_laberinto()
    # Obtener las dimensiones actuales del cuadro de juego 2
    ancho_cuadro = cuadro_juego2.winfo_width()
    alto_cuadro = cuadro_juego2.winfo_height()
    # Si las dimensiones son 1 (valor por defecto antes de ser dibujado), espera y vuelve a intentar.
    if ancho_cuadro <= 1 or alto_cuadro <= 1:
        cuadro_juego2.after(10, lambda: visualizar_laberinto(matriz))
        return
    # Calcular el tamaño de la celda para que el laberinto se ajuste
    dimension_str = configuraciones_de_juego["dimensiones"]
    filas = int(dimension_str.split('x')[0])
    columnas = int(dimension_str.split('x')[1])
    # Calcula el tamaño de celda para que encaje
    tamaño_celda = min(ancho_cuadro // columnas, alto_cuadro // filas)
    # crear canvas con el tamaño del laberinto, centrado en el cuadro de juego 2
    celda = tk.Canvas(cuadro_juego2, width=columnas * tamaño_celda, height=filas * tamaño_celda, bg="lightgray", highlightthickness=0)
    celda.grid(row=0, column=0, sticky='nsew')
    # Coordenadas de inicio para centrar el canvas en el cuadro de juego 2
    offset_x = (ancho_cuadro - columnas * tamaño_celda) / 2
    offset_y = (alto_cuadro - filas * tamaño_celda) / 2
    for r in range(filas):
        for c in range(columnas):
            x1 = c * tamaño_celda + offset_x
            y1 = r * tamaño_celda + offset_y
            x2 = x1 + tamaño_celda
            y2 = y1 + tamaño_celda
            
            color = "white"  # Default
            if matriz[r][c] == 1:
                color = "brown"  # Pared
            elif matriz[r][c] == -1:
                color = "green"  # Inicio
            elif matriz[r][c] == 2:
                color = "yellow" # Final
            
            celda.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
            print(celda.winfo_id())
            
    # Usa `update_idletasks` para forzar el redibujado
    ventana_principal.update_idletasks()

# INICIAR PARTIDA -------------------------------------------------------------------------------------------------------------------------
# E: 
# S: 
# R: 
def iniciar_partida():
    cuadro_juego2.bind('<Configure>', lambda event: visualizar_laberinto(laberinto_en_memoria))


# CODIGO DE INTERFAZ GRAFICA ______________________________________________________________________________________________________________
# CONFIGURACION DE VENTANA PRINCIPAL ------------------------------------------------------------------------------------------------------
ventana_principal = tk.Tk()
ventana_principal.title("Laberinto")
ventana_principal.geometry("1000x800")
ventana_principal.resizable(False, False) # ventana de tamano inmutable
ventana_principal.columnconfigure(0, weight=3) # 10% for the menu
ventana_principal.columnconfigure(1, weight=7) # 90% for the main game area
ventana_principal.rowconfigure(0, weight=1) # la unica fila de la columna 0 cubre todo el espacio vertical

# estilo para todos los botones
estilo_default_botones = ttk.Style()
estilo_default_botones.configure('estilo_custom.TButton', font=('Courier', 14, 'bold'))

# CUADRO | CONTENEDOR DE AREA DE JUEGO ----------------------------------------------------------------------------------------------------
# un cuadro para contener los 2 cuadros que se van a incluir
container_juego = ttk.Frame(ventana_principal)
container_juego.grid(row=0, column=1, sticky='nsew')
container_juego.columnconfigure(0, weight=1) # La unica columna del area de juego general se extiende a lo largo
container_juego.rowconfigure(0, weight=0)
container_juego.rowconfigure(1, weight=1)

# CUADRO | AREA DE JUEGO 1 ----------------------------------------------------------------------------------------------------------------
# un cuadro para contener las estadisticas de la partida
cuadro_juego1 = ttk.Frame(container_juego, padding=15)
cuadro_juego1.grid(row=0, column=0, sticky='nsew')
cuadro_juego1.rowconfigure(0, weight=0)
cuadro_juego1.rowconfigure(1, weight=0)
cuadro_juego1.rowconfigure(2, weight=0)
cuadro_juego1.columnconfigure(0, weight=1)
cuadro_juego1.columnconfigure(1, weight=1)
cuadro_juego1.columnconfigure(2, weight=1)
cuadro_juego1.columnconfigure(3, weight=1)

# variable para actualizar el modo de juego seleccionado y mostrarlo en el area de juego
modo_seleccionado = tk.StringVar()
# etiqueta para mostrar el modo de juego seleccionado
etiqueta_modo_area1 = ttk.Label(cuadro_juego1, text=f"Modo:", font=("Courier", 16, "bold"))
etiqueta_modo_area1.grid(column=0, row=0, sticky='nsew')
# etiqueta para mostrar el valor del modo de juego seleccionado
etiqueta_modo_valor = ttk.Label(cuadro_juego1, textvariable=modo_seleccionado, font=("Courier", 14,))
etiqueta_modo_valor.grid(column=1, row=0, sticky='nsew')

# variable para actualizar la dificultad de juego seleccionada y mostrarla en el area de juego
dificultad_seleccionada = tk.StringVar()
# etiqueta para mostrar la dificultad de juego seleccionado
etiqueta_dificultad_area1 = ttk.Label(cuadro_juego1, text=f"Dificultad:", font=("Courier", 16, "bold"))
etiqueta_dificultad_area1.grid(column=0, row=1, sticky='nsew')
# etiqueta para mostrar el valor de la dificultad de juego seleccionado
etiqueta_dificultad_valor = ttk.Label(cuadro_juego1, textvariable=dificultad_seleccionada, font=("Courier", 14,))
etiqueta_dificultad_valor.grid(column=1, row=1, sticky='nsew')

# variable para actualizar el tamaño del laberinto y mostrarla en el area de juego
dimensiones_seleccionadas = tk.StringVar()
# etiqueta para mostrar el tamaño del laberinto seleccionado
etiqueta_dimension_area1 = ttk.Label(cuadro_juego1, text=f"Dimensiones:", font=("Courier", 16, "bold"))
etiqueta_dimension_area1.grid(column=2, row=0, sticky='nsew')
# etiqueta para mostrar el valor del tamaño del laberinto seleccionado
etiqueta_dimension_valor = ttk.Label(cuadro_juego1, textvariable=dimensiones_seleccionadas, font=("Courier", 14,))
etiqueta_dimension_valor.grid(column=3, row=0, sticky='nsew')

# variable para actualizar el tiempo de juego y mostrarlo en el area de juego
contador_tiempo = tk.IntVar()
# etiqueta para mostrar el tiempo de juego seleccionado
etiqueta_tiempo_area1 = ttk.Label(cuadro_juego1, text=f"Tiempo:", font=("Courier", 16, "bold"))
etiqueta_tiempo_area1.grid(column=2, row=1, sticky='nsew')
# etiqueta para mostrar el valor del tiempo de juego seleccionado
etiqueta_dimension_valor = ttk.Label(cuadro_juego1, textvariable=contador_tiempo, font=("Courier", 14,))
etiqueta_dimension_valor.grid(column=3, row=1, sticky='nsew')

# boton para comenzar la partida
boton_iniciar_partida = ttk.Button(cuadro_juego1, text="Iniciar", command=iniciar_partida, style='estilo_custom.TButton')
boton_iniciar_partida.grid(column=0, row=2, sticky='nsew')

# boton para abandonar la partida
boton_abandonar_partida = ttk.Button(cuadro_juego1, text="Reiniciar", command=None, style='estilo_custom.TButton')
boton_abandonar_partida.grid(column=1, row=2, sticky='nsew')

# boton para autocompletar el laberinto
boton_auto_completar = ttk.Button(cuadro_juego1, text="Auto completar", command=None, style='estilo_custom.TButton')
boton_auto_completar.grid(column=2, row=2, sticky='nsew')

# boton para autocompletar el laberinto
boton_auto_completar = ttk.Button(cuadro_juego1, text="Abandonar", command=None, style='estilo_custom.TButton')
boton_auto_completar.grid(column=3, row=2, sticky='nsew')

# CUADRO | AREA DE JUEGO 2 ----------------------------------------------------------------------------------------------------------------
# un cuadro para contener el laberinto
cuadro_juego2 = ttk.Frame(container_juego, relief="sunken")
cuadro_juego2.grid(column=0, row=1, sticky='nsew')
cuadro_juego2.columnconfigure(0, weight=1) 

# CUADRO | MENU DE JUEGO ------------------------------------------------------------------------------------------------------------------
cuadro_menu = ttk.Frame(ventana_principal, padding=15, relief="raised")
cuadro_menu.grid(row=0, column=0, sticky='nsew')
cuadro_menu.columnconfigure(0, weight=1)

# etiqueta menu
menu = ttk.Label(cuadro_menu, text="Menu", font=("Courier", 20, "bold"))
menu.grid(row=0, column=0, pady=(0, 15))

# etiqueta tipo de partida
etiqueta_modo_juego = ttk.Label(cuadro_menu, text="Modo de Juego", font=("Courier", 14, "bold", "italic"))
etiqueta_modo_juego.grid(row=1, column=0, sticky='w')
# combobox para seleccionar el tipo de partida
combo_partida = ttk.Combobox(cuadro_menu, values=["Normal", "Contra Tiempo"])
combo_partida.grid(row=2, column=0, sticky='nsew', pady=(0, 5))
combo_partida.set("Normal")
combo_partida.bind("<<ComboboxSelected>>", tiempo_partida_dinamico)

# etiqueta tiempo de partida
etiqueta_tiempo = ttk.Label(cuadro_menu, text="Minutos de Juego", font=("Courier", 14, "bold", "italic"))
combo_tiempo = ttk.Combobox(cuadro_menu, values=[2,5,7])

# etiqueta dificultad
etiqueta_dificultad = ttk.Label(cuadro_menu, text="Dificultad", font=("Courier", 14, "bold", "italic"))
etiqueta_dificultad.grid(row=5, column=0, sticky='w')
# combobx para seleccionar la dificultad
combo_dificultad = ttk.Combobox(cuadro_menu, values=["Fácil", "Medio", "Difícil"])
combo_dificultad.grid(row=6, column=0, sticky='nsew', pady=(0, 5))
combo_dificultad.set("Fácil")
combo_dificultad.bind("<<ComboboxSelected>>", dimensiones_dinamicas)

# etiqueta dimesiones
etiqueta_dimensiones = ttk.Label(cuadro_menu, text="Dimensiones", font=("Courier", 14, "bold", "italic"))
etiqueta_dimensiones.grid(row=7, column=0, sticky='w', pady=(0, 0))
# combobox para seleccionar las dimensiones en base a la dificultad
combo_dimensiones = ttk.Combobox(cuadro_menu)

combo_dimensiones.grid(row=8, column=0, sticky='nsew', pady=(0, 5))

# boton para guardar las configuraciones
boton_guardar_juego = ttk.Button(cuadro_menu, text="Guardar Configuracion", command=guardar_configuraciones, style='estilo_custom.TButton')
boton_guardar_juego.grid(row=9, column=0, sticky='nsew', pady=(10, 10))

# etiqueta ranking
etiqueta_ranking = ttk.Label(cuadro_menu, text="Ranking", font=("Courier", 20, "bold"))
etiqueta_ranking.grid(row=10, column=0, pady=(25, 5))

# treeview para mostrar el ranking actual
ranking = ttk.Treeview(cuadro_menu, columns=("Tiempo", "Nombre", "Tamaño", "Pasos"), show="headings")
ranking.grid(row=11, column=0, pady=(0, 5), sticky='nsew')
ranking.heading("Tiempo", text="Tiempo", anchor=tk.W)
ranking.heading("Nombre", text="Nombre", anchor=tk.W)
ranking.heading("Tamaño", text="Tamaño", anchor=tk.W)
ranking.heading("Pasos", text="Pasos", anchor=tk.W)
ranking.column("Tiempo", width=60, anchor=tk.W)
ranking.column("Nombre", width=60, anchor=tk.W)
ranking.column("Tamaño", width=60, anchor=tk.W)
ranking.column("Pasos", width=60, anchor=tk.W)

dimensiones_dinamicas(None)
guardar_configuraciones()
# visualizar_laberinto(laberinto_en_memoria)
ranking_en_memoria = cargar_rankings("archivos/rankings.txt")
ventana_principal.mainloop()