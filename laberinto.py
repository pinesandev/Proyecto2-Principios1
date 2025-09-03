# IMPORTS / LIBRARIES
import tkinter as tk
from tkinter import ttk, PhotoImage
import time # utilizado para utilizar la funcion sleep()
from datetime import datetime, timedelta # para manejar todos los tiempos del programa
import threading # para crear un proceso / thread  para el cronometro
from validar_laberinto import validar_laberinto

# CLASSES _________________________________________________________________________________________________________________________________
# CRONOMETRO ------------------------------------------------------------------------------------------------------------------------------
class cronometro:
    def __init__(self, tipo_crono, partida):
        self.partida = partida
        self.segundos = partida.contador_tiempo.get()
        self.tipo_crono = tipo_crono
        self.corriendo = False # almacena el estado del cronometro para controlar los procesos
        self.proceso = None # se guarda el proceso / thread que comienza al inicializar el cronometro
        

    # *** FUNCIONES DE CLASE ***
    def iniciar(self):
        # validar que el cronometro no esta corriendo; corriendo == False
        if self.corriendo == False:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} INFO: cronometro {self.tipo_crono} inicializado")
            self.corriendo = True
            self.proceso = threading.Thread(target=self.runtime, daemon=True)
            self.proceso.start()
    
    def runtime(self):
        while self.corriendo == True:
            time.sleep(1)
            if self.tipo_crono == "progresivo" and self.corriendo:
                self.segundos += 1
                self.partida.contador_tiempo.set(self.segundos)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CRONO: tiempo transcurrido {self.segundos} s")
            elif self.tipo_crono == "regresivo" and self.corriendo:
                if self.segundos == 0:
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CRONO: se acabo el tiempo!")
                    self.detener() # se detiene el cronometro         
                    ventana_perdida = tk.Toplevel(self.partida.ventana_root)
                    ventana_perdida.title("¡LABERINTO FALLIDO!")
                    ventana_perdida.resizable(False, False)
                    ventana_perdida.protocol("WM_DELETE_WINDOW", lambda: None)
                    ventana_perdida.geometry(f"300x200+{self.partida.ventana_root.winfo_x() + (self.partida.ventana_root.winfo_width()//2) - (280//2)}+{self.partida.ventana_root.winfo_y() + (self.partida.ventana_root.winfo_height()//2) - (150//2)}")
                    ttk.Label(ventana_perdida, text="Se acabo el tiempo", font=("Courier", 20)).place(relx=0.5, rely=0.3, anchor="center")
                    ttk.Button(ventana_perdida, text="Volver", command=lambda: self.partida.finalizar_partida(None, ventana_perdida, False), style='estilo_custom.TButton').place(relx=0.5, rely=0.7, anchor="center")
                else:
                    self.segundos -= 1
                    self.partida.contador_tiempo.set(self.segundos)
                    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CRONO: tiempo transcurrido {300 - self.segundos} s")
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} CRONO: cronometro detenido")

    def detener(self):
        self.corriendo = False # cambia el estado del cronometro para que el ciclo del runtime termine
            
# CLASE BLOQUE ----------------------------------------------------------------------------------------------------------------------------
class bloque:
    def __init__(self, cuadro, bloque, fila, columna, valor):
        self.cuadro = cuadro # cuadro de juego conteniendo todos los bloques; tipo canvas de tkinter
        self.bloque = bloque # informacion sobre el cuadro de bloque que se crea para cada celda del laberinto
        self.fila = fila
        self.columna = columna
        self.valor = valor  # -1: inicio, 0: camino abierto, 1: pared, 2: meta
        self.visitado = False # para modificar el bloque al ser visitado durante el juego

    # *** FUNCIONES DE CLASE ***
    # SET COLOR ---------------------------------------------------------------------------------------------------------------------------
    # E: tiene como entrada el valor del color que se va a establecer o cambiar en el bloque
    # S: no tiene salidas; la funcion se encarga de cambiar el color del bloque
    # R: el color tiene que ser de tipo string y un color valido para tkinter e .itemconfigure()
    def set_color(self, color): # metodo para cambiar el valor y color del widget
        self.cuadro.itemconfigure(self.bloque, fill=color)

    # GET COLOR ---------------------------------------------------------------------------------------------------------------------------
    # E: no tiene entradas
    # S: retorna el color que debe tener el bloque en base a su valor (-1, 0, 1, 2)
    # R: no tiene restricciones
    def get_color(self): # metodo para obtener el color del
        if self.valor== 1:
            return "brown"  # Pared
        elif self.valor == 2:
            return "yellow" # Final
        elif self.valor == -1:
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
        self.ventana_root.resizable(False, False)
        self.ventana_root.columnconfigure(0, weight=3, minsize=250)
        self.ventana_root.columnconfigure(1, weight=7)
        self.ventana_root.rowconfigure(0, weight=1)

        # configuraciones y variables de juego
        self.partida_iniciada = False
        self.cronometro = None # guarda el cronometro inicializado en la partida
        self.ranking = []
        self.laberinto = []
        self.bloques = [] # guardar una matriz de todos los objetos tipo bloque se que crean para cada laberinto
        self.posicion_totem = None # almacena la posicion del totem en el laberinto
        self.modo_seleccionado = tk.StringVar()
        self.dificultad_seleccionada = tk.StringVar()
        self.dimensiones_seleccionadas = tk.StringVar()
        self.contador_tiempo = tk.IntVar()
        self.movimientos_partida = tk.IntVar()
        self.nombre_usuario = None

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
        ttk.Label(self.cuadro_juego1, text="Movimientos:", font=("Courier", 16, "bold")).grid(column=0, row=1, sticky='w') # etiqueta estatica de dificultad
        ttk.Label(self.cuadro_juego1, textvariable=self.movimientos_partida, font=("Courier", 14,)).grid(column=1, row=1, sticky='w') # etiqueta mutable de dificultad
        ttk.Label(self.cuadro_juego1, text="Dimensiones:", font=("Courier", 16, "bold")).grid(column=2, row=0, sticky='w') # etiqueta estatica de dimensiones
        ttk.Label(self.cuadro_juego1, textvariable=self.dimensiones_seleccionadas, font=("Courier", 14,)).grid(column=3, row=0, sticky='w') # etiqueta mutable de dimeniones
        ttk.Label(self.cuadro_juego1, text="Tiempo:", font=("Courier", 16, "bold")).grid(column=2, row=1, sticky='w') # etiqueta estatica de tiempo
        ttk.Label(self.cuadro_juego1, textvariable=self.contador_tiempo, font=("Courier", 14,)).grid(column=3, row=1, sticky='w') # etiqueta mutable de tiempo

        # botones del area de juego 1 para controlar el funcionamiento de la patida
        ttk.Button(self.cuadro_juego1, text="Iniciar", command=self.iniciar_partida, style='estilo_custom.TButton').grid(column=0, row=2, sticky='nsew')
        ttk.Button(self.cuadro_juego1, text="Reiniciar", command=self.reiniciar_partida, style='estilo_custom.TButton').grid(column=1, row=2, sticky='nsew')
        ttk.Button(self.cuadro_juego1, text="Auto completar", command=self.autocompletar, style='estilo_custom.TButton').grid(column=2, row=2, sticky='nsew')
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
        self.cuadro_menu.rowconfigure(11, weight=1)

        # *** WIDGETS | CUADRO MENU *** 
        ttk.Label(self.cuadro_menu, text="Menu", font=("Courier", 20, "bold")).grid(row=0, column=0, pady=(0, 15))
        ttk.Label(self.cuadro_menu, text="Modo de Juego", font=("Courier", 14, "bold", "italic")).grid(row=1, column=0, sticky='w')
        self.combo_partida = ttk.Combobox(self.cuadro_menu, values=["Normal", "Contra Tiempo"])
        self.combo_partida.grid(row=2, column=0, sticky='nsew', pady=(0, 5))
        self.combo_partida.set("Normal")
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
        self.ranking = self.cargar_rankings("archivos/rankings.txt") # se cargan los rankings
        self.mostrar_ranking() # se carga el rakning en el treeview

        # *** VICULAR EVENTOS ***
        # se vinculan eventos como cambiar el tamaño de la pantalla y inputs del teclado con su respectiva funcion
        self.ventana_root.bind("<Key>", self.movimiento) ### VALIDAR PARA ACEPTAR INPUTS UNICAMENTE CUANDO SE INICIA LA PARTIDA

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
                validacion = validar_laberinto(laberinto)
                if not validacion['valido']:
                    print(validacion['mensaje'])
                    laberinto = []
        except FileNotFoundError:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Error: Archivo no encontrado en {ruta}")
            return None
        return laberinto
    

    # LLAVE ORDEN -------------------------------------------------------------------------------------------------------------------------
    # E: una lista representativa de la linea de los rankings
    # S: una tupla de 3 valores con el tiempo, las dimensiones y los movimientos de cada partida
    # R: el parametro de entrada debe ser de tipo lista; no tiene validaciones programadas
    def llave(self, linea_partida):
        tiempo = int(linea_partida[0])
        dimensiones = int(linea_partida[2].split("x")[0])
        movimientos = int(linea_partida[3])
        return (tiempo,-dimensiones, movimientos)

    # CARGAR RANKING ----------------------------------------------------------------------------------------------------------------------
    # E: Ruta al archivo de texto que contiene el ranking guardado
    # S: Devuelve una matriz que representa el ranking ordenada
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
        for i in range(len(lista_ranking)):
            indice_minimo = i
            for ii in range(i+1, len(lista_ranking)):
                if self.llave(lista_ranking[ii]) < self.llave(lista_ranking[indice_minimo]):
                    indice_minimo = ii
            lista_ranking[i], lista_ranking[indice_minimo] = lista_ranking[indice_minimo], lista_ranking[i]
        return lista_ranking

    # GUARDAR INFORMACION -----------------------------------------------------------------------------------------------------------------
    # E: no tiene entradas
    # S: no tiene salidas; la funcion unicamente guarda la informacion en los archivos .txt a la hora de salir del programa
    # R: no tiene restricciones
    def guardar_rankings(self):
        archivo_ranking = open("archivos/rankings.txt", "w")
        for partida in self.ranking:
            archivo_ranking.write(f"{partida[0]},{partida[1]},{partida[2]},{partida[3]}\n")
        archivo_ranking.close()

    # MOSTRAR RANKING ---------------------------------------------------------------------------------------------------------------------
    # E: no tiene entradas
    # S: la funcion se encarga de limpiar los valores en el treeview donde se muestra el raking y cargarlos nuevamente
    # R: TBD
    def mostrar_ranking(self):
            for item in self.ranking_treeview.get_children(): # ciclo para limpiar el widget 'ranking_treeview'
                self.ranking_treeview.delete(item)
            
            for fila in self.ranking: # cargar datos nuevamente en el widget 'ranking_treeview'
                self.ranking_treeview.insert("", "end", values=fila)

    # GUARDAR CONFIGURACIONES -------------------------------------------------------------------------------------------------------------
    # E: no tiene entradas; la funcion se encarga de guardar las selecciones del usuario en la variable global 'configuraciones_de_juego'
    # S: no tiene salidas; el resultado de invocar la funcion es modificar la variable global donde se guardan las configuraciones de juego antes de comenzar
    # R: TBD
    def guardar_configuraciones(self):
        if self.partida_iniciada == False: # solo guarda las configuraciones cuando la partida esta inactiva
            # guardar las configuraciones de juego seleccionadas en el menu dentro de un diccionario en el objeto tipo partida (configuraciones_de_juego)
            self.modo_seleccionado.set(self.combo_partida.get())
            if self.modo_seleccionado.get() == "Contra Tiempo": # se valida la configuracion guardada en el diccionario para asignar el valor de segundos correctamente
                self.contador_tiempo.set(300)
            else:
                self.contador_tiempo.set(0)
                self.movimientos_partida.set(0)
            self.dificultad_seleccionada.set(self.combo_dificultad.get())
            self.dimensiones_seleccionadas.set(self.combo_dimensiones.get())
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Las siguientes configuraciones fueron cargadas:") # log en terminal que indica las configuraciones cargadas
            print(f"Tipo: {self.modo_seleccionado.get()} | Segundos: {self.contador_tiempo.get()} | Dificultad: {self.dificultad_seleccionada.get()} | Dimensiones: {self.dimensiones_seleccionadas.get()}")
            # se crea ruta del laberinto en base a las configuraciones cargadas y se carga el laberinto con dicha ruta
            ruta_laberinto = f"archivos/laberintos/{self.dificultad_seleccionada.get()}/{self.dimensiones_seleccionadas.get()}.txt"
            self.laberinto = self.cargar_laberinto(ruta_laberinto)
        
            
    
    # DIMENSIONES DINAMICAS ---------------------------------------------------------------------------------------------------------------
    # E: el parametro de entrada es un evento que sucede al cambiar la seleccion de dificultad en el combobox del menu
    # S: no tiene salidas; la funcion se encarga de cambiar los valores disponibles en el combobox de dimeniones en base a la dificultad seleccionada
    # R: TBD
    def dimensiones_dinamicas(self, evento):
        if self.combo_dificultad.get() == "Fácil":
            dimension_opciones = ["8x8", "9x9", "10x10"]
        elif self.combo_dificultad.get() == "Medio":
            dimension_opciones = ["11x11", "12x12", "13x13"]
        elif self.combo_dificultad.get() == "Difícil":
            dimension_opciones = ["14x14", "15x15", "16x16"]
        self.combo_dimensiones["values"] = dimension_opciones
        self.combo_dimensiones.set(dimension_opciones[0])
    
    # VISUALIZAR LABERINTO ----------------------------------------------------------------------------------------------------------------
    # E: no tiene parametros de entrada
    # S: la funcion se encarga de mostrar en pantalla el laberinto cargado en memoria creando objetos 'bloque'
    # R: 
    def visualizar_laberinto(self):
        if self.laberinto == []:
            print('No se puede cargar un laberinto vacio')
            return 
        self.canvas_laberinto.delete("all")
        self.bloques.clear()
        tamaño_celda = min(self.canvas_laberinto.winfo_width() // len(self.laberinto[0]), self.canvas_laberinto.winfo_height() // len(self.laberinto)) # calculo para obtener el tamanho de celda para mostrar el laberinto en base al tamanho de la pantalla
        for fila in range(len(self.laberinto)):
            fila_de_bloques = [] # lista vacia para guardar todos los bloques de la fila a guardar
            for columna in range(len(self.laberinto[0])):
                if self.laberinto[fila][columna] == -1: # en el momento que se encuentre el punto de inicio, se guarda en la partida para la posicion inicial del totem
                    self.posicion_totem = (fila, columna)
                x1 = columna * tamaño_celda #coordenadas de inicio del bloque en pantalla
                y1 = fila * tamaño_celda
                x2 = x1 + tamaño_celda # coordenadas de final del bloque en pantalla
                y2 = y1 + tamaño_celda
                rectangulo_id = self.canvas_laberinto.create_rectangle(x1, y1, x2, y2, outline="gray") # guarda el id de cada rectangulo creado en el canvas principal donde se va a posicionar el nuevo bloque a crear
                nuevo_bloque = bloque(self.canvas_laberinto, rectangulo_id, fila, columna, self.laberinto[fila][columna])
                nuevo_bloque.set_color(nuevo_bloque.get_color())
                fila_de_bloques.append(nuevo_bloque) # se agrega el bloque creado a la fila de bloques que se guardara en la matriz de bloques
            self.bloques.append(fila_de_bloques)
        print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Laberinto cargado en la ventana.") # se agrega la fila de bloques a la matriz de bloques
    
    # MOSTRAR TOTEM -----------------------------------------------------------------------------------------------------------------------
    # E: como parametro de entrada se recibe una tupla con los valores (fila, columna) para manejar la posicion del token
    # S: no tiene salida; la funcion se encarga de mover el token en la pantalla; cada instancia de la funcion limpia y vuelve a mostrar el token en base a la posicion actual en la partida
    # R: TBD
    def mostrar_totem(self, posicion):
        self.canvas_laberinto.delete("totem") # se borra el token de la posicion actual; esta funcion se llama cada movimiento que se hace en la posicion del token
        fila, columna = posicion
        tamaño_celda = min(self.canvas_laberinto.winfo_width() // len(self.laberinto[0]), 
                        self.canvas_laberinto.winfo_height() // len(self.laberinto))
        centro_fila = columna * tamaño_celda + tamaño_celda / 2
        centro_columna = fila * tamaño_celda + tamaño_celda / 2
        tamaño_totem = tamaño_celda / 3
        x1 = centro_fila - tamaño_totem
        y1 = centro_columna - tamaño_totem
        x2 = centro_fila + tamaño_totem
        y2 = centro_columna + tamaño_totem
        self.canvas_laberinto.create_oval(x1, y1, x2, y2, fill="gold", tags="totem") # vuelve a generar el totem en al pantalla con su posicion actualizada

    # MOVIMIENTO TECLAS -------------------------------------------------------------------------------------------------------------------
    # E: el paremetro de entrada es un evento; en este caso el evento de pserionar una tecla con el enfoque en la venta de juego
    # S: no tiene salidas; la funcion se encarga de registar los movimientos de las teclas en 
    # R: TBD
    def movimiento(self, event):
        if self.partida_iniciada == False: # no actua si la partida no esta iniciada
            return
        # se guardan los valores fila y columna de la posicion actual en variables separadas para manejarlos en la funcion
        fila, columna = self.posicion_totem
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
        if (0 <= nueva_fila < len(self.laberinto) and 
            0 <= nueva_columna < len(self.laberinto[0]) and
            self.laberinto[nueva_fila][nueva_columna] != 1):
            self.movimientos_partida.set(self.movimientos_partida.get() + 1) # aumenta los movimientos de la partida
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} movimiento {event.keysym} #{self.movimientos_partida.get()}")
            bloque_anterior = self.bloques[fila][columna]
            if bloque_anterior.valor == 0 and not bloque_anterior.visitado:
                bloque_anterior.set_color("lightgreen")
                bloque_anterior.visitado = True
            self.posicion_totem = (nueva_fila, nueva_columna)
            self.mostrar_totem(self.posicion_totem)
            if self.laberinto[nueva_fila][nueva_columna] == 2:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS: partida ganada!")
                self.cronometro.detener() # se detiene el cronometro         
                ventana_gane = tk.Toplevel(self.ventana_root)
                ventana_gane.title("¡LABERINTO COMPLETADO!")
                ventana_gane.resizable(False, False)
                ventana_gane.protocol("WM_DELETE_WINDOW", lambda: None)
                ventana_gane.geometry(f"300x200+{self.ventana_root.winfo_x() + (self.ventana_root.winfo_width()//2) - (280//2)}+{self.ventana_root.winfo_y() + (self.ventana_root.winfo_height()//2) - (150//2)}")
                ttk.Label(ventana_gane, text="Digite su Nombre", font=("Courier", 20)).place(relx=0.5, rely=0.3, anchor="center")
                entrada_usuario = ttk.Entry(ventana_gane, width=30, textvariable=self.nombre_usuario)
                entrada_usuario.place(relx=0.5, rely=0.5, anchor="center")
                ttk.Button(ventana_gane, text="Guardar Partida", command=lambda: self.finalizar_partida(entrada_usuario.get(), ventana_gane, True), style='estilo_custom.TButton').place(relx=0.5, rely=0.7, anchor="center")

    # RESOLVER LABERINTO ------------------------------------------------------------------------------------------------------------------
    # E: la funcion toma como parametros el laberinto cargado en la partida, la posición de fila y columna del totem y una matriz nueva generada únicamente para iterar los caminos en la validación
    # S: la funcion retorna una lista con el camino correcto para iterar y mostrar en la ventana de laberinto; en caso de no tener salida, retorna False
    # R: solo opera cuanto la posicion del totem se encuentra dentro de un rango valido en el laberinto (camino o borde de la matriz)
    def resolver_laberinto(self, laberinto, fila, columna, matriz_visitados):
        if (fila < 0 or fila >= len(laberinto) or
            columna < 0 or columna >= len(laberinto[0]) or
            laberinto[fila][columna] == 1 or
            matriz_visitados[fila][columna]): # valida que la posicion se mantenga dentro de los limites del laberinto / matriz
            return False
        if laberinto[fila][columna] == 2: # condicion de finalizacion
            return [(fila, columna)]
        matriz_visitados[fila][columna] = True
        for x, y in [(-1,0), (1,0), (0,-1), (0,1)]:
            camino_correcto = self.resolver_laberinto(laberinto, fila+x, columna+y, matriz_visitados)
            if camino_correcto:
                return [(fila, columna)] + camino_correcto
        return False

    # INICIAR PARTIDA -------------------------------------------------------------------------------------------------------------------------
    # E: no tiene entradas; comienza la partida
    # S: no tiene salidas; la funcion se encarga de cambiar el valor 'partida_iniciada' de la partida; inicia los movimientos en 0; crea un objeto cronometro y lo inicia; dibuja el totem en la pantalla
    # R: solo se inicia la partida en caso de que el valor de la partida 'partida_iniciada' sea False
    def iniciar_partida(self):
        if self.laberinto == []:
            ventana_invalida = tk.Toplevel(self.ventana_root)
            ventana_invalida.title("¡LABERINTO INVALIDO!")
            ventana_invalida.protocol("WM_DELETE_WINDOW", lambda: None)
            ventana_invalida.geometry(f"300x200+{self.ventana_root.winfo_x() + (self.ventana_root.winfo_width()//2) - (280//2)}+{self.ventana_root.winfo_y() + (self.ventana_root.winfo_height()//2) - (150//2)}")
            ttk.Label(ventana_invalida, text="Laberinto Invalido", font=("Courier", 20)).place(relx=0.5, rely=0.3, anchor="center")
            ttk.Button(ventana_invalida, text="Volver", command=lambda: ventana_invalida.destroy(), style='estilo_custom.TButton').place(relx=0.5, rely=0.7, anchor="center")
        elif self.partida_iniciada == False:
            self.movimientos_partida.set(0)
            self.partida_iniciada = True # habilita el movimiento del totem
            self.visualizar_laberinto()
            self.mostrar_totem(self.posicion_totem) # muestra el totem en la ventana
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS: Partida iniciada. Usa las flechas para moverte.")
            if self.modo_seleccionado.get() == "Contra Tiempo":
                self.cronometro = cronometro("regresivo", self)
            else:
                self.cronometro = cronometro("progresivo", self)    
            self.cronometro.iniciar()
            
            

    # REINICIAR PARTIDA -------------------------------------------------------------------------------------------------------------------
    # E: la funcion no tiene entradas; reinicia la partida
    # S: no tiene salidas; la funcion se encarga de imprimir en consola que la partida fue reiniciada, cambia el estado de partida_iniciada temporalmente a Falso, detiene el cronometro, vuelve a guardar las configuraciones y actualiza la pantalla y por ultimo inicia la partida nuevamente
    # R: solo se puede reiniciar la partida en caso de que el valor de partida_iniciada sea True
    def reiniciar_partida(self):
        if self.partida_iniciada == True:
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} Reiniciando partida...")
            self.partida_iniciada = False
            self.cronometro.detener()
            self.guardar_configuraciones()
            self.iniciar_partida()

    # AUTOCOMPLETAR -----------------------------------------------------------------------------------------------------------------------
    # E: no tiene entradas; la funcion se encarga de autocompletar el laberinto una vez que se conozca la solucion
    # S: no tiene salidas; esta funcion llama la funcion resolver laberinto para obtener ya sea False en caso de no tener solucion y la lista de movimientos en caso de existir una salida encontrada
    # R: solo se puede autocompletar la partida en caso de que el valor de partida_iniciada sea True
    def autocompletar(self):   
        if self.partida_iniciada == True:
            self.partida_iniciada = False
            self.cronometro.detener()
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS: Autocompletando partida")
            matriz_visitados = [[False for _ in fila] for fila in self.laberinto]
            fila_inicio, columna_inicio = self.posicion_totem
            camino_meta = self.resolver_laberinto(self.laberinto, fila_inicio, columna_inicio, matriz_visitados)
            if camino_meta: # en caso de que la lista sea algo diferente de None, False o []
                for fila, columna in camino_meta:
                    bloque_actual = self.bloques[fila][columna]
                    if bloque_actual.valor == 0:
                        bloque_actual.set_color("lightgreen")
                        bloque_actual.visitado = True
                    self.posicion_totem = (fila, columna)
                    self.mostrar_totem(self.posicion_totem)
                    self.ventana_root.update()
                    self.ventana_root.after(100)
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS: Laberinto completado automáticamente.")
                ventana_auto = tk.Toplevel(self.ventana_root)
                ventana_auto.title("¡LABERINTO COMPLETADO!")
                ventana_auto.resizable(False, False)
                ventana_auto.protocol("WM_DELETE_WINDOW", lambda: None)
                ventana_auto.geometry(f"300x200+{self.ventana_root.winfo_x() + (self.ventana_root.winfo_width()//2) - (280//2)}+{self.ventana_root.winfo_y() + (self.ventana_root.winfo_height()//2) - (150//2)}")
                ttk.Label(ventana_auto, text="Laberinto autocompletado", font=("Courier", 20)).place(relx=0.5, rely=0.3, anchor="center")
                ttk.Button(ventana_auto, text="Volver", command=lambda: self.finalizar_partida(None, ventana_auto, False), style='estilo_custom.TButton').place(relx=0.5, rely=0.7, anchor="center")
            else:
                print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS: No se encontró solución al laberinto.")

    # ABANDONAR PARTIDA -------------------------------------------------------------------------------------------------------------------
    # E: la funcion no tiene entradas; abandona la partida
    # S: la funcion no tiene salidas; se encarga de abandonar la partida en base a la desicion del usuario
    # R: solo se puede abandonar la partida en caso de que el valor de partida_iniciada sea True
    def abandonar_partida(self):
        if self.partida_iniciada == True:
            self.partida_iniciada = False
            self.cronometro.detener()
            self.guardar_configuraciones()
            self.visualizar_laberinto()
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} STATUS: Partida abandonada")

    # FINALIZAR PARTIDA -------------------------------------------------------------------------------------------------------------------
    # E: esta funcion toma como parametros de entrada el nombre del usuario, la ventana emergente y una variable bool para establecer si la partida fue ganada o no
    # S: no tiene salidas; la funcion se encarga de guardar el ranking en caso de que la partida haya sido ganada y limpiar  el laberinto recargando las configuraciones; en caso de ser una partida perdida, solo se limpia el laberinto y se vuelve a cargar la configuracion de partida
    # R: solo se puede finalizar la partida en caso de que el valor de partida_iniciada sea True
    def finalizar_partida(self, nombre_usuario, ventana_emergente, partida_ganada):
        self.partida_iniciada = False
        if nombre_usuario != "" and partida_ganada == True:
            if self.modo_seleccionado.get() == "Contra Tiempo":
                self.ranking.append([(300 - self.contador_tiempo.get()), nombre_usuario, self.dimensiones_seleccionadas.get(), self.movimientos_partida.get()])
            else:
                self.ranking.append([self.contador_tiempo.get(), nombre_usuario, self.dimensiones_seleccionadas.get(), self.movimientos_partida.get()])
            self.guardar_rankings()
            self.ranking = self.cargar_rankings("archivos/rankings.txt")
            self.mostrar_ranking()
        self.guardar_configuraciones()
        self.visualizar_laberinto()
        ventana_emergente.destroy()

# INICIO DE PARTIDA Y VENTANA PRINCIPAL ___________________________________________________________________________________________________
if __name__ == "__main__": # iniciar la ventana unicamente si el archvo se esta ejecutando directamente 
    print(f"\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} LABERINTO 1.0 INICIADO")
    ventana = tk.Tk() # se crea una instancia de una ventana .Tk()
    juego = partida(ventana) # se envia la ventana como parametro para la variable "ventana_root" del objeto tipo partida
    ventana.mainloop() # genera la ventana principal
