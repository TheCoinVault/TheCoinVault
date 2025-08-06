# 1. Creamos nuestra lista vacía para guardar la colección.
mi_coleccion = []

# 2. Creamos una variable para llevar el conteo de las monedas.
contador_monedas = 0

# 3. Definimos una función para generar el código único automáticamente.
def generar_codigo_unico(pais, anio):
    global contador_monedas
    contador_monedas += 1
    numero_correlativo = f"{contador_monedas:07d}"
    return f"{pais}-{anio}-{numero_correlativo}"

# 4. Definimos una función para añadir una moneda.
# Esta función recibe un diccionario con todos los datos de la moneda.
def anadir_moneda(datos_moneda):
    # Generamos el código único automáticamente.
    codigo_unico_generado = generar_codigo_unico(datos_moneda['pais_emisor'], datos_moneda['anio_acunacion'])
    
    # Asignamos el código único al diccionario de la moneda.
    datos_moneda['codigo_unico'] = codigo_unico_generado
    
    # Añadimos el diccionario a la lista de la colección.
    mi_coleccion.append(datos_moneda)
    print(f"✅ Moneda '{datos_moneda['valor_nominal_texto']}' de {datos_moneda['pais_emisor']} añadida. Código: {codigo_unico_generado}")

# 5. Creamos un diccionario con la información de la primera moneda.
moneda_1_datos = {
    "pais_emisor": "USA",
    "anio_acunacion": 1888,
    "tipo_moneda": "Dólar de plata Morgan",
    "anios_emision": "1878-1904, 1921",
    "valor_numerico": 1,
    "valor_nominal_texto": "Un Dólar",
    "unidad_monetaria": "Dólar",
    "composicion_material": "Plata 90%",
    "peso_g": 26.73,
    "diametro_mm": 38.1,
    "grosor_mm": 2.5,
    "orientacion": "Moneda",
    "desmonetizacion": "No",
    "tipo_canto": "Estriado",
    "ceca": "Philadelphia",
    "tirada": 19150000,
    "cantidad_en_coleccion": 1,
    "estado_conservacion": "VF (Very Fine)",
    "nota": "Moneda popular entre coleccionistas.",
    "foto_anverso": "url_anverso_1.jpg",
    "foto_reverso": "url_reverso_1.jpg",
    "foto_bandera": "url_bandera_usa.png",
    "foto_escudo": "url_escudo_usa.png"
}

# 6. Llamamos a la función `anadir_moneda` con el diccionario de la primera moneda.
anadir_moneda(moneda_1_datos)

# 7. Creamos otro diccionario para la segunda moneda.
moneda_2_datos = {
    "pais_emisor": "ARG",
    "anio_acunacion": 1993,
    "tipo_moneda": "Moneda de 1 peso",
    "anios_emision": "1992-Presente",
    "valor_numerico": 1,
    "valor_nominal_texto": "Un Peso",
    "unidad_monetaria": "Peso",
    "composicion_material": "Plata 90%",
    "peso_g": 6.35,
    "diametro_mm": 23,
    "grosor_mm": 2.2,
    "orientacion": "Moneda",
    "desmonetizacion": "No",
    "tipo_canto": "Estriado",
    "ceca": "Buenos Aires",
    "tirada": 50000000,
    "cantidad_en_coleccion": 1,
    "estado_conservacion": "EBC (Excelente)",
    "nota": "Moneda de uso corriente.",
    "foto_anverso": "url_anverso_2.jpg",
    "foto_reverso": "url_reverso_2.jpg",
    "foto_bandera": "url_bandera_arg.png",
    "foto_escudo": "url_escudo_arg.png"
}

# 8. Llamamos a la función `anadir_moneda` con el diccionario de la segunda moneda.
anadir_moneda(moneda_2_datos)

# 9. Mostramos el tamaño actual de nuestra colección.
print(f"\nMi colección tiene {len(mi_coleccion)} monedas.")