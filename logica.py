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
        
    # Validar cap maximo de las dimensiones del laberinto
    if cantidad_filas > 20 or cantidad_columnas > 20:
        return {
                "valido": False,
                "mensaje": "No se permiten dimensiones mayores a 20x20",
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
    if cantidad_metas == 0 or cantidad_inicios == 0:
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

laberinto_valido = validar_laberinto(laberinto)

# ---------------------------- CARGAR RANKING ---------------------------
def cargar_rankings(ruta):
    '''
FUNCION PARA CARGAR RANKINGS DESDE UN ARCHIVO DE TEXTO
E: Ruta al archivo de texto que contiene los rankings
S: Devuelve una matriz con rankings 
R: El archivo debe existir

    '''
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
    segundos = tiempo.tm_hour*3600 + tiempo.tm_min*60 + tiempo.tm_sec
    return int(segundos)

# ---------------------------- VALIDAR RANKING ---------------------------
def validar_ranking(rankings):

    filas_validas = []
    errores = False # Acumulador de errores. En los testings se descubrio que usar continue, hace que si hay mas de un bug en una sola fila, solo se imprime el error del primer bug 

    # 1. Validar misma cantidad de columnas en todas las filas  
    for indice_fila in range(len(rankings)):
        fila = rankings[indice_fila]
        if len(fila) != 4: # ranking siempre va a ser de 4 columnas, por lo que podemos 'hardcode' 4 
            print(f'ERROR. Fila {indice_fila+1} debe tener solamente 4 columnas')
            errores = True
    
        # Columnas de valores de las filas de la matriz de rankings
        tiempo = fila[0]
        nombre = fila[1].strip().lower()
        dimensiones = fila[2].strip()
        movimientos = fila[3].strip()

        # 2. Validar que exista un formato de tiempo valido HH:MM:SS
        try:   
            horas, minutos, segundos = map(int, (tiempo.split(":"))) # map toma cada columna que devuelve split y lo transforma a int
            if horas < 0 or minutos < 0 or minutos > 59 or segundos < 0 or segundos > 59:
                print(f"ERROR: Tiempo invalido en {indice_fila+1}")  
                errores = True
        except ValueError:  # si en tiempo hay letras por ejemplo, se ejecuta el ValueError 
            print(f"ERROR: Tiempo invalido en {indice_fila+1}")
            errores = True
        
         # 3. Validar nombre correcto 
        if nombre == '':
            print(f"ERROR: Nombre vacio en fila {indice_fila+1}")
            errores = True  
        
        # 4. Validar dimensiones 
        if 'x' not in dimensiones:   
            print(f"ERROR: Dimension invalida en fila {indice_fila+1}")
            errores = True

        # Validar que las dimensiones sean solo de dos partes
        partes_dimensiones = dimensiones.split('x')
        if len(partes_dimensiones) != 2:
            print(f"ERROR: Dimensiones invalidas en fila {indice_fila+1}")
            errores = True

        fil, col = partes_dimensiones[0], partes_dimensiones[1]
        try:   # Valida que se puedan convertir las filas y columnas a int 
            fil = int(fil)
            col = int(col)
            if fil <= 0 or col <= 0:
                print(f"ERROR: Dimensiones invalidas en fila {indice_fila+1}")
                errores = True
        except ValueError:
            print(f"ERROR: Dimensiones invalidas en fila {indice_fila+1}")
            errores = True

        # 5. Validar movimientos 
        try:
            movimientos = int(movimientos)
            if movimientos <= 0:
                print(f"ERROR: Movimientos invalidos en fila {indice_fila+1}")
                errores = True
        except ValueError:
            print(f"ERROR: Movimientos invalidos en fila {indice_fila+1}")
            errores = True
        
        if errores:
            continue
            
        registro = {
            'tiempo': tiempo,
            'nombre': nombre.capitalize(),
            'dimensiones': dimensiones,
            'movimientos': movimientos,
            'segundos': formatear_tiempo(tiempo)
        }

        filas_validas.append(registro)

    return filas_validas

ranking_valido = validar_ranking(rankings)

# ---------------------------- ORDENAR RANKING ---------------------------
# FUNCION AUXILIAR 
def clave_segundos(fila):
    return fila["segundos"]

def ordenar_ranking(ranking_valido):

    # RANKEADO BURBUJA 
    # largo_ranking = len(ranking_valido)

    # for pasadas in range(largo_ranking):
    #     limite = largo_ranking - pasadas - 1    
                          
    #     for j in range(limite):
    #         tiempo_actual = ranking_valido[j]["segundos"]
    #         tiempo_siguiente = ranking_valido[j+1]["segundos"]

    #         if tiempo_actual > tiempo_siguiente:
                
    #             temp = ranking_valido[j]
    #             ranking_valido[j] = ranking_valido[j+1]
    #             ranking_valido[j+1] = temp

    ranking_valido.sort(key=clave_segundos)
    return ranking_valido

ranking_ordenado = ordenar_ranking(ranking_valido)
print(ranking_ordenado)
