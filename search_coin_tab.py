from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QMessageBox, QDialog, QFormLayout, QDateEdit, QCheckBox, QSpinBox,
    QScrollArea, QFrame
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QPixmap 
import os 
import shutil 
import uuid 

import coin_data_manager 

class SearchCoinTab(QWidget):
    # Señal para notificar a la ventana principal que los datos han cambiado
    data_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_initial_data() # Cargar datos al iniciar la pestaña
        self.dialog = None # Referencia al diálogo de edición
        self.current_editing_coin_id = None # ID de la moneda que se está editando

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        main_layout.setContentsMargins(50, 50, 50, 50)

        title_label = QLabel("Buscar, Ver y Gestionar Monedas")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #2C3E50;")
        main_layout.addWidget(title_label)

        # Sección de búsqueda
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar por País, Año o Tipo:")
        search_label.setStyleSheet("font-size: 16px;")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ej. 'España', '1980', 'Euro'")
        self.search_input.setStyleSheet("padding: 8px; border-radius: 5px; border: 1px solid #ccc; font-size: 16px;")
        
        search_button = QPushButton("Buscar")
        search_button.clicked.connect(self.perform_search)
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #5DADE2; /* Azul claro */
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #3498DB; /* Azul más oscuro */
            }
        """)
        
        show_all_button = QPushButton("Mostrar Todas")
        show_all_button.clicked.connect(self.load_initial_data) # Recargar todos los datos
        show_all_button.setStyleSheet("""
            QPushButton {
                background-color: #7F8C8D; /* Gris */
                color: white;
                padding: 8px 15px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #6C7A89; 
            }
        """)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        search_layout.addWidget(show_all_button)
        main_layout.addLayout(search_layout)

        # Separador visual
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        separator1.setStyleSheet("margin-top: 15px; margin-bottom: 15px;")
        main_layout.addWidget(separator1)

        # Tabla de resultados
        self.results_table = QTableWidget()
        self.results_table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # Hacerla de solo lectura
        self.results_table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows) # Seleccionar filas completas
        self.results_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #D3D3D3;
                border-radius: 8px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #ECF0F1; /* Gris claro para el encabezado */
                padding: 5px;
                border-bottom: 1px solid #D3D3D3;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget::item:selected {
                background-color: #D6EAF8; /* Azul claro al seleccionar */
                color: black;
            }
        """)
        
        # Conectar el doble clic a la función de edición
        self.results_table.doubleClicked.connect(self.edit_selected_coin)
        main_layout.addWidget(self.results_table)

        # Botones de acción (Editar y Eliminar)
        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        edit_button = QPushButton("Editar Moneda Seleccionada")
        edit_button.clicked.connect(self.edit_selected_coin)
        edit_button.setStyleSheet("""
            QPushButton {
                background-color: #F39C12; /* Naranja */
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #E67E22;
            }
        """)

        delete_button = QPushButton("Eliminar Moneda Seleccionada")
        delete_button.clicked.connect(self.delete_selected_coin)
        delete_button.setStyleSheet("""
            QPushButton {
                background-color: #E74C3C; /* Rojo */
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #C0392B;
            }
        """)
        action_buttons_layout.addWidget(edit_button)
        action_buttons_layout.addWidget(delete_button)
        main_layout.addLayout(action_buttons_layout)
        
        # Inicializar la tabla con las columnas
        self.setup_table_headers()

    def setup_table_headers(self):
        # Mapeo de claves internas a nombres de columnas amigables para el usuario
        self.column_map = {
            coin_data_manager.CAMPO_CODIGO_UNICO: "Código Único",
            coin_data_manager.CAMPO_PAIS_EMISOR: "País Emisor",
            coin_data_manager.CAMPO_ANO_ACUNACION: "Año de Acuñación",
            coin_data_manager.CAMPO_TIPO: "Tipo",
            coin_data_manager.CAMPO_VALOR_NOMINAL: "Valor Nominal",
            coin_data_manager.CAMPO_UNIDAD_MONETARIA: "Unidad Monetaria",
            coin_data_manager.CAMPO_COMPOSICION: "Composición",
            coin_data_manager.CAMPO_ESTADO: "Estado",
            coin_data_manager.CAMPO_CANTIDAD: "Cantidad",
            # No mostrar todas las columnas por defecto para una vista concisa
            # Las demás se verán en el diálogo de edición
        }
        
        # Orden de las columnas en la tabla
        self.display_order_keys = [
            coin_data_manager.CAMPO_CODIGO_UNICO,
            coin_data_manager.CAMPO_PAIS_EMISOR,
            coin_data_manager.CAMPO_ANO_ACUNACION,
            coin_data_manager.CAMPO_TIPO,
            coin_data_manager.CAMPO_VALOR_NOMINAL,
            coin_data_manager.CAMPO_UNIDAD_MONETARIA,
            coin_data_manager.CAMPO_COMPOSICION,
            coin_data_manager.CAMPO_ESTADO,
            coin_data_manager.CAMPO_CANTIDAD,
        ]

        # Crear los encabezados de la tabla basados en el mapeo
        headers = [self.column_map[key] for key in self.display_order_keys]
        self.results_table.setColumnCount(len(headers))
        self.results_table.setHorizontalHeaderLabels(headers)
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch) # Ajustar al ancho

    def load_initial_data(self):
        """Carga y muestra todas las monedas en la tabla."""
        coin_data_manager.cargar_coleccion()
        self.display_results(coin_data_manager.mi_coleccion)
        self.search_input.clear() # Limpiar el campo de búsqueda

    def display_results(self, coins):
        """Muestra una lista de monedas en la tabla de resultados."""
        self.results_table.setRowCount(len(coins))
        for row_idx, coin in enumerate(coins):
            for col_idx, key in enumerate(self.display_order_keys):
                value = coin.get(key, "")
                if key == coin_data_manager.CAMPO_DESMONETIZADA:
                    item_value = "Sí" if value else "No"
                elif key == coin_data_manager.CAMPO_CANTIDAD and value is None:
                    item_value = "1" # Por defecto 1 si no está especificado
                else:
                    item_value = str(value) if value is not None else ""
                
                item = QTableWidgetItem(item_value)
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter) # Centrar texto
                self.results_table.setItem(row_idx, col_idx, item)
        self.data_changed.emit() # Emitir señal de que los datos han cambiado

    def perform_search(self):
        """Realiza una búsqueda basada en el texto de entrada y actualiza la tabla."""
        search_text = self.search_input.text().strip()
        if not search_text:
            self.load_initial_data() # Si no hay texto, mostrar todo
            return

        criterios = {}
        # Asumiendo que el usuario podría buscar por estos campos principales
        # Se buscará el texto en cualquiera de ellos (OR implícito por la implementación de buscar_monedas)
        criterios[coin_data_manager.CAMPO_PAIS_EMISOR] = search_text
        criterios[coin_data_manager.CAMPO_ANO_ACUNACION] = search_text
        criterios[coin_data_manager.CAMPO_TIPO] = search_text
        criterios[coin_data_manager.CAMPO_VALOR_NOMINAL] = search_text
        criterios[coin_data_manager.CAMPO_UNIDAD_MONETARIA] = search_text
        criterios[coin_data_manager.CAMPO_COMPOSICION] = search_text
        criterios[coin_data_manager.CAMPO_ESTADO] = search_text
        criterios[coin_data_manager.CAMPO_CECA] = search_text
        criterios[coin_data_manager.CAMPO_CANTO] = search_text


        found_coins = coin_data_manager.buscar_monedas(criterios)
        if found_coins:
            self.display_results(found_coins)
            QMessageBox.information(self, "Búsqueda Exitosa", f"Se encontraron {len(found_coins)} monedas.")
        else:
            self.results_table.setRowCount(0) # Limpiar tabla
            QMessageBox.information(self, "No se Encontraron Monedas", "No se encontraron monedas que coincidan con los criterios de búsqueda.")

    def get_selected_coin_id(self):
        """Retorna el código único de la moneda seleccionada en la tabla."""
        selected_rows = self.results_table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Ninguna Moneda Seleccionada", "Por favor, seleccione una moneda de la tabla para realizar esta acción.")
            return None
        
        row_index = selected_rows[0].row()
        # El código único siempre está en la primera columna (índice 0)
        coin_id_item = self.results_table.item(row_index, self.display_order_keys.index(coin_data_manager.CAMPO_CODIGO_UNICO))
        return coin_id_item.text() if coin_id_item else None

    def edit_selected_coin(self):
        """Abre un diálogo para editar la moneda seleccionada."""
        coin_id = self.get_selected_coin_id()
        if not coin_id:
            return

        coin_to_edit = coin_data_manager.obtener_moneda_por_id(coin_id)
        if not coin_to_edit:
            QMessageBox.critical(self, "Error", "No se pudo encontrar la moneda para editar.")
            return

        self.current_editing_coin_id = coin_id # Guardar el ID de la moneda que se está editando
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle(f"Editar Moneda: {coin_id}")
        self.dialog.setGeometry(100, 100, 800, 700) # Tamaño más grande para el diálogo
        
        dialog_main_layout = QVBoxLayout()
        self.dialog.setLayout(dialog_main_layout)

        dialog_scroll_area = QScrollArea()
        dialog_scroll_area.setWidgetResizable(True)
        dialog_content_widget = QWidget()
        dialog_form_layout = QFormLayout(dialog_content_widget)
        dialog_form_layout.setHorizontalSpacing(20)
        dialog_form_layout.setVerticalSpacing(10)
        dialog_scroll_area.setWidget(dialog_content_widget)
        
        self.edit_fields = {} # Para almacenar los widgets del diálogo de edición

        # Definición de todos los campos para edición, incluyendo fotos
        # Usamos TODAS las llaves para asegurar que todos los campos sean editables
        edit_field_definitions = [
            (coin_data_manager.CAMPO_PAIS_EMISOR, "País Emisor:", QLineEdit),
            (coin_data_manager.CAMPO_ANO_ACUNACION, "Año de Acuñación:", QLineEdit),
            (coin_data_manager.CAMPO_TIPO, "Tipo:", QLineEdit),
            (coin_data_manager.CAMPO_ANOS_DE_EMISION, "Años De Emisión:", QLineEdit),
            (coin_data_manager.CAMPO_VALOR, "Valor:", QLineEdit),
            (coin_data_manager.CAMPO_VALOR_NOMINAL, "Valor Nominal:", QLineEdit),
            (coin_data_manager.CAMPO_UNIDAD_MONETARIA, "Unidad monetaria:", QLineEdit),
            (coin_data_manager.CAMPO_COMPOSICION, "Composición:", QLineEdit),
            (coin_data_manager.CAMPO_PESO, "Peso:", QLineEdit),
            (coin_data_manager.CAMPO_DIAMETRO, "Diámetro:", QLineEdit),
            (coin_data_manager.CAMPO_GROSOR, "Grosor:", QLineEdit),
            (coin_data_manager.CAMPO_ORIENTACION, "Orientación:", QLineEdit),
            (coin_data_manager.CAMPO_DESMONETIZADA, "Desmonetizada:", QCheckBox),
            (coin_data_manager.CAMPO_CANTO, "Canto:", QLineEdit),
            (coin_data_manager.CAMPO_CECA, "Ceca:", QLineEdit),
            (coin_data_manager.CAMPO_TIRADA, "Tirada:", QLineEdit),
            (coin_data_manager.CAMPO_CANTIDAD, "Cantidad:", QSpinBox),
            (coin_data_manager.CAMPO_ESTADO, "Estado:", QLineEdit),
            (coin_data_manager.CAMPO_NOTA_IMPORTANTE, "Nota Importante:", QLineEdit),
        ]

        for field_name, label_text, widget_type in edit_field_definitions:
            label = QLabel(label_text)
            widget = None
            current_value = coin_to_edit.get(field_name)

            if widget_type == QLineEdit:
                widget = QLineEdit()
                widget.setText(str(current_value) if current_value is not None else "")
                widget.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")
            elif widget_type == QDateEdit:
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                if current_value:
                    widget.setDate(QDate.fromString(str(current_value), "yyyy-MM-dd"))
                else:
                    widget.setDate(QDate.currentDate())
                widget.setDisplayFormat("yyyy-MM-dd")
                widget.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")
            elif widget_type == QCheckBox:
                widget = QCheckBox()
                widget.setText("Sí")
                widget.setChecked(bool(current_value))
                widget.setStyleSheet("margin-top: 5px; margin-bottom: 5px;")
            elif widget_type == QSpinBox:
                widget = QSpinBox()
                widget.setMinimum(1)
                widget.setMaximum(999999999)
                widget.setValue(int(current_value) if isinstance(current_value, (int, float)) else 1)
                widget.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")
            
            if widget:
                self.edit_fields[field_name] = widget
                dialog_form_layout.addRow(label, widget)
        
        dialog_main_layout.addWidget(dialog_scroll_area)

        # Sección de fotos en el diálogo de edición
        dialog_separator_photos = QFrame()
        dialog_separator_photos.setFrameShape(QFrame.Shape.HLine)
        dialog_separator_photos.setFrameShadow(QFrame.Shadow.Sunken)
        dialog_separator_photos.setStyleSheet("margin-top: 15px; margin-bottom: 15px;")
        dialog_main_layout.addWidget(dialog_separator_photos)

        dialog_photos_label = QLabel("Imágenes:")
        dialog_photos_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px; color: #34495E;")
        dialog_main_layout.addWidget(dialog_photos_label, alignment=Qt.AlignmentFlag.AlignLeft)

        dialog_image_grid_container = QWidget()
        dialog_image_grid_layout = QGridLayout(dialog_image_grid_container)
        dialog_image_grid_layout.setSpacing(20)
        dialog_image_grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Atributos para almacenar las rutas de imagen en el diálogo de edición
        self.edit_anverso_path = coin_to_edit.get(coin_data_manager.CAMPO_FOTO_ANVERSO, '') or ''
        self.edit_reverso_path = coin_to_edit.get(coin_data_manager.CAMPO_FOTO_REVERSO, '') or ''
        self.edit_bandera_path = coin_to_edit.get(coin_data_manager.CAMPO_FOTO_BANDERA, '') or ''
        self.edit_escudo_path = coin_to_edit.get(coin_data_manager.CAMPO_FOTO_ESCUDO, '') or ''

        # Función auxiliar para añadir widgets de imagen en el diálogo
        def add_dialog_image_widget(layout, row, col, label_text, image_key, path_attr_name, image_label_ref):
            v_layout = QVBoxLayout()
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-weight: bold; color: #555;")
            
            image_label = QLabel("No hay imagen")
            image_label.setFixedSize(160, 160)
            image_label.setStyleSheet("border: 2px dashed #D3D3D3; background-color: #FAFAFA; border-radius: 8px; font-style: italic; color: #888;")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            setattr(self, image_label_ref, image_label)

            # Cargar la imagen existente si hay una ruta
            initial_path = getattr(self, path_attr_name)
            if initial_path and os.path.exists(initial_path):
                pixmap = QPixmap(initial_path)
                if not pixmap.isNull():
                    image_label.setPixmap(pixmap.scaled(image_label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                    image_label.setText("")
                    image_label.setStyleSheet("border: 2px solid #5DADE2; border-radius: 8px;")
                else:
                    image_label.setText("Error al cargar imagen")
                    image_label.setStyleSheet("border: 2px dashed #E74C3C; background-color: #FAE0E0; border-radius: 8px; color: #E74C3C;")


            button = QPushButton(f"Cambiar {label_text.split()[0]}")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #5DADE2;
                    color: white;
                    padding: 8px 15px;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3498DB;
                }
            """)
            button.clicked.connect(lambda: self.load_and_copy_image_for_edit(image_label, image_key, path_attr_name))

            v_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            v_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
            v_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addLayout(v_layout, row, col)

        add_dialog_image_widget(dialog_image_grid_layout, 0, 0, "Foto Anverso", coin_data_manager.CAMPO_FOTO_ANVERSO, "edit_anverso_path", "dialog_anverso_image")
        add_dialog_image_widget(dialog_image_grid_layout, 0, 1, "Foto Reverso", coin_data_manager.CAMPO_FOTO_REVERSO, "edit_reverso_path", "dialog_reverso_image")
        add_dialog_image_widget(dialog_image_grid_layout, 1, 0, "Foto Bandera", coin_data_manager.CAMPO_FOTO_BANDERA, "edit_bandera_path", "dialog_bandera_image")
        add_dialog_image_widget(dialog_image_grid_layout, 1, 1, "Foto Escudo", coin_data_manager.CAMPO_FOTO_ESCUDO, "edit_escudo_path", "dialog_escudo_image")

        dialog_main_layout.addWidget(dialog_image_grid_container)

        # Botones de guardar y cancelar en el diálogo
        dialog_buttons_layout = QHBoxLayout()
        dialog_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        save_edit_button = QPushButton("Guardar Cambios")
        save_edit_button.clicked.connect(self.save_edited_coin)
        save_edit_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        cancel_edit_button = QPushButton("Cancelar")
        cancel_edit_button.clicked.connect(self.dialog.reject)
        cancel_edit_button.setStyleSheet("""
            QPushButton {
                background-color: #7F8C8D;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 16px;
                margin-top: 15px;
            }
            QPushButton:hover {
                background-color: #6C7A89;
            }
        """)

        dialog_buttons_layout.addWidget(save_edit_button)
        dialog_buttons_layout.addWidget(cancel_edit_button)
        dialog_main_layout.addLayout(dialog_buttons_layout)

        self.dialog.exec() # Mostrar el diálogo de forma modal

    def load_and_copy_image_for_edit(self, image_label_widget, field_name_key, path_attr_name):
        # Asegurarse de que el directorio de destino exista
        initial_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'imagenes_monedas')
        os.makedirs(initial_dir, exist_ok=True)

        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            f"Seleccionar Archivo para {field_name_key.replace('_', ' ').title()}", 
            initial_dir,
            "Archivos de Imagen (*.png *.jpg *.jpeg *.gif *.bmp);;Todos los Archivos (*)", 
        )

        if file_path:
            # Generar un nombre de archivo único
            unique_filename = f"{uuid.uuid4().hex}_{os.path.basename(file_path)}"
            destination_path = os.path.join(initial_dir, unique_filename)

            try:
                shutil.copyfile(file_path, destination_path)
            except Exception as e:
                QMessageBox.critical(self, "Error de Copia", f"No se pudo copiar el archivo: {e}")
                return

            relative_path = os.path.relpath(destination_path, os.path.dirname(os.path.abspath(__file__)))

            # Actualizar la imagen en el QLabel del diálogo
            pixmap = QPixmap(destination_path)
            if not pixmap.isNull():
                image_label_widget.setPixmap(pixmap.scaled(image_label_widget.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
                image_label_widget.setText("")
                image_label_widget.setStyleSheet("border: 2px solid #5DADE2; border-radius: 8px;")
                # Almacenar la nueva ruta en el atributo del diálogo
                setattr(self, path_attr_name, relative_path)
            else:
                QMessageBox.warning(self, "Error de Carga", "No se pudo cargar la imagen seleccionada.")
                image_label_widget.setText("Error")
                image_label_widget.setStyleSheet("border: 2px dashed #E74C3C; background-color: #FAE0E0; border-radius: 8px; color: #E74C3C;")
                setattr(self, path_attr_name, '') # Limpiar la ruta si falla

    def save_edited_coin(self):
        """Guarda los cambios de la moneda editada."""
        if not self.current_editing_coin_id:
            QMessageBox.critical(self, "Error", "No hay moneda seleccionada para guardar.")
            return

        updated_data = {}
        for field_name, widget in self.edit_fields.items():
            if isinstance(widget, QLineEdit):
                value = widget.text().strip()
                # Conversión de tipos para campos numéricos y años, igual que en add_coin_tab
                if field_name in [coin_data_manager.CAMPO_VALOR, coin_data_manager.CAMPO_PESO, 
                                  coin_data_manager.CAMPO_DIAMETRO, coin_data_manager.CAMPO_GROSOR]:
                    value_cleaned = value.replace('.', '').replace(',', '.')
                    if value_cleaned:
                        try:
                            updated_data[field_name] = float(value_cleaned)
                        except ValueError:
                            QMessageBox.warning(self, "Error de Datos", 
                                                f"Valor inválido para '{field_name.replace('_', ' ').title()}'. "
                                                "Por favor, introduzca un número válido (ej. 12,34 o 1.234,56).")
                            return
                    else:
                        updated_data[field_name] = None
                elif field_name == coin_data_manager.CAMPO_ANO_ACUNACION:
                    if value.isdigit():
                        updated_data[field_name] = int(value)
                    elif value == "":
                        updated_data[field_name] = None
                    else:
                        QMessageBox.warning(self, "Error de Datos", 
                                            f"Valor inválido para '{field_name.replace('_', ' ').title()}'. "
                                            "Por favor, introduzca un año numérico válido (ej. 1971).")
                        return
                elif field_name == coin_data_manager.CAMPO_TIRADA:
                    value_cleaned = value.replace('.', '').replace(',', '')
                    if value_cleaned.isdigit():
                        updated_data[field_name] = int(value_cleaned)
                    elif value_cleaned == "":
                        updated_data[field_name] = None
                    else:
                        QMessageBox.warning(self, "Error de Datos", 
                                            f"Valor inválido para '{field_name.replace('_', ' ').title()}'. "
                                            "Por favor, introduzca un número entero válido (ej. 73.641.000).")
                        return
                else:
                    updated_data[field_name] = value if value else None
            elif isinstance(widget, QDateEdit):
                updated_data[field_name] = widget.date().toString("yyyy-MM-dd")
            elif isinstance(widget, QCheckBox):
                updated_data[field_name] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                updated_data[field_name] = widget.value()

        # Asegurarse de incluir las rutas de las fotos del diálogo
        updated_data[coin_data_manager.CAMPO_FOTO_ANVERSO] = self.edit_anverso_path if self.edit_anverso_path else None
        updated_data[coin_data_manager.CAMPO_FOTO_REVERSO] = self.edit_reverso_path if self.edit_reverso_path else None
        updated_data[coin_data_manager.CAMPO_FOTO_BANDERA] = self.edit_bandera_path if self.edit_bandera_path else None
        updated_data[coin_data_manager.CAMPO_FOTO_ESCUDO] = self.edit_escudo_path if self.edit_escudo_path else None

        try:
            success = coin_data_manager.actualizar_moneda(self.current_editing_coin_id, updated_data)
            if success:
                QMessageBox.information(self, "Éxito", "✅ Moneda actualizada correctamente.")
                self.dialog.accept() # Cerrar el diálogo
                self.load_initial_data() # Recargar la tabla para mostrar los cambios
            else:
                QMessageBox.warning(self, "Error", "No se pudo actualizar la moneda.")
        except Exception as e:
            QMessageBox.critical(self, "Error al Actualizar", f"❌ Ocurrió un error: {e}")

    def delete_selected_coin(self):
        """Elimina la moneda seleccionada de la colección."""
        coin_id = self.get_selected_coin_id()
        if not coin_id:
            return

        reply = QMessageBox.question(self, "Confirmar Eliminación", 
                                     f"¿Está seguro de que desea eliminar la moneda con Código Único: {coin_id}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            try:
                success = coin_data_manager.eliminar_moneda(coin_id)
                if success:
                    QMessageBox.information(self, "Éxito", "🗑️ Moneda eliminada correctamente.")
                    self.load_initial_data() # Recargar la tabla para reflejar la eliminación
                else:
                    QMessageBox.warning(self, "Error", "No se pudo eliminar la moneda.")
            except Exception as e:
                QMessageBox.critical(self, "Error al Eliminar", f"❌ Ocurrió un error: {e}")
