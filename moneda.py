# Un diccionario se define con llaves {} y pares de clave: valor
moneda_de_muestra = {
    "codigo_unico": "USA-1888-SILVER",
    "pais_emisor": "Estados Unidos",
    "anio_acuñacion": 1888,
    "tipo_moneda": "Dólar de plata",
    "composicion_material": "Plata 90%",
    "peso_g": 26.73,
    "diametro_mm": 38.1,
    # AÑADE AQUÍ DOS NUEVOS CAMPOS DE TU LISTA
    "grosor_mm": 2.5,  # <- Ejemplo de nuevo campo
    "orientacion": "Moneda" # <- Otro ejemplo
}

# Para acceder a un valor, usamos la clave entre corchetes []
print("--- Detalles de la Moneda ---")
print("Código Único:", moneda_de_muestra["codigo_unico"])
print("País Emisor:", moneda_de_muestra["pais_emisor"])
print("Año:", moneda_de_muestra["anio_acuñacion"])
print("Composición:", moneda_de_muestra["composicion_material"])
print("Peso:", moneda_de_muestra["peso_g"], "g")
print("Diámetro:", moneda_de_muestra["diametro_mm"], "mm")
print("Grosor:", moneda_de_muestra["grosor_mm"], "mm") # <- Imprimimos el nuevo campo
print("Orientación:", moneda_de_muestra["orientacion"]) # <- Imprimimos el otro nuevo campo