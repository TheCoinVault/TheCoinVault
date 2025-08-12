import json
import os
import uuid 

# Nombre del archivo de la colección
ARCHIVO_COLECCION = 'the_coin_vault_collection.json'

# Lista global para almacenar las monedas cargadas en memoria
mi_coleccion = []

# =========================================================================
# Definición de las CLAVES INTERNAS de los campos según el Excel del usuario
# Estas claves se usarán para almacenar y acceder a los datos de las monedas
# en los diccionarios Python y en el archivo JSON.
# =========================================================================
CAMPO_CODIGO_UNICO = 'codigo_unico'
CAMPO_PAIS_EMISOR = 'pais_emisor'
CAMPO_ANO_ACUNACION = 'ano_acunacion'
CAMPO_TIPO = 'tipo'
CAMPO_ANOS_DE_EMISION = 'anos_de_emision'
CAMPO_VALOR = 'valor'
CAMPO_VALOR_NOMINAL = 'valor_nominal'
CAMPO_UNIDAD_MONETARIA = 'unidad_monetaria'
CAMPO_COMPOSICION = 'composicion'
CAMPO_PESO = 'peso'
CAMPO_DIAMETRO = 'diametro'
CAMPO_GROSOR = 'grosor'
CAMPO_ORIENTACION = 'orientacion'
CAMPO_DESMONETIZADA = 'desmonetizada'
CAMPO_CANTO = 'canto'
CAMPO_CECA = 'ceca'
CAMPO_TIRADA = 'tirada'
CAMPO_CANTIDAD = 'cantidad'
CAMPO_ESTADO = 'estado'
CAMPO_NOTA_IMPORTANTE = 'nota_importante'
CAMPO_FOTO_ANVERSO = 'foto_anverso'
CAMPO_FOTO_REVERSO = 'foto_reverso'
CAMPO_FOTO_BANDERA = 'foto_bandera'
CAMPO_FOTO_ESCUDO = 'foto_escudo'


# Lista de todos los campos definidos, en el orden lógico para uso general
TODOS_LOS_CAMPOS_LLAVES = [
    CAMPO_CODIGO_UNICO,
    CAMPO_PAIS_EMISOR,
    CAMPO_ANO_ACUNACION,
    CAMPO_TIPO,
    CAMPO_ANOS_DE_EMISION,
    CAMPO_VALOR,
    CAMPO_VALOR_NOMINAL,
    CAMPO_UNIDAD_MONETARIA,
    CAMPO_COMPOSICION,
    CAMPO_PESO,
    CAMPO_DIAMETRO,
    CAMPO_GROSOR,
    CAMPO_ORIENTACION,
    CAMPO_DESMONETIZADA,
    CAMPO_CANTO,
    CAMPO_CECA,
    CAMPO_TIRADA,
    CAMPO_CANTIDAD,
    CAMPO_ESTADO,
    CAMPO_NOTA_IMPORTANTE,
    CAMPO_FOTO_ANVERSO,
    CAMPO_FOTO_REVERSO,
    CAMPO_FOTO_BANDERA,
    CAMPO_FOTO_ESCUDO,
]

# =========================================================================
# Funciones para la gestión de la colección (cargar, guardar, añadir, etc.)
# =========================================================================

def generar_codigo_unico(pais_emisor, ano_acunacion):
    """Genera un código único en formato personalizado (EJ: ALE-1971-000001)."""
    
    # Normalizar país: primeras 3 letras mayúsculas, sin espacios ni caracteres especiales
    # Si el país es None o vacío, usar "XXX"
    pais_prefix = "".join(filter(str.isalpha, str(pais_emisor))).upper()[:3] if pais_emisor else "XXX"
    
    # Año de acuñación: asegurar que sea un string de 4 dígitos. Si es None o no válido, usar "XXXX"
    ano_str = ""
    if isinstance(ano_acunacion, (int, float)):
        ano_str = str(int(ano_acunacion)) # Convertir a entero primero para eliminar decimales
    elif isinstance(ano_acunacion, str) and ano_acunacion.isdigit():
        ano_str = ano_acunacion
    
    if not ano_str or len(ano_str) != 4:
        ano_str = "XXXX"

    # Contar monedas existentes con ese prefijo y año actual de la MI_COLECCION
    # Esto asegura que el contador es correcto incluso para nuevas monedas.
    max_secuencial = 0
    # Iterar sobre una copia para evitar problemas si la colección se modifica
    for moneda in list(mi_coleccion): 
        current_id = str(moneda.get(CAMPO_CODIGO_UNICO, ""))
        parts = current_id.split('-')
        if len(parts) == 3: # Asegurarse de que el ID tiene el formato esperado
            existing_pais_prefix = parts[0]
            existing_ano_str = parts[1]
            existing_secuencial_str = parts[2]
            
            if existing_pais_prefix == pais_prefix and existing_ano_str == ano_str:
                try:
                    max_secuencial = max(max_secuencial, int(existing_secuencial_str))
                except ValueError:
                    pass # Ignorar si la parte secuencial no es un número válido
    
    secuencial = max_secuencial + 1 
    secuencial_str = f"{secuencial:06d}" # Asegurar 6 dígitos con ceros iniciales
    
    return f"{pais_prefix}-{ano_str}-{secuencial_str}"

def cargar_coleccion():
    """Carga la colección de monedas desde el archivo JSON."""
    global mi_coleccion
    if os.path.exists(ARCHIVO_COLECCION):
        with open(ARCHIVO_COLECCION, 'r', encoding='utf-8') as f:
            mi_coleccion = json.load(f)
    else:
        mi_coleccion = [] 

def guardar_coleccion():
    """Guarda la colección de monedas actual en el archivo JSON."""
    with open(ARCHIVO_COLECCION, 'w', encoding='utf-8') as f:
        json.dump(mi_coleccion, f, indent=4, ensure_ascii=False)

def anadir_moneda(moneda):
    """Añade una nueva moneda a la colección."""
    pais_emisor_val = moneda.get(CAMPO_PAIS_EMISOR, "")
    ano_acunacion_val = moneda.get(CAMPO_ANO_ACUNACION, "")
    
    # Asegurarse que ano_acunacion_val sea un tipo compatible para generar el ID
    if isinstance(ano_acunacion_val, str) and ano_acunacion_val.isdigit():
        ano_acunacion_val = int(ano_acunacion_val)
    elif not isinstance(ano_acunacion_val, int):
        ano_acunacion_val = None 

    moneda[CAMPO_CODIGO_UNICO] = generar_codigo_unico(pais_emisor_val, ano_acunacion_val)

    # Crear una nueva moneda con todas las llaves definidas, asegurando que existan
    nueva_moneda = {key: moneda.get(key) for key in TODOS_LOS_CAMPOS_LLAVES}
    mi_coleccion.append(nueva_moneda)
    guardar_coleccion()

def obtener_moneda_por_id(codigo_unico):
    """Busca y retorna una moneda por su código único."""
    for moneda in mi_coleccion:
        if moneda.get(CAMPO_CODIGO_UNICO) == codigo_unico:
            return moneda
    return None

def buscar_monedas(criterios):
    """
    Busca monedas en la colección basándose en los criterios proporcionados.
    Los criterios deben usar las claves internas (ej. 'pais_emisor').
    """
    resultados = []
    for moneda in mi_coleccion:
        coincide = True
        for key, value in criterios.items():
            moneda_value = moneda.get(key)
            if value is None or value == "": 
                continue

            moneda_value_str = str(moneda_value).lower() if moneda_value is not None else ""
            value_str = str(value).lower() if value is not None else ""

            if value_str not in moneda_value_str:
                coincide = False
                break
            
        if coincide:
            resultados.append(moneda)
    return resultados


def actualizar_moneda(codigo_unico, nuevos_datos):
    """
    Actualiza los datos de una moneda existente por su código único.
    nuevos_datos debe ser un diccionario con las claves internas actualizadas.
    """
    for i, moneda in enumerate(mi_coleccion):
        if moneda.get(CAMPO_CODIGO_UNICO) == codigo_unico:
            for key, value in nuevos_datos.items():
                mi_coleccion[i][key] = value
            guardar_coleccion()
            return True
    return False

def eliminar_moneda(codigo_unico):
    """Elimina una moneda de la colección por su código único."""
    global mi_coleccion
    initial_len = len(mi_coleccion)
    mi_coleccion = [moneda for moneda in mi_coleccion if moneda.get(CAMPO_CODIGO_UNICO) != codigo_unico]
    if len(mi_coleccion) < initial_len:
        guardar_coleccion()
        return True
    return False

# =========================================================================
# Funciones para el cálculo de estadísticas
# =========================================================================

def obtener_conteo_monedas_unicas():
    """Retorna el número de entradas de monedas únicas en la colección."""
    return len(mi_coleccion)

def obtener_conteo_monedas_total():
    """Retorna el total de monedas considerando la cantidad de cada una."""
    total = 0
    for moneda in mi_coleccion:
        cantidad = moneda.get(CAMPO_CANTIDAD, 1) 
        try:
            total += int(cantidad)
        except (ValueError, TypeError):
            total += 1 
    return total

def obtener_conteo_paises_unicos():
    """Retorna el número de países emisores únicos en la colección."""
    paises = set()
    for moneda in mi_coleccion:
        if moneda.get(CAMPO_PAIS_EMISOR): 
            paises.add(moneda[CAMPO_PAIS_EMISOR].lower())
    return len(paises)

def obtener_distribucion_por_pais():
    """Retorna un diccionario con la distribución de monedas por país emisor."""
    distribucion = {}
    for moneda in mi_coleccion:
        pais = moneda.get(CAMPO_PAIS_EMISOR) 
        if pais:
            distribucion[pais] = distribucion.get(pais, 0) + 1
    return distribucion

def obtener_distribucion_por_ceca():
    """Retorna un diccionario con la distribución de monedas por ceca."""
    distribucion = {}
    for moneda in mi_coleccion:
        ceca = moneda.get(CAMPO_CECA) 
        if ceca:
            distribucion[ceca] = distribucion.get(ceca, 0) + 1
    return distribucion

def obtener_distribucion_por_estado_conservacion():
    """Retorna un diccionario con la distribución de monedas por estado de conservación."""
    distribucion = {}
    for moneda in mi_coleccion:
        estado = moneda.get(CAMPO_ESTADO) 
        if estado:
            distribucion[estado] = distribucion.get(estado, 0) + 1
    return distribucion

def obtener_distribucion_desmonetizacion():
    """Retorna un diccionario con la distribución de monedas por estado de desmonetización."""
    distribucion = {"Sí": 0, "No": 0}
    for moneda in mi_coleccion:
        desmonetizada = moneda.get(CAMPO_DESMONETIZADA, False) 
        if desmonetizada:
            distribucion["Sí"] += 1
        else:
            distribucion["No"] += 1
    return distribucion

def obtener_distribucion_por_tipo():
    """Retorna un diccionario con la distribución de monedas por tipo."""
    distribucion = {}
    for moneda in mi_coleccion:
        tipo = moneda.get(CAMPO_TIPO) 
        if tipo:
            distribucion[tipo] = distribucion.get(tipo, 0) + 1
    return distribucion

def obtener_distribucion_por_orientacion():
    """Retorna un diccionario con la distribución de monedas por orientación."""
    distribucion = {}
    for moneda in mi_coleccion:
        orientacion = moneda.get(CAMPO_ORIENTACION) 
        if orientacion:
            distribucion[orientacion] = distribucion.get(orientacion, 0) + 1
    return distribucion
