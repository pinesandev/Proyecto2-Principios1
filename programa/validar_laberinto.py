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

