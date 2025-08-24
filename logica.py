
# ---------------------------- FUNCIONES ----------------------------

# Como la logica del juego es independiente de la interfaz grafica, la descripcion de las funciones, asi como sus entradas, salidas y restricciones, se van a integrar en formato docstring, para poder acceder a ellas desde cualquier parte del programa con mas facilidad.
# Se accede con help(nombre_funcion)

# ---------------------------- CARGAR LABERINTO ---------------------------
def cargar_laberinto(ruta): # La ruta se elije en el UI cuando el usuario seleccione una dificultad

    ''' 
FUNCION PARA CARGAR LABERINTOS DESDE UN ARCHIVO DE TEXTO
E: Ruta al archivo de texto que contiene el laberinto seleccionada por el usuario en el UI
S: Devuelve una matriz que representa el laberinto seleccionado
R: - El archivo debe existir
- Debe contener solo valores validos (1, 2, 0 y -1)
- Filas y columnas deben tener la misma longitud
    ''' 

    laberinto = []
    with open(ruta, 'r') as archivo: # with abre y cierra el archivo automaticamente
        for linea in archivo:
            # Ignorar líneas que comienzan con '#' o espacio en blanco
            linea = linea.strip()
            if linea.startswith('#'):
                continue
            if linea == '': 
                continue
            fila = [int(celda) for celda in linea.strip().split()]
            laberinto.append(fila)
    return laberinto



