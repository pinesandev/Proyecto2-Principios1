# IMPORTS / LIBRARIES
import tkinter as tk
from tkinter import ttk
import time # utilizado para utilizar la funcion sleep()
from datetime import datetime # para manejar todos los tiempos del programa
import threading # para crear un proceso / thread  para el cronometro

# CLASSES _________________________________________________________________________________________________________________________________
# CRONOMETRO ------------------------------------------------------------------------------------------------------------------------------
class cronometro:
    def __init__(self, tipo_crono, partida):
        self.partida = partida
        self.segundos_totales = partida.contador_tiempo.get()
        self.tipo_crono = tipo_crono
        self.corriendo = False # almacena el estado del cronometro para controlar los procesos
        self.proceso = None # se guarda el proceso / thread que comienza al inicializar el cronometro
        

    # *** FUNCIONES DE CLASE ***
    def iniciar(self):
        # validar que el cronometro no esta corriendo; corriendo == False
        if self.corriendo == False:
            if self.tipo_crono == "regresivo":
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} INFO: cronometro {self.tipo_crono} inicializado")
                self.corriendo = True
                self.tiempo_inicio = datetime.now()
                self.proceso = threading.Thread(target=self.runtime, daemon=True)
                self.proceso.start()
            else:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} INFO: cronometro {self.tipo_crono} inicializado")
                self.corriendo = True
                self.tiempo_inicio = datetime.now()
                self.proceso = threading.Thread(target=self.runtime, daemon=True)
                self.proceso.start()

    
    def runtime(self):
        while self.corriendo == True:
            time.sleep(1)
            if self.tipo_crono == "progresivo" and self.corriendo:
                self.segundos_totales += 1
                self.partida.contador_tiempo.set(self.segundos_totales)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CRONO: tiempo transcurrido {self.segundos_totales} s")
            elif self.tipo_crono == "regresivo" and self.corriendo:
                self.segundos_totales -= 1
                self.partida.contador_tiempo.set(self.segundos_totales)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CRONO: tiempo transcurrido {self.segundos_totales} s")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CRONO: cronometro detenido")

    def detener(self):
        self.corriendo = False # cambia el estado del cronometro para que el ciclo del runtime termine

            
# CLASE BLOQUE ----------------------------------------------------------------------------------------------------------------------------
class bloque:
    def __init__(self, cuadro_2_canvas, cuadro_bloque, fila, columna, valor_bloque):
        self.cuadro_2_canvas = cuadro_2_canvas # cuadro de juego conteniendo todos los bloques; tipo canvas de tkinter
        self.cuadro_bloque = cuadro_bloque # informacion sobre el cuadro de bloque que se crea para cada celda del laberinto
        self.fila = fila
        self.columna = columna
        self.valor_bloque = valor_bloque  # -1: inicio, 0: camino abierto, 1: pared, 2: meta
        self.visitado = False # para modificar el bloque al ser visitado durante el juego

    # *** FUNCIONES DE CLASE ***
    # SET COLOR ---------------------------------------------------------------------------------------------------------------------------
    # E: tiene como entrada el valor del color que se va a establecer o cambiar en el bloque
    # S: no tiene salidas; la funcion se encarga de cambiar el color del bloque
    # R: el color tiene que ser de tipo string y un color valido para tkinter e .itemconfigure()
    def set_color(self, color): # metodo para cambiar el valor y color del widget
        self.cuadro_2_canvas.itemconfigure(self.cuadro_bloque, fill=color)

    # GET COLOR ---------------------------------------------------------------------------------------------------------------------------
    # E: no tiene entradas
    # S: retorna el color que debe tener el bloque en base a su valor (-1, 0, 1, 2)
    # R: no tiene restricciones
    def get_color(self): # metodo para obtener el color del
        if self.valor_bloque== 1:
            return "brown"  # Pared
        elif self.valor_bloque == 2:
            return "yellow" # Final
        elif self.valor_bloque == -1:
            return "green"  # Inicio
        else:
            return "white" # Camino   

# CLASE PARTIDA ---------------------------------------------------------------------------------------------------------------------------
class partida:
    def __init__(self, ventana_root):
        self.ventana_root = ventana_root

        # configuraciones de la ventana principal
        self.ventana_root.title("Laberinto")
        self.ventana_root.geometry("980x750")
        self.ventana_root.columnconfigure(0, weight=3, minsize=250)
        self.ventana_root.columnconfigure(1, weight=7)
        self.ventana_root.rowconfigure(0, weight=1)

        # configuraciones y variables de juego
        self.partida_iniciada = False
        self.movimientos_partida = 0
        self.configuraciones_de_juego = {"tipo_partida": "Normal", "tiempo": None, "dificultad": "Fácil", "dimensiones": "8x8"}
        self.ranking_en_memoria = []
        self.laberinto_en_memoria = []
        self.bloque_matriz = [] # guardar una matriz de todos los objetos tipo bloque se que crean para cada laberinto
        self.posicion_actual_totem = None # almacena la posicion del totem en el laberinto
        self.modo_seleccionado = tk.StringVar(value=self.configuraciones_de_juego["tipo_partida"])
        self.dificultad_seleccionada = tk.StringVar(value=self.configuraciones_de_juego["dificultad"])
        self.dimensiones_seleccionadas = tk.StringVar(value=self.configuraciones_de_juego["dimensiones"])
        self.contador_tiempo = tk.IntVar(value=self.configuraciones_de_juego["tiempo"])
        self.instancia_cronometro = None # guarda el cronometro inicializado en la partida

        # estilo customizado para los botones
        self.estilo_default_botones = ttk.Style()
        self.estilo_default_botones.configure('estilo_custom.TButton', font=('Courier', 14, 'bold'))
        
        # *** CUADRO VENTANA DE JUEGO *** cuadro donde se van a contener ambos areas de juego
        self.ventana_juego = ttk.Frame(ventana_root)
        self.ventana_juego.grid(row=0, column=1, sticky='nsew')
        self.ventana_juego.columnconfigure(0, weight=1)
        self.ventana_juego.rowconfigure(0, weight=0)
        self.ventana_juego.rowconfigure(1, weight=1)

        # *** CUADRO AREA DE JUEGO 1 ***
        self.cuadro_juego1 = ttk.Frame(self.ventana_juego, padding=15)
        self.cuadro_juego1.grid(row=0, column=0, sticky='nsew')
        self.cuadro_juego1.columnconfigure((0, 1, 2, 3), weight=1)
        
        # *** WIDGETS | CUADRO AREA DE JUEGO 1 ***
        # las etiquetas estaticas se presentan en "bold" en el area de juego 1
        # las etiquetas mutables cambian en base a la seleccion de configuraciones en el menu del usuario cuando se guardan las configuraciones
        ttk.Label(self.cuadro_juego1, text="Modo:", font=("Courier", 16, "bold")).grid(column=0, row=0, sticky='w') # etiqueta estatica de modo
        ttk.Label(self.cuadro_juego1, textvariable=self.modo_seleccionado, font=("Courier", 14,)).grid(column=1, row=0, sticky='w') # etiqueta mutable de modo
        ttk.Label(self.cuadro_juego1, text="Dificultad:", font=("Courier", 16, "bold")).grid(column=0, row=1, sticky='w') # etiqueta estatica de dificultad
        ttk.Label(self.cuadro_juego1, textvariable=self.dificultad_seleccionada, font=("Courier", 14,)).grid(column=1, row=1, sticky='w') # etiqueta mutable de dificultad
        ttk.Label(self.cuadro_juego1, text="Dimensiones:", font=("Courier", 16, "bold")).grid(column=2, row=0, sticky='w') # etiqueta estatica de dimensiones
        ttk.Label(self.cuadro_juego1, textvariable=self.dimensiones_seleccionadas, font=("Courier", 14,)).grid(column=3, row=0, sticky='w') # etiqueta mutable de dimeniones
        ttk.Label(self.cuadro_juego1, text="Tiempo:", font=("Courier", 16, "bold")).grid(column=2, row=1, sticky='w') # etiqueta estatica de tiempo
        ttk.Label(self.cuadro_juego1, textvariable=self.contador_tiempo, font=("Courier", 14,)).grid(column=3, row=1, sticky='w') # etiqueta mutable de tiempo

        # botones del area de juego 1 para controlar el funcionamiento de la patida
        ttk.Button(self.cuadro_juego1, text="Iniciar", command=self.iniciar_partida, style='estilo_custom.TButton').grid(column=0, row=2, sticky='nsew')
        ttk.Button(self.cuadro_juego1, text="Reiniciar", command=self.reiniciar_partida, style='estilo_custom.TButton').grid(column=1, row=2, sticky='nsew')
        ttk.Button(self.cuadro_juego1, text="Auto completar", command=self.autocompletar_laberinto, style='estilo_custom.TButton').grid(column=2, row=2, sticky='nsew')
        ttk.Button(self.cuadro_juego1, text="Abandonar", command=self.abandonar_partida, style='estilo_custom.TButton').grid(column=3, row=2, sticky='nsew')

        # *** CUADRO AREA DE JUEGO 2 ***
        self.cuadro_juego2 = ttk.Frame(self.ventana_juego, relief="sunken")
        self.cuadro_juego2.grid(column=0, row=1, sticky='nsew')
        self.cuadro_juego2.columnconfigure(0, weight=1)
        self.cuadro_juego2.rowconfigure(0, weight=1)

        self.canvas_laberinto = tk.Canvas(self.cuadro_juego2, bg="black", highlightthickness=0)
        self.canvas_laberinto.pack(fill="both", expand=True, anchor="center")

        # *** CUADRO MENU *** 
        self.cuadro_menu = ttk.Frame(ventana_root, padding=15, relief="raised")
        self.cuadro_menu.grid(row=0, column=0, sticky='nsew')
        self.cuadro_menu.columnconfigure(0, weight=1)

        # *** WIDGETS | CUADRO MENU *** 
        ttk.Label(self.cuadro_menu, text="Menu", font=("Courier", 20, "bold")).grid(row=0, column=0, pady=(0, 15))
        ttk.Label(self.cuadro_menu, text="Modo de Juego", font=("Courier", 14, "bold", "italic")).grid(row=1, column=0, sticky='w')
        self.combo_partida = ttk.Combobox(self.cuadro_menu, values=["Normal", "Contra Tiempo"])
        self.combo_partida.grid(row=2, column=0, sticky='nsew', pady=(0, 5))
        self.combo_partida.set("Normal")
        self.combo_partida.bind("<<ComboboxSelected>>", self.tiempo_partida_dinamico)
        self.etiqueta_tiempo = ttk.Label(self.cuadro_menu, text="Minutos de Juego", font=("Courier", 14, "bold", "italic"))
        self.combo_tiempo = ttk.Combobox(self.cuadro_menu, values=[2,5,7])
        ttk.Label(self.cuadro_menu, text="Dificultad", font=("Courier", 14, "bold", "italic")).grid(row=5, column=0, sticky='w')
        self.combo_dificultad = ttk.Combobox(self.cuadro_menu, values=["Fácil", "Medio", "Difícil"])
        self.combo_dificultad.grid(row=6, column=0, sticky='nsew', pady=(0, 5))
        self.combo_dificultad.set("Fácil")
        self.combo_dificultad.bind("<<ComboboxSelected>>", self.dimensiones_dinamicas)
        ttk.Label(self.cuadro_menu, text="Dimensiones", font=("Courier", 14, "bold", "italic")).grid(row=7, column=0, sticky='w', pady=(0, 0))
        self.combo_dimensiones = ttk.Combobox(self.cuadro_menu)
        self.combo_dimensiones.grid(row=8, column=0, sticky='nsew', pady=(0, 5))
        ttk.Button(self.cuadro_menu, text="Guardar Configuracion", command=self.guardar_configuraciones, style='estilo_custom.TButton').grid(row=9, column=0, sticky='nsew', pady=(10, 10))
        # porcion del menu para mostrar el ranking
        ttk.Label(self.cuadro_menu, text="Ranking", font=("Courier", 20, "bold")).grid(row=10, column=0, pady=(25, 5))        
        self.ranking_treeview = ttk.Treeview(self.cuadro_menu, columns=("Tiempo", "Nombre", "Tamaño", "Pasos"), show="headings")
        self.ranking_treeview.grid(row=11, column=0, pady=(0, 5), sticky='nsew')
        self.ranking_treeview.heading("Tiempo", text="Tiempo", anchor=tk.W)
        self.ranking_treeview.heading("Nombre", text="Nombre", anchor=tk.W)
        self.ranking_treeview.heading("Tamaño", text="Tamaño", anchor=tk.W)
        self.ranking_treeview.heading("Pasos", text="Pasos", anchor=tk.W)
        self.ranking_treeview.column("Tiempo", width=60, anchor=tk.W)
        self.ranking_treeview.column("Nombre", width=60, anchor=tk.W)
        self.ranking_treeview.column("Tamaño", width=60, anchor=tk.W)
        self.ranking_treeview.column("Pasos", width=60, anchor=tk.W)

        # *** CARGAR DATOS INICIALES DE PARTIDA ***
        # se inicia el juego con datos por defecto; en este caso una aprtida de tipo normal con dimensiones 8x8
        self.dimensiones_dinamicas(None) # dimensiones dinamicas toma un evento como parametro; en este caso un cambio en el combobox de dificultad de partida
        self.guardar_configuraciones() # se cargan las confoguraciones en base a los valores por defecto de todos los comboboxes en el menu
        self.ranking_en_memoria = self.cargar_rankings("archivos/rankings.txt") # se cargan los rankings
        self.mostrar_ranking() # se carga el rakning en el treeview

        # *** VICULAR EVENTOS ***
        # se vinculan eventos como cambiar el tamaño de la pantalla y inputs del teclado con su respectiva funcion
        self.ventana_root.bind("<Key>", self.movimiento_teclas) ### VALIDAR PARA ACEPTAR INPUTS UNICAMENTE CUANDO SE INICIA LA PARTIDA

    # *** FUNCIONES DE CLASE ***
    # CARGAR LABERINTO --------------------------------------------------------------------------------------------------------------------
    # E: Ruta al archivo de texto que contiene el laberinto seleccionada por el usuario en el UI
    # S: Devuelve una matriz que representa el laberinto seleccionado
    # R: El archivo debe existir
    def cargar_laberinto(self, ruta):
            laberinto = []
            try:
                with open(ruta, 'r') as archivo:
                    for linea in archivo:
                        linea = linea.strip()
                        if linea.startswith('#') or linea == '':
                            continue
                        fila = [int(celda) for celda in linea.strip().split(',')]
                        laberinto.append(fila)
            except FileNotFoundError:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error: Archivo no encontrado en {ruta}")
                return None
            return laberinto

    # CARGAR RANKING ----------------------------------------------------------------------------------------------------------------------
    # E: Ruta al archivo de texto que contiene el ranking guardado
    # S: Devuelve una matriz que representa el ranking
    # R: El archivo debe existir
    def cargar_rankings(self, ruta):
            lista_ranking = []
            try:
                with open(ruta, 'r') as archivo: 
                    for linea in archivo:
                        linea = linea.strip()
                        if linea.startswith('#') or linea == '':
                            continue
                        fila = [valor for valor in linea.split(',')]
                        lista_ranking.append(fila)
            except FileNotFoundError:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} *** Error: Archivo de ranking no encontrado en {ruta} ***")
                return []
            return lista_ranking

    # MOSTRAR RANKING ---------------------------------------------------------------------------------------------------------------------
    # E: no tiene entradas
    # S: la funcion se encarga de limpiar los valores en el treeview donde se muestra el raking y cargarlos nuevamente
    # R: TBD
    def mostrar_ranking(self):
            for item in self.ranking_treeview.get_children(): # ciclo para limpiar el widget 'ranking_treeview'
                self.ranking_treeview.delete(item)
            
            for fila in self.ranking_en_memoria: # cargar datos nuevamente en el widget 'ranking_treeview'
                self.ranking_treeview.insert("", "end", values=fila)

    # GUARDAR CONFIGURACIONES -------------------------------------------------------------------------------------------------------------
    # E: no tiene entradas; la funcion se encarga de guardar las selecciones del usuario en la variable global 'configuraciones_de_juego'
    # S: no tiene salidas; el resultado de invocar la funcion es modificar la variable global donde se guardan las configuraciones de juego antes de comenzar
    # R: TBD
    def guardar_configuraciones(self):
        # guardar las configuraciones de juego seleccionadas en el menu dentro de un diccionario en el objeto tipo partida (configuraciones_de_juego)
        self.configuraciones_de_juego["tipo_partida"] = self.combo_partida.get()
        print(self.combo_tiempo.get())
        if self.combo_partida.get() == "Contra Tiempo":
            if self.combo_tiempo.get() == '2':
                print("dentro 2")
                self.configuraciones_de_juego["tiempo"] = 120 # contratiempo 2 minutos
                self.contador_tiempo.set(120)
            elif self.combo_tiempo.get() == '5':
                self.configuraciones_de_juego["tiempo"] = 300 # contratiempo 5 minutos
                self.contador_tiempo.set(300)
            elif self.combo_tiempo.get() == '7':
                self.configuraciones_de_juego["tiempo"] = 420 # contratiempo 7 minutos
                self.contador_tiempo.set(420)
        else:
            self.configuraciones_de_juego["tiempo"] = 0
            self.contador_tiempo.set(0)
        self.configuraciones_de_juego["dificultad"] = self.combo_dificultad.get()
        self.modo_seleccionado.set(self.configuraciones_de_juego["tipo_partida"])
        self.configuraciones_de_juego["dimensiones"] = self.combo_dimensiones.get()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Las siguientes configuraciones fueron cargadas:") # log en terminal que indica las configuraciones cargadas
        print(self.configuraciones_de_juego)
        
        # se crea ruta del laberinto en base a las configuraciones cargadas y se carga el laberinto con dicha ruta
        ruta_laberinto = f"archivos/laberintos/{self.configuraciones_de_juego['dificultad']}/{self.configuraciones_de_juego['dimensiones']}.txt"
        self.laberinto_en_memoria = self.cargar_laberinto(ruta_laberinto)
        
        # actualizar las variables que controlan el contenido de las etiquetas mutables del area de juego 1
        self.modo_seleccionado.set(self.configuraciones_de_juego["tipo_partida"])
        self.dificultad_seleccionada.set(self.configuraciones_de_juego["dificultad"])
        self.dimensiones_seleccionadas.set(self.configuraciones_de_juego["dimensiones"])
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Valores de área 1 actualizadas.")
        
        self.visualizar_laberinto()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Laberinto cargado en la ventana.")

    # DIMENSIONES DINAMICAS ---------------------------------------------------------------------------------------------------------------
    # E: el parametro de entrada es un evento que sucede al cambiar la seleccion de dificultad en el combobox del menu
    # S: no tiene salidas; la funcion se encarga de cambiar los valores disponibles en el combobox de dimeniones en base a la dificultad seleccionada
    # R: TBD
    def dimensiones_dinamicas(self, evento):
        dificultad_seleccionada = self.combo_dificultad.get()
        if dificultad_seleccionada == "Fácil":
            dimension_opciones = ["8x8", "9x9", "10x10"]
        elif dificultad_seleccionada == "Medio":
            dimension_opciones = ["11x11", "12x12", "13x13"]
        elif dificultad_seleccionada == "Difícil":
            dimension_opciones = ["14x14", "15x15", "16x16"]
        else:
            dimension_opciones = ["selección"]
        self.combo_dimensiones["values"] = dimension_opciones
        self.combo_dimensiones.set(dimension_opciones[0])

    # TIEMPO PARTIDA DINAMICO -------------------------------------------------------------------------------------------------------------
    # E: el paramtro de entrada es un evento que sucede al cambiar la seleccion del modo de juego en el combobox del menu
    # S: no tiene salida; la funcion se encarga de mostrar o esconder la etiqueta y combobox de seleccion de minutos de partida
    # R: TBD
    def tiempo_partida_dinamico(self, evento):
        selected_type = self.combo_partida.get()
        if selected_type == "Contra Tiempo":
            self.etiqueta_tiempo.grid(row=3, column=0, sticky='w')
            self.combo_tiempo.grid(row=4, column=0, pady=(0, 5), sticky='nsew')
            self.combo_tiempo.set(2)

        else:
            self.etiqueta_tiempo.grid_forget()
            self.combo_tiempo.grid_forget()
    
    # VISUALIZAR LABERINTO ----------------------------------------------------------------------------------------------------------------
    # E: no tiene parametros de entrada
    # S: la funcion se encarga de mostrar en pantalla el laberinto cargado en memoria creando objetos 'bloque'
    # R: 
    def visualizar_laberinto(self):
        self.canvas_laberinto.delete("all") # limpia el canvas que contiene los bloques del laberinto antes de crear y mostrar nuevos bloques
        self.bloque_matriz.clear() # limpia la matriz donde se almacenan los bloques del laberinto

        ancho_cuadro = self.canvas_laberinto.winfo_width() # guarda el ancho actual de la ventana para calcular el tamaño de los bloques
        alto_cuadro = self.canvas_laberinto.winfo_height() # guarda el alto actual de la ventana para calcular el tamaño de los bloques

        filas = len(self.laberinto_en_memoria)
        columnas = len(self.laberinto_en_memoria[0]) # se carga la cantidad de columnas asumiendo que el laberinto fue validado
        tamaño_celda = min(ancho_cuadro // columnas, alto_cuadro // filas) # calculo para obtener el tamanho de celda para mostrar el laberinto en base al tamanho de la pantalla

        for fila in range(filas):
            fila_de_bloques = [] # lista vacia para guardar todos los bloques de la fila a guardar
            for columna in range(columnas):
                x1 = columna * tamaño_celda #coordenadas de inicio del bloque en pantalla
                y1 = fila * tamaño_celda
                x2 = x1 + tamaño_celda # coordenadas de final del bloque en pantalla
                y2 = y1 + tamaño_celda
                
                valor_en_laberinto = self.laberinto_en_memoria[fila][columna] # carga el valor que va a tener el bloque (-1, 0, 1, 2)
                
                rectangulo_id = self.canvas_laberinto.create_rectangle(x1, y1, x2, y2, outline="gray") # guarda el id de cada rectangulo creado en el canvas principal donde se va a posicionar el nuevo bloque a crear
                
                nuevo_bloque = bloque(self.canvas_laberinto, rectangulo_id, fila, columna, valor_en_laberinto)
                nuevo_bloque.set_color(nuevo_bloque.get_color())

                fila_de_bloques.append(nuevo_bloque) # se agrega el bloque creado a la fila de bloques que se guardara en la matriz de bloques
                
                if valor_en_laberinto == -1: # en el momento que se encuentre el punto de inicio, se guarda en la partida para la posicion inicial del totem
                    self.posicion_actual_totem = (fila, columna)

            self.bloque_matriz.append(fila_de_bloques) # se agrega la fila de bloques a la matriz de bloques
    
    # MOSTRAR TOKEN -----------------------------------------------------------------------------------------------------------------------
    # E: como parametro de entrada se recibe una tupla con los valores (fila, columna) para manejar la posicion del token
    # S: no tiene salida; la funcion se encarga de mover el token en la pantalla; cada instancia de la funcion limpia y vuelve a mostrar el token en base a la posicion actual en la partida
    # R: TBD
    def mostrar_totem(self, position):
        self.canvas_laberinto.delete("totem") # se borra el token de la posicion actual; esta funcion se llama cada movimiento que se hace en la posicion del token
        fila, columna = position
        
        tamaño_celda = min(self.canvas_laberinto.winfo_width() // len(self.laberinto_en_memoria[0]), 
                        self.canvas_laberinto.winfo_height() // len(self.laberinto_en_memoria))
        
        centro_fila = columna * tamaño_celda + tamaño_celda / 2
        centro_columna = fila * tamaño_celda + tamaño_celda / 2
        
        tamaño_totem = tamaño_celda / 3
        
        x1 = centro_fila - tamaño_totem
        y1 = centro_columna - tamaño_totem
        x2 = centro_fila + tamaño_totem
        y2 = centro_columna + tamaño_totem
        
        self.canvas_laberinto.create_oval(x1, y1, x2, y2, fill="blue", tags="totem") # vuelve a generar el totem en al pantalla con su posicion actualizada

    # MOVIMIENTO TECLAS -------------------------------------------------------------------------------------------------------------------
    # E: el paremetro de entrada es un evento; en este caso el evento de pserionar una tecla con el enfoque en la venta de juego
    # S: no tiene salidas; la funcion se encarga de registar los movimientos de las teclas en 
    # R: TBD
    def movimiento_teclas(self, event):
        if self.partida_iniciada == False: # no actua si la partida no esta iniciada
            return
        # se guardan los valores fila y columna de la posicion actual en variables separadas para manejarlos en la funcion
        fila, columna = self.posicion_actual_totem
        nueva_fila, nueva_columna = fila, columna
        
        # se valida el tipo de input que se recibe del evento
        if event.keysym == "Up":
            nueva_fila -= 1
        elif event.keysym == "Down":
            nueva_fila += 1
        elif event.keysym == "Left":
            nueva_columna -= 1
        elif event.keysym == "Right":
            nueva_columna += 1

        if (0 <= nueva_fila < len(self.laberinto_en_memoria) and 
            0 <= nueva_columna < len(self.laberinto_en_memoria[0]) and
            self.laberinto_en_memoria[nueva_fila][nueva_columna] != 1):
            self.movimientos_partida += 1 # aumenta los movimientos de la partida
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} movimiento {event.keysym} #{self.movimientos_partida}")
            bloque_anterior = self.bloque_matriz[fila][columna]
            if bloque_anterior.valor_bloque == 0 and not bloque_anterior.visitado:
                bloque_anterior.set_color("lightblue")
                bloque_anterior.visitado = True
                
            self.posicion_actual_totem = (nueva_fila, nueva_columna)
            self.mostrar_totem(self.posicion_actual_totem)
            
            if self.laberinto_en_memoria[nueva_fila][nueva_columna] == 2:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ¡Has llegado al final!")
                self.canvas_laberinto.create_text(
                    self.canvas_laberinto.winfo_width() / 2,
                    self.canvas_laberinto.winfo_height() / 2,
                    text="¡Ganaste!", font=("Helvetica", 40, "bold"), fill="blue"
                )

    # INICIAR PARTIDA -------------------------------------------------------------------------------------------------------------------------
    # E: no tiene entradas; comienza la partida
    # S: la funcion se encarga de cambiar el valor 'partida_iniciada' de la partida; inicia los movimientos en 0; crea un objeto cronometro y lo inicia; dibuja el totem en la pantalla
    # R: 
    def iniciar_partida(self):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS: Partida iniciada. Usa las flechas para moverte.")
        self.movimientos_partida = 0
        self.partida_iniciada = True # habilita el movimiento del totem
        self.mostrar_totem(self.posicion_actual_totem) # muestra el totem en la ventana
        if self.configuraciones_de_juego["tipo_partida"] == "Contra Tiempo":
            self.instancia_cronometro = cronometro("regresivo", self)
        else:
            self.instancia_cronometro = cronometro("progresivo", self)    
        self.instancia_cronometro.iniciar()

    def reiniciar_partida(self):
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Reiniciando partida...")
        self.visualizar_laberinto()
        self.iniciar_partida()

    def autocompletar_laberinto(self):
        print("Función de auto-completar aún no implementada.")

    def abandonar_partida(self):
        self.partida_iniciada = False
        self.instancia_cronometro.detener()
        self.visualizar_laberinto()
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS: Partida abandonada")

# INICIO DE PARTIDA Y VENTANA PRINCIPAL ___________________________________________________________________________________________________
if __name__ == "__main__": # iniciar la ventana unicamente si el archvo se esta ejecutando directamente 
    print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} LABERINTO 1.0 INICIADO")
    ventana = tk.Tk() # se crea una instancia de una ventana .Tk()
    juego = partida(ventana) # se envia la ventana como parametro para la variable "ventana_root" del objeto tipo partida
    ventana.mainloop() # genera la ventana principal
