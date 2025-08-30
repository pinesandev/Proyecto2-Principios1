import tkinter as tk
from tkinter import ttk
from random import shuffle

# CLASES __________________________________________________________________________________________________________________________________
class bloque:
    def __init__(self, canvas_widget, rect_id, fila, columna, valor_bloque): # clase para instanciar un bloque individual en el laberinto; cuadro juego 2
        self.canvas_widget = canvas_widget
        self.rect_id = rect_id
        self.row = fila
        self.col = columna
        self.value = valor_bloque  # -1: inicio, 0: camino abierto, 1: pared, 2: meta
        self.is_visited = False

    def set_color(self, color):
        """Método para cambiar el color del rectángulo en el canvas."""
        self.canvas_widget.itemconfigure(self.rect_id, fill=color)
        
    def get_color(self):
        """Método para retornar el color apropiado para el valor del bloque."""
        if self.value == 1:
            return "brown"  # Pared
        elif self.value == 2:
            return "yellow" # Final
        elif self.value == -1:
            return "green"  # Inicio
        else:
            return "white" # Camino

class juego_laberinto:
    def __init__(self, root):
        self.root = root
        self.root.title("Laberinto")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)

        # Atributos de la clase (reemplazan a las variables globales)
        self.configuraciones_de_juego = {"tipo_partida": "Normal", "tiempo": None, "dificultad": "Fácil", "dimensiones": "8x8"}
        self.ranking_en_memoria = []
        self.laberinto_en_memoria = []
        self.bloque_matrix = []
        self.current_position = None
        self.totem_id = None
        
        # Estilo para los botones
        self.estilo_default_botones = ttk.Style()
        self.estilo_default_botones.configure('estilo_custom.TButton', font=('Courier', 14, 'bold'))

        # Configuración de la cuadrícula principal
        self.root.columnconfigure(0, weight=3, minsize=250)
        self.root.columnconfigure(1, weight=7)
        self.root.rowconfigure(0, weight=1)

        # Contenedor del área de juego
        self.container_juego = ttk.Frame(root)
        self.container_juego.grid(row=0, column=1, sticky='nsew')
        self.container_juego.columnconfigure(0, weight=1)
        self.container_juego.rowconfigure(0, weight=0)
        self.container_juego.rowconfigure(1, weight=1)

        # CUADRO | AREA DE JUEGO 1
        self.cuadro_juego1 = ttk.Frame(self.container_juego, padding=15)
        self.cuadro_juego1.grid(row=0, column=0, sticky='nsew')
        self.cuadro_juego1.columnconfigure((0, 1, 2, 3), weight=1)

        self.modo_seleccionado = tk.StringVar(value=self.configuraciones_de_juego["tipo_partida"])
        self.dificultad_seleccionada = tk.StringVar(value=self.configuraciones_de_juego["dificultad"])
        self.dimensiones_seleccionadas = tk.StringVar(value=self.configuraciones_de_juego["dimensiones"])
        self.contador_tiempo = tk.IntVar()

        ttk.Label(self.cuadro_juego1, text="Modo:", font=("Courier", 16, "bold")).grid(column=0, row=0, sticky='w')
        ttk.Label(self.cuadro_juego1, textvariable=self.modo_seleccionado, font=("Courier", 14,)).grid(column=1, row=0, sticky='w')
        
        ttk.Label(self.cuadro_juego1, text="Dificultad:", font=("Courier", 16, "bold")).grid(column=0, row=1, sticky='w')
        ttk.Label(self.cuadro_juego1, textvariable=self.dificultad_seleccionada, font=("Courier", 14,)).grid(column=1, row=1, sticky='w')

        ttk.Label(self.cuadro_juego1, text="Dimensiones:", font=("Courier", 16, "bold")).grid(column=2, row=0, sticky='w')
        ttk.Label(self.cuadro_juego1, textvariable=self.dimensiones_seleccionadas, font=("Courier", 14,)).grid(column=3, row=0, sticky='w')

        ttk.Label(self.cuadro_juego1, text="Tiempo:", font=("Courier", 16, "bold")).grid(column=2, row=1, sticky='w')
        ttk.Label(self.cuadro_juego1, textvariable=self.contador_tiempo, font=("Courier", 14,)).grid(column=3, row=1, sticky='w')

        ttk.Button(self.cuadro_juego1, text="Iniciar", command=self.iniciar_partida, style='estilo_custom.TButton').grid(column=0, row=2, sticky='nsew')
        ttk.Button(self.cuadro_juego1, text="Reiniciar", command=self.reiniciar_partida, style='estilo_custom.TButton').grid(column=1, row=2, sticky='nsew')
        ttk.Button(self.cuadro_juego1, text="Auto completar", command=self.autocompletar_laberinto, style='estilo_custom.TButton').grid(column=2, row=2, sticky='nsew')
        ttk.Button(self.cuadro_juego1, text="Abandonar", command=self.abandonar_partida, style='estilo_custom.TButton').grid(column=3, row=2, sticky='nsew')

        # CUADRO | AREA DE JUEGO 2
        self.cuadro_juego2 = ttk.Frame(self.container_juego, relief="sunken")
        self.cuadro_juego2.grid(column=0, row=1, sticky='nsew')
        self.cuadro_juego2.columnconfigure(0, weight=1)
        self.cuadro_juego2.rowconfigure(0, weight=1)

        self.maze_canvas = tk.Canvas(self.cuadro_juego2, bg="lightgray", highlightthickness=0)
        self.maze_canvas.pack(fill="both", expand=True)

        # CUADRO | MENU DE JUEGO
        self.cuadro_menu = ttk.Frame(root, padding=15, relief="raised")
        self.cuadro_menu.grid(row=0, column=0, sticky='nsew')
        self.cuadro_menu.columnconfigure(0, weight=1)

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

        # Cargar datos iniciales
        self.dimensiones_dinamicas(None)
        self.guardar_configuraciones()
        self.ranking_en_memoria = self.cargar_rankings("archivos/rankings.txt")
        self.mostrar_ranking()

        # Vincular eventos
        self.root.bind("<Configure>", self.on_resize)
        self.root.bind("<Key>", self.handle_key_press)
        
    # FUNCIONES ___________________________________________________________________________________________________________________________

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
            print(f"Error: Archivo no encontrado en {ruta}")
            return None
        return laberinto

    def cargar_rankings(self, ruta):
        rankings = []
        try:
            with open(ruta, 'r') as archivo: 
                for linea in archivo:
                    linea = linea.strip()
                    if linea.startswith('#') or linea == '':
                        continue
                    fila = [valor for valor in linea.split(',')]
                    rankings.append(fila)
        except FileNotFoundError:
            print(f"Error: Archivo de ranking no encontrado en {ruta}")
            return []
        return rankings

    def mostrar_ranking(self):
        """Muestra los datos del ranking en el Treeview."""
        # Limpiar Treeview
        for item in self.ranking_treeview.get_children():
            self.ranking_treeview.delete(item)
        
        # Insertar nuevos datos
        for fila in self.ranking_en_memoria:
            self.ranking_treeview.insert("", "end", values=fila)

    def guardar_configuraciones(self):
        self.configuraciones_de_juego["tipo_partida"] = self.combo_partida.get()
        if self.combo_partida.get() == "Contra Tiempo":
            self.configuraciones_de_juego["tiempo"] = self.combo_tiempo.get()
        self.configuraciones_de_juego["dificultad"] = self.combo_dificultad.get()
        self.configuraciones_de_juego["dimensiones"] = self.combo_dimensiones.get()
        
        print("Las siguientes configuraciones fueron cargadas:")
        print(self.configuraciones_de_juego)
        
        ruta_laberinto = f"archivos/laberintos/{self.configuraciones_de_juego['dificultad']}/{self.configuraciones_de_juego['dimensiones']}.txt"
        self.laberinto_en_memoria = self.cargar_laberinto(ruta_laberinto)
        
        self.modo_seleccionado.set(self.configuraciones_de_juego["tipo_partida"])
        self.dificultad_seleccionada.set(self.configuraciones_de_juego["dificultad"])
        self.dimensiones_seleccionadas.set(self.configuraciones_de_juego["dimensiones"])
        print("Valores de área 1 modificados.")
        
        self.visualizar_laberinto()
        print("Laberinto cargado en la ventana.")

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

    def tiempo_partida_dinamico(self, evento):
        selected_type = self.combo_partida.get()
        if selected_type == "Contra Tiempo":
            self.etiqueta_tiempo.grid(row=3, column=0, sticky='w')
            self.combo_tiempo.grid(row=4, column=0, pady=(0, 5), sticky='nsew')
            self.combo_tiempo.set(2)
        else:
            self.etiqueta_tiempo.grid_forget()
            self.combo_tiempo.grid_forget()

    def visualizar_laberinto(self):
        if not self.laberinto_en_memoria:
            print("No hay laberinto cargado para visualizar.")
            return

        self.maze_canvas.delete("all")
        self.bloque_matrix.clear()

        ancho_cuadro = self.maze_canvas.winfo_width()
        alto_cuadro = self.maze_canvas.winfo_height()

        if ancho_cuadro <= 1 or alto_cuadro <= 1:
            self.maze_canvas.after(10, self.visualizar_laberinto)
            return

        filas = len(self.laberinto_en_memoria)
        columnas = len(self.laberinto_en_memoria[0])
        tamaño_celda = min(ancho_cuadro // columnas, alto_cuadro // filas)

        for r in range(filas):
            row_of_bloques = []
            for c in range(columnas):
                x1 = c * tamaño_celda
                y1 = r * tamaño_celda
                x2 = x1 + tamaño_celda
                y2 = y1 + tamaño_celda
                
                maze_value = self.laberinto_en_memoria[r][c]
                
                rect_id = self.maze_canvas.create_rectangle(x1, y1, x2, y2, outline="gray")
                
                new_bloque = bloque(self.maze_canvas, rect_id, r, c, maze_value)
                new_bloque.set_color(new_bloque.get_color())

                row_of_bloques.append(new_bloque)
                
                if maze_value == -1:
                    self.current_position = (r, c)

            self.bloque_matrix.append(row_of_bloques)
            
        self.draw_totem(self.current_position)

    def draw_totem(self, position):
        """Dibuja el tótem (un pequeño círculo) en un bloque dado."""
        self.maze_canvas.delete("totem")
        r, c = position
        
        cell_size = min(self.maze_canvas.winfo_width() // len(self.laberinto_en_memoria[0]), 
                        self.maze_canvas.winfo_height() // len(self.laberinto_en_memoria))
        
        x_center = c * cell_size + cell_size / 2
        y_center = r * cell_size + cell_size / 2
        
        totem_size = cell_size / 3
        
        x1 = x_center - totem_size
        y1 = y_center - totem_size
        x2 = x_center + totem_size
        y2 = y_center + totem_size
        
        self.totem_id = self.maze_canvas.create_oval(x1, y1, x2, y2, fill="blue", tags="totem")

    def handle_key_press(self, event):
        """Maneja las pulsaciones de tecla para mover el tótem."""
        if self.current_position is None:
            return

        r, c = self.current_position
        new_r, new_c = r, c
        
        if event.keysym == "Up":
            new_r -= 1
        elif event.keysym == "Down":
            new_r += 1
        elif event.keysym == "Left":
            new_c -= 1
        elif event.keysym == "Right":
            new_c += 1
            
        if (0 <= new_r < len(self.laberinto_en_memoria) and 
            0 <= new_c < len(self.laberinto_en_memoria[0]) and
            self.laberinto_en_memoria[new_r][new_c] != 1):
            
            old_bloque = self.bloque_matrix[r][c]
            if old_bloque.value == 0 and not old_bloque.is_visited:
                old_bloque.set_color("lightblue")
                old_bloque.is_visited = True
                
            self.current_position = (new_r, new_c)
            self.draw_totem(self.current_position)
            
            if self.laberinto_en_memoria[new_r][new_c] == 2:
                print("¡Has llegado al final!")
                self.maze_canvas.create_text(
                    self.maze_canvas.winfo_width() / 2,
                    self.maze_canvas.winfo_height() / 2,
                    text="¡Ganaste!", font=("Helvetica", 40, "bold"), fill="blue"
                )

    def on_resize(self, event):
        """Vuelve a dibujar el laberinto cuando se redimensiona la ventana."""
        self.root.after(1, self.visualizar_laberinto)

    def iniciar_partida(self):
        """Inicia la partida, permitiendo el movimiento del tótem."""
        self.guardar_configuraciones()
        self.maze_canvas.delete("all")
        self.visualizar_laberinto()
        self.draw_totem(self.current_position)
        print("Partida iniciada. Usa las flechas para moverte.")

    def reiniciar_partida(self):
        """Reinicia la partida con la configuración actual."""
        print("Reiniciando partida...")
        self.visualizar_laberinto()

    def autocompletar_laberinto(self):
        # Esta función requerirá un algoritmo de búsqueda de camino (e.g., A*)
        print("Función de auto-completar aún no implementada.")

    def abandonar_partida(self):
        # Esta función requerirá guardar el estado y/o volver al menú principal
        print("Partida abandonada. Volviendo al menú principal.")
        self.visualizar_laberinto()

if __name__ == "__main__":
    root = tk.Tk()
    app = juego_laberinto(root)
    root.mainloop()
