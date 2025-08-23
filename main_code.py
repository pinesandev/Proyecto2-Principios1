# IMPORTS / LIBRARIES
from tkinter import *
from tkinter import ttk

# FUNCIONES

# MAIN WINDOW CONFIG
ventana = Tk() # crear una instancia de una ventanta
ventana.title("LABERINTOS") # nombre de la ventana
ventana.geometry("600x400") # tamanho de la ventada
# ventana.resizable(False,False) # no se puede modificar el tamanho de la ventana

# ventana.columnconfigure(0, weight=1)
# ventana.rowconfigure(0, weight=1)
 
# FRAMES
# Menu
menu = ttk.Frame(ventana, padding=10)
menu.grid(column=0, row=0)

# Area de Juego
area_juego = ttk.Frame(ventana, padding=10)
area_juego.grid(column=1, row=0)

# Area de Juego
area_juego2 = ttk.Frame(ventana, padding=10)
area_juego2.grid(column=2, row=0)

# OBJECTS
ttk.Label(menu, text="Menu Principal de Juego").grid(column=0, row=0, sticky='nsew')
ttk.Button(menu, text="Jugar", command=ventana.destroy).grid(column=0, row=1, sticky='nsew')

ttk.Label(area_juego, text="testing").grid(column=0, row=0, sticky='nsew')

ttk.Label(area_juego2, text="testing2").grid(column=0, row=0, sticky='nsew')

ventana.mainloop()