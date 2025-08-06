import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QTabWidget,
    QLineEdit, QPushButton, QGridLayout, QMessageBox, QTextEdit, QHBoxLayout # Nuevas importaciones
)

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

# 10. Definimos una función para buscar monedas por país emisor Y año de acuñación (lógica).
def buscar_monedas(pais=None, anio=None):
    monedas_encontradas = []
    for moneda in mi_coleccion:
        # Comprobamos si el país coincide (si se proporcionó un país para buscar)
        pais_coincide = True
        if pais:
            if moneda["pais_emisor"].upper() != pais.upper():
                pais_coincide = False
        
        # Comprobamos si el año coincide (si se proporcionó un año para buscar)
        anio_coincide = True
        if anio:
            try:
                if moneda["anio_acunacion"] != int(anio):
                    anio_coincide = False
            except ValueError:
                # Si el año en el campo no es un número válido, no coincide
                anio_coincide = False

        # Si ambos criterios coinciden (o no se especificaron), añadimos la moneda
        if pais_coincide and anio_coincide:
            monedas_encontradas.append(moneda)
    return monedas_encontradas

# ---- INICIO DEL CÓDIGO DE LA INTERFAZ ----
class TheCoinVaultApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('The Coin Vault')
        self.setGeometry(100, 100, 800, 600)  # (x, y, ancho, alto)
        
        self.tabs = QTabWidget()
        
        self.tab_coleccion = QWidget()
        self.tab_anadir = QWidget()
        self.tab_buscar = QWidget()
        self.tab_estadisticas = QWidget()

        self.tabs.addTab(self.tab_coleccion, "Mi Colección")
        self.tabs.addTab(self.tab_anadir, "Añadir Moneda")
        self.tabs.addTab(self.tab_buscar, "Buscar Moneda")
        self.tabs.addTab(self.tab_estadisticas, "Estadísticas")

        self.init_tab_coleccion()
        self.init_tab_anadir()
        self.init_tab_buscar() 
        self.init_tab_estadisticas()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        self.setLayout(main_layout)

    def init_tab_coleccion(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Aquí se mostrará tu colección de monedas."))
        self.tab_coleccion.setLayout(layout)

    def init_tab_anadir(self):
        grid_layout = QGridLayout()

        self.campos_anadir = {}
        campos_a_mostrar = [
            ("País Emisor (3 letras):", "pais_emisor"),
            ("Año de Acuñación:", "anio_acunacion"),
            ("Tipo de Moneda:", "tipo_moneda"),
            ("Años de Emisión:", "anios_emision"),
            ("Valor Numérico:", "valor_numerico"),
            ("Valor Nominal (Texto):", "valor_nominal_texto"),
            ("Unidad Monetaria:", "unidad_monetaria"),
            ("Composición Material:", "composicion_material"),
            ("Peso (g):", "peso_g"),
            ("Diámetro (mm):", "diametro_mm"),
            ("Grosor (mm):", "grosor_mm"),
            ("Orientación:", "orientacion"),
            ("Desmonetización:", "desmonetizacion"),
            ("Tipo de Canto:", "tipo_canto"),
            ("Casa de la Moneda (Ceca):", "ceca"),
            ("Tirada:", "tirada"),
            ("Cantidad en mi Colección:", "cantidad_en_coleccion"),
            ("Estado de Conservación:", "estado_conservacion"),
            ("Nota:", "nota"),
            ("Foto Anverso (URL):", "foto_anverso"),
            ("Foto Reverso (URL):", "foto_reverso"),
            ("Foto Bandera País (URL):", "foto_bandera"),
            ("Foto Escudo País (URL):", "foto_escudo")
        ]

        row = 0
        for label_text, field_name in campos_a_mostrar:
            label = QLabel(label_text)
            line_edit = QLineEdit(self)
            self.campos_anadir[field_name] = line_edit
            grid_layout.addWidget(label, row, 0)
            grid_layout.addWidget(line_edit, row, 1)
            row += 1

        btn_anadir = QPushButton("Añadir Moneda")
        btn_limpiar = QPushButton("Limpiar Campos")

        btn_anadir.clicked.connect(self.procesar_anadir_moneda)
        btn_limpiar.clicked.connect(self.limpiar_campos_anadir)

        grid_layout.addWidget(btn_anadir, row, 0)
        grid_layout.addWidget(btn_limpiar, row, 1)

        self.tab_anadir.setLayout(grid_layout)

    def init_tab_buscar(self):
        layout = QVBoxLayout() # Layout principal de la pestaña de búsqueda

        # Campo de entrada para el país a buscar
        search_pais_layout = QHBoxLayout() # Layout horizontal para el campo y el botón
        search_pais_label = QLabel("Buscar por País Emisor:")
        self.search_pais_input = QLineEdit(self) # Campo donde el usuario escribirá el país
        search_pais_layout.addWidget(search_pais_label)
        search_pais_layout.addWidget(self.search_pais_input)
        layout.addLayout(search_pais_layout) # Añadimos el layout horizontal al layout principal

        # Campo de entrada para el año a buscar (NUEVO)
        search_anio_layout = QHBoxLayout()
        search_anio_label = QLabel("Buscar por Año de Acuñación:")
        self.search_anio_input = QLineEdit(self) # Campo donde el usuario escribirá el año
        search_anio_layout.addWidget(search_anio_label)
        search_anio_layout.addWidget(self.search_anio_input)
        layout.addLayout(search_anio_layout)

        # Botón de búsqueda
        btn_buscar = QPushButton("Buscar Monedas")
        layout.addWidget(btn_buscar)

        # Área para mostrar los resultados
        self.search_results_area = QTextEdit(self)
        self.search_results_area.setReadOnly(True) # Hacemos que el área de texto sea de solo lectura
        layout.addWidget(self.search_results_area)

        # Conectamos el botón de búsqueda a la función que procesará la búsqueda
        btn_buscar.clicked.connect(self.procesar_busqueda_moneda)

        self.tab_buscar.setLayout(layout)

    def init_tab_estadisticas(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Aquí verás estadísticas de tu colección."))
        self.tab_estadisticas.setLayout(layout)

    # --- Funciones para manejar la interacción de la interfaz ---
    def procesar_anadir_moneda(self):
        datos_nueva_moneda = {}
        for field_name, line_edit in self.campos_anadir.items():
            datos_nueva_moneda[field_name] = line_edit.text()
        
        if not datos_nueva_moneda.get("pais_emisor") or not datos_nueva_moneda.get("anio_acunacion"):
            QMessageBox.warning(self, "Error de Entrada", "Los campos 'País Emisor' y 'Año de Acuñación' son obligatorios.")
            return

        try:
            datos_nueva_moneda['anio_acunacion'] = int(datos_nueva_moneda['anio_acunacion'])
            datos_nueva_moneda['valor_numerico'] = float(datos_nueva_moneda['valor_numerico']) if datos_nueva_moneda['valor_numerico'] else 0.0
            datos_nueva_moneda['peso_g'] = float(datos_nueva_moneda['peso_g']) if datos_nueva_moneda['peso_g'] else 0.0
            datos_nueva_moneda['diametro_mm'] = float(datos_nueva_moneda['diametro_mm']) if datos_nueva_moneda['diametro_mm'] else 0.0
            datos_nueva_moneda['grosor_mm'] = float(datos_nueva_moneda['grosor_mm']) if datos_nueva_moneda['grosor_mm'] else 0.0
            datos_nueva_moneda['tirada'] = int(datos_nueva_moneda['tirada']) if datos_nueva_moneda['tirada'] else 0
            datos_nueva_moneda['cantidad_en_coleccion'] = int(datos_nueva_moneda['cantidad_en_coleccion']) if datos_nueva_moneda['cantidad_en_coleccion'] else 0
        except ValueError:
            QMessageBox.critical(self, "Error de Formato", "Por favor, introduce valores numéricos válidos para los campos correspondientes (Año, Valor Numérico, Peso, Diámetro, Grosor, Tirada, Cantidad).")
            return

        anadir_moneda(datos_nueva_moneda)
        QMessageBox.information(self, "Moneda Añadida", "¡La moneda ha sido añadida a tu colección!")
        self.limpiar_campos_anadir()

    def procesar_busqueda_moneda(self):
        pais_a_buscar = self.search_pais_input.text() # Obtenemos el texto del campo de país
        anio_a_buscar = self.search_anio_input.text() # Obtenemos el texto del campo de año (NUEVO)

        # Si ambos campos están vacíos, mostramos una advertencia
        if not pais_a_buscar and not anio_a_buscar:
            QMessageBox.warning(self, "Búsqueda Vacía", "Por favor, introduce al menos un País Emisor o un Año de Acuñación para buscar.")
            return

        # Llamamos a nuestra función de lógica de búsqueda con ambos parámetros
        monedas_encontradas = buscar_monedas(pais=pais_a_buscar, anio=anio_a_buscar)
        
        self.search_results_area.clear() # Limpiamos el área de resultados antes de mostrar nuevos
        
        if monedas_encontradas:
            self.search_results_area.append(f"Se encontraron {len(monedas_encontradas)} monedas con los criterios especificados:\n")
            for moneda in monedas_encontradas:
                self.search_results_area.append(f"- Código: {moneda['codigo_unico']}, Tipo: {moneda['tipo_moneda']}, Año: {moneda['anio_acunacion']}, País: {moneda['pais_emisor']}")
        else:
            self.search_results_area.append(f"No se encontraron monedas con los criterios especificados.")


    def limpiar_campos_anadir(self):
        for line_edit in self.campos_anadir.values():
            line_edit.clear()

# 2. El bloque principal para ejecutar la aplicación.
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = TheCoinVaultApp()
    ventana.show()  # Muestra la ventana en pantalla
    sys.exit(app.exec())