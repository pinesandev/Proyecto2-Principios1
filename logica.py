import time

# ---------------------------- FUNCIONES ----------------------------

# Como la logica del juego es independiente de la interfaz grafica, la descripcion de las funciones, asi como sus entradas, salidas y restricciones, 
# se van a integrar en formato docstring, para poder acceder a ellas desde cualquier parte del programa con mas facilidad.
# Se accede con help(nombre_funcion)

# ---------------------------- CARGAR LABERINTO ---------------------------
def cargar_laberinto(ruta): # La ruta se elije en el UI cuando el usuario seleccione una dificultad

    ''' 
FUNCION PARA CARGAR LABERINTOS DESDE UN ARCHIVO DE TEXTO
E: Ruta al archivo de texto que contiene el laberinto seleccionada por el usuario en el UI
S: Devuelve una matriz que representa el laberinto seleccionado
R: El archivo debe existir
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
            fila = [int(celda) for celda in linea.split(',')]
            laberinto.append(fila)
    return laberinto

laberinto = cargar_laberinto('/Users/johel/Desktop/Johel/Johel/TEC Johel/Principios de Progra/Proyectos/Proyecto2-Principios1/archivos/laberintos/Fácil/8x8.txt')

# ---------------------------- VALIDAR MATRIZ ---------------------------
def validar_laberinto(matriz):

    ''' 
FUNCION PARA VALIDAR QUE LA MATRIZ CARGADA CONTENGA UN LABERINTO VALIDO
E: Matriz que se retorna de la funcion cargar_laberinto
S: Un diccionario con pares de clave-valor que indican si el laberinto es valido o no, y en caso de no serlo, el error que se encontro:
    {
        "valido": True/False,
        "mensaje": str,
        "cantidad_filas": int,
        "cantidad_columnas": int,
        "posicion_inicio": (fila, columna) o None,
        "posicion_meta": (fila, columna) o None
        
    }
R: - Todas las filas deben tener la misma cantidad de columnas.
    - Solo se permiten valores: -1 (INICIO), 0 (CAMINO), 1 (PARED), 2 (META).
    - Debe existir al menos y exactamente UN inicio (-1) y UNA meta (2).
    '''

    # Validar que la matriz no este vacia y exista al menos una fila y una columna

    cantidad_filas = len(matriz)
    cantidad_columnas = len(matriz[0]) # Se toma de standard la cantidad de columnas de la primera fila

    if matriz is None or cantidad_filas == 0 or cantidad_columnas == 0:
        return {
            "valido": False,
            "mensaje": "La matriz esta vacia o es invalida.",
            "cantidad_filas": 0,
            "cantidad_columnas": 0,
            "posicion_inicio": None,
            "posicion_meta": None
        }

    # Validar que todas las filas tengan la misma cantidad de columnas

    for indice_fila in range(cantidad_filas):
        if len(matriz[indice_fila]) != cantidad_columnas:
            return {
                "valido": False,
                "mensaje": "Todas las filas deben tener la misma cantidad de columnas.",
                "cantidad_filas": cantidad_filas,
                "cantidad_columnas": cantidad_columnas,
                "posicion_inicio": None,
                "posicion_meta": None
            }
    
    # Validar que solo existan los valores permitidos, una sola posicion de inicio y una sola posicion de meta

    valores_permitidos = {-1, 0, 1, 2} # Se instancia un set con los valores permitidos del laberinto
    posicion_inicio = None
    posicion_meta = None
    cantidad_inicios = 0
    cantidad_metas = 0

    # Se obtiene cada elemento de la matriz para validarlo despues
    for indice_fila in range(cantidad_filas):
        for indice_columna in range(cantidad_columnas):
            elemento = matriz[indice_fila][indice_columna] 
            if elemento not in valores_permitidos: 
                return {
                    "valido": False,
                    "mensaje": f"Valor invalido {elemento} en la posicion ({indice_fila}, {indice_columna}). Solo se permiten los valores: -1 (INICIO), 0 (CAMINO), 1 (PARED), 2 (META).",
                    "cantidad_filas": cantidad_filas,
                    "cantidad_columnas": cantidad_columnas,
                    "posicion_inicio": None,
                    "posicion_meta": None
                }
            
            # Se encuentra y establece la posicion de inicio
            if elemento == -1:
                cantidad_inicios += 1
                posicion_inicio = (indice_fila, indice_columna)

            # Se encuentra y establece la meta
            if elemento == 2:
                cantidad_metas += 1
                posicion_meta = (indice_fila, indice_columna)

    # Validar que exista un inicio y una meta
    if cantidad_metas == 0 and cantidad_inicios == 0:
        return {
            "valido": False,
            "mensaje": "Debe existir exactamente UN inicio (-1) y UNA meta (2). No se encontraron inicios ni metas.",
            "cantidad_filas": cantidad_filas,
            "cantidad_columnas": cantidad_columnas,
            "posicion_inicio": None,
            "posicion_meta": None
        }
    
    # Valida que exista unicamente un inicio
    if cantidad_inicios != 1:
        return {
            "valido": False,
            "mensaje": f"Debe existir exactamente UN inicio (-1). Se encontraron {cantidad_inicios} inicios.",
            "cantidad_filas": cantidad_filas,
            "cantidad_columnas": cantidad_columnas,
            "posicion_inicio": None,
            "posicion_meta": posicion_meta
        }
    
    # Valida que exista unicamente una meta
    if cantidad_metas != 1:
        return {
            "valido": False,
            "mensaje": f"Debe existir exactamente UNA meta (2). Se encontraron {cantidad_metas} metas.",
            "cantidad_filas": cantidad_filas,
            "cantidad_columnas": cantidad_columnas,
            "posicion_inicio": posicion_inicio,
            "posicion_meta": None
        }
    
    # Si pasa todas las validaciones, el laberinto es valido
    resultado = {
        "valido": True,
        "mensaje": "El laberinto es valido.",
        "cantidad_filas": cantidad_filas,
        "cantidad_columnas": cantidad_columnas,
        "posicion_inicio": posicion_inicio,
        "posicion_meta": posicion_meta
    }       
            
    return resultado



# ---------------------------- CARGAR RANKINGS ---------------------------
    '''
FUNCION PARA CARGAR RANKINGS DESDE UN ARCHIVO DE TEXTO
E: Ruta al archivo de texto que contiene los rankings
S: Devuelve una matriz con rankings 
R: El archivo debe existir
    ''' 

# ---------------------------- CARGAR RANKING ---------------------------

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

rankings = cargar_rankings('/Users/johel/Desktop/Johel/Johel/TEC Johel/Principios de Progra/Proyectos/Proyecto2-Principios1/archivos/rankings.txt')

# ---------------------------- FORMATO TIEMPO RANKING ---------------------------

def formatear_tiempo(string_tiempo):
    tiempo = time.strptime(string_tiempo, '%H:%M:%S')
    return tiempo.tm_hour*3600 + tiempo.tm_min*60 + tiempo.tm_sec

# ---------------------------- VALIDAR RANKING ---------------------------

def validar_ranking(rankings):

    # Misma cantidad de columnas en todas las filas 

    cantidad_filas = len(rankings)
    cantidad_columnas = len(rankings[0])

    for indice_fila in range(cantidad_filas):
        if len(rankings[indice_fila]) != cantidad_columnas:
                print(f'ERROR. Fila {indice_fila+1} debe tener solo 4 columnas.')
    
    # Se instancia un diccionario con las claves y sus valores para facil acceso 

    filas_validas = []
    for fila in rankings:
        valores_ranking = {
            'tiempo': fila[0],
            'nombre': fila[1],
            'dimensiones': fila[2],
            'movimientos': fila[3]
        }
    filas_validas.append(valores_ranking)
    print(filas_validas)


validar_ranking(rankings)




