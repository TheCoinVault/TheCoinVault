import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QTabWidget

# ---- INICIO DEL CÓDIGO DE LA COLECCIÓN ----
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

# ---- INICIO DEL CÓDIGO DE LA INTERFAZ ----
class TheCoinVaultApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('The Coin Vault')
        self.setGeometry(100, 100, 800, 600)  # (x, y, ancho, alto)
        
        # Creamos el widget de pestañas
        self.tabs = QTabWidget()
        
        # Creamos las pestañas individuales
        self.tab_coleccion = QWidget()
        self.tab_anadir = QWidget()
        self.tab_buscar = QWidget()
        self.tab_estadisticas = QWidget()

        # Añadimos las pestañas al widget de pestañas
        self.tabs.addTab(self.tab_coleccion, "Mi Colección")
        self.tabs.addTab(self.tab_anadir, "Añadir Moneda")
        self.tabs.addTab(self.tab_buscar, "Buscar Moneda")
        self.tabs.addTab(self.tab_estadisticas, "Estadísticas")

        # Configuramos el contenido de cada pestaña
        self.init_tab_coleccion()
        self.init_tab_anadir()
        self.init_tab_buscar()
        self.init_tab_estadisticas()

        # Creamos el layout principal de la ventana y añadimos las pestañas
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    # Métodos para inicializar el contenido de cada pestaña
    def init_tab_coleccion(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Aquí se mostrará tu colección de monedas."))
        self.tab_coleccion.setLayout(layout)

    def init_tab_anadir(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Aquí podrás añadir nuevas monedas."))
        self.tab_anadir.setLayout(layout)

    def init_tab_buscar(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Aquí podrás buscar monedas en tu colección."))
        self.tab_buscar.setLayout(layout)

    def init_tab_estadisticas(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Aquí verás estadísticas de tu colección."))
        self.tab_estadisticas.setLayout(layout)

# 2. El bloque principal para ejecutar la aplicación.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = TheCoinVaultApp()
    ventana.show()  # Muestra la ventana en pantalla
    sys.exit(app.exec())
