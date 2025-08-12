from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QFormLayout, QDateEdit, QCheckBox, QMessageBox, QFileDialog, QSpinBox,
    QGridLayout, QSizePolicy, QScrollArea, QFrame 
)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
from PyQt6.QtGui import QPixmap 
import os 
import shutil 
import uuid 

import coin_data_manager

class AddCoinTab(QWidget):
    coin_added = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()
        # Rutas de las imágenes actualmente cargadas para la moneda
        self.current_anverso_path = ''
        self.current_reverso_path = ''
        self.current_bandera_path = ''
        self.current_escudo_path = ''

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setContentsMargins(50, 50, 50, 50)

        title_label = QLabel("Añadir Nueva Moneda a la Colección")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #2C3E50;")
        main_layout.addWidget(title_label)

        # Usar un QScrollArea para el formulario si es muy largo
        form_scroll_area = QScrollArea()
        form_scroll_area.setWidgetResizable(True)
        form_content_widget = QWidget()
        form_layout = QFormLayout(form_content_widget)
        # Ajustar el espaciado del formulario
        form_layout.setHorizontalSpacing(20)
        form_layout.setVerticalSpacing(10)
        form_scroll_area.setWidget(form_content_widget)
        
        self.fields = {} 

        # Definición de los campos EXÁCTAMENTE como en tu Excel, en orden
        # Usamos las constantes de coin_data_manager para las claves internas
        field_definitions = [
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

        for field_name, label_text, widget_type in field_definitions:
            label = QLabel(label_text)
            widget = None
            if widget_type == QLineEdit:
                widget = QLineEdit()
                widget.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")
            elif widget_type == QDateEdit: 
                widget = QDateEdit()
                widget.setCalendarPopup(True)
                widget.setDate(QDate.currentDate())
                widget.setDisplayFormat("yyyy-MM-dd")
                widget.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")
            elif widget_type == QCheckBox:
                widget = QCheckBox()
                widget.setText("Sí") # Etiqueta para el checkbox
                widget.setStyleSheet("margin-top: 5px; margin-bottom: 5px;")
            elif widget_type == QSpinBox:
                widget = QSpinBox()
                widget.setMinimum(1)
                widget.setMaximum(999999999) 
                widget.setValue(1)
                widget.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")
            
            if widget:
                self.fields[field_name] = widget
                form_layout.addRow(label, widget)
        
        main_layout.addWidget(form_scroll_area) 

        # Separador visual
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        separator1.setStyleSheet("margin-top: 20px; margin-bottom: 20px;")
        main_layout.addWidget(separator1)

        photos_section_label = QLabel("Imágenes de la Moneda:")
        photos_section_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 15px; color: #34495E;")
        main_layout.addWidget(photos_section_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Diseño mejorado para las imágenes: 2x2 grid
        image_grid_container = QWidget()
        image_grid_layout = QGridLayout(image_grid_container) 
        image_grid_layout.setSpacing(20) # Espaciado entre elementos de la cuadrícula
        image_grid_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Función auxiliar para añadir widgets de imagen
        def add_image_widget_to_grid(layout, row, col, label_text, image_key, path_attr_name, image_label_ref):
            v_layout = QVBoxLayout()
            label = QLabel(label_text)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-weight: bold; color: #555;")
            
            image_label = QLabel("No hay imagen")
            image_label.setFixedSize(160, 160) # Tamaño de previsualización un poco más grande
            image_label.setStyleSheet("border: 2px dashed #D3D3D3; background-color: #FAFAFA; border-radius: 8px; font-style: italic; color: #888;")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            setattr(self, image_label_ref, image_label) # Guarda la referencia al QLabel

            button = QPushButton(f"Cargar {label_text.split()[0]}")
            button.setStyleSheet("""
                QPushButton {
                    background-color: #5DADE2; /* Azul claro */
                    color: white;
                    padding: 8px 15px;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #3498DB; /* Azul más oscuro al pasar el ratón */
                }
            """)
            button.clicked.connect(lambda: self.load_and_copy_image(image_label, image_key, path_attr_name))

            v_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
            v_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
            v_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.addLayout(v_layout, row, col)

        # Posicionamiento en la cuadrícula (dos filas de dos columnas para las 4 imágenes)
        add_image_widget_to_grid(image_grid_layout, 0, 0, "Foto Anverso", coin_data_manager.CAMPO_FOTO_ANVERSO, "current_anverso_path", "anverso_image")
        add_image_widget_to_grid(image_grid_layout, 0, 1, "Foto Reverso", coin_data_manager.CAMPO_FOTO_REVERSO, "current_reverso_path", "reverso_image")
        add_image_widget_to_grid(image_grid_layout, 1, 0, "Foto Bandera", coin_data_manager.CAMPO_FOTO_BANDERA, "current_bandera_path", "bandera_image")
        add_image_widget_to_grid(image_grid_layout, 1, 1, "Foto Escudo", coin_data_manager.CAMPO_FOTO_ESCUDO, "current_escudo_path", "escudo_image")
        
        main_layout.addWidget(image_grid_container)

        # Separador visual
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        separator2.setStyleSheet("margin-top: 20px; margin-bottom: 20px;")
        main_layout.addWidget(separator2)

        save_button = QPushButton("Guardar Moneda")
        save_button.clicked.connect(self.save_coin)
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; /* Verde */
                color: white;
                padding: 12px 25px;
                border: none;
                border-radius: 8px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)
        main_layout.addWidget(save_button, alignment=Qt.AlignmentFlag.AlignCenter)

    def load_and_copy_image(self, image_label_widget, field_name_key, path_attr_name):
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
            # Generar un nombre de archivo único para evitar colisiones
            unique_filename = f"{uuid.uuid4().hex}_{os.path.basename(file_path)}"
            destination_path = os.path.join(initial_dir, unique_filename)

            try:
                shutil.copyfile(file_path, destination_path)
            except Exception as e:
                QMessageBox.critical(self, "Error de Copia", f"No se pudo copiar el archivo: {e}")
                return

            # Almacenar la ruta relativa
            relative_path = os.path.relpath(destination_path, os.path.dirname(os.path.abspath(__file__)))

            # Mostrar la imagen en el QLabel
            pixmap = QPixmap(destination_path)
            if not pixmap.isNull():
                image_label_widget.setPixmap(pixmap.scaled(image_label_widget.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)) 
                image_label_widget.setText("") # Borrar texto si la imagen se carga
                image_label_widget.setStyleSheet("border: 2px solid #5DADE2; border-radius: 8px;") # Borde azul al cargar
                
                # Actualizar la ruta en el atributo de la instancia
                setattr(self, path_attr_name, relative_path)
            else:
                QMessageBox.warning(self, "Error de Carga", "No se pudo cargar la imagen seleccionada. Formato inválido o archivo corrupto.")
                image_label_widget.setText("Error")
                image_label_widget.setStyleSheet("border: 2px dashed #E74C3C; background-color: #FAE0E0; border-radius: 8px; color: #E74C3C;")
                setattr(self, path_attr_name, '') # Limpiar la ruta si falla

    def save_coin(self):
        coin_data = {}
        for field_name, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                value = widget.text().strip()
                # Conversión de tipos para campos numéricos y años
                if field_name in [coin_data_manager.CAMPO_VALOR, coin_data_manager.CAMPO_PESO, 
                                  coin_data_manager.CAMPO_DIAMETRO, coin_data_manager.CAMPO_GROSOR]:
                    # Reemplazar coma por punto para conversión a float, y eliminar separadores de miles
                    value_cleaned = value.replace('.', '').replace(',', '.') 
                    if value_cleaned:
                        try:
                            coin_data[field_name] = float(value_cleaned)
                        except ValueError:
                            QMessageBox.warning(self, "Error de Datos", 
                                                f"Valor inválido para '{field_name.replace('_', ' ').title()}'. "
                                                "Por favor, introduzca un número válido (ej. 12,34 o 1.234,56).")
                            return 
                    else:
                        coin_data[field_name] = None
                elif field_name == coin_data_manager.CAMPO_ANO_ACUNACION:
                    if value.isdigit(): 
                        coin_data[field_name] = int(value)
                    elif value == "":
                        coin_data[field_name] = None
                    else:
                        QMessageBox.warning(self, "Error de Datos", 
                                            f"Valor inválido para '{field_name.replace('_', ' ').title()}'. "
                                            "Por favor, introduzca un año numérico válido (ej. 1971).")
                        return
                elif field_name == coin_data_manager.CAMPO_TIRADA:
                    # Eliminar puntos y comas para la tirada, asegurar entero
                    value_cleaned = value.replace('.', '').replace(',', '')
                    if value_cleaned.isdigit():
                        coin_data[field_name] = int(value_cleaned)
                    elif value_cleaned == "":
                        coin_data[field_name] = None
                    else:
                        QMessageBox.warning(self, "Error de Datos", 
                                            f"Valor inválido para '{field_name.replace('_', ' ').title()}'. "
                                            "Por favor, introduzca un número entero válido (ej. 73.641.000).")
                        return
                else: 
                    # Almacenar None si el campo de texto está vacío
                    coin_data[field_name] = value if value else None 
            elif isinstance(widget, QDateEdit):
                coin_data[field_name] = widget.date().toString("yyyy-MM-dd")
            elif isinstance(widget, QCheckBox):
                coin_data[field_name] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                coin_data[field_name] = widget.value()
        
        # Asignar las rutas de imagen almacenadas, asegurarse de que sean None si no se cargó ninguna
        coin_data[coin_data_manager.CAMPO_FOTO_ANVERSO] = self.current_anverso_path if self.current_anverso_path else None
        coin_data[coin_data_manager.CAMPO_FOTO_REVERSO] = self.current_reverso_path if self.current_reverso_path else None
        coin_data[coin_data_manager.CAMPO_FOTO_BANDERA] = self.current_bandera_path if self.current_bandera_path else None
        coin_data[coin_data_manager.CAMPO_FOTO_ESCUDO] = self.current_escudo_path if self.current_escudo_path else None

        try:
            # Aquí coin_data_manager.anadir_moneda se encargará de generar el ID único
            coin_data_manager.anadir_moneda(coin_data)
            QMessageBox.information(self, "Éxito", "✅ Moneda guardada correctamente.")
            self.clear_fields()
            self.coin_added.emit() 
        except Exception as e:
            QMessageBox.critical(self, "Error al Guardar", f"❌ Ocurrió un error al guardar la moneda: {e}")

    def clear_fields(self):
        """Limpia todos los campos del formulario y restablece las vistas de imagen."""
        for field_name, widget in self.fields.items():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QDateEdit):
                widget.setDate(QDate.currentDate())
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
            elif isinstance(widget, QSpinBox):
                widget.setValue(1) # Restablecer a 1
        
        # Limpiar y restablecer las etiquetas de imagen a su estado original
        self.anverso_image.clear()
        self.anverso_image.setText("No hay imagen")
        self.reverso_image.clear()
        self.reverso_image.setText("No hay imagen")
        self.bandera_image.clear()
        self.bandera_image.setText("No hay imagen")
        self.escudo_image.clear()
        self.escudo_image.setText("No hay imagen")
        
        # Restablecer el estilo por defecto de los QLabel de imagen
        default_image_style = "border: 2px dashed #D3D3D3; background-color: #FAFAFA; border-radius: 8px; font-style: italic; color: #888;"
        self.anverso_image.setStyleSheet(default_image_style)
        self.reverso_image.setStyleSheet(default_image_style)
        self.bandera_image.setStyleSheet(default_image_style)
        self.escudo_image.setStyleSheet(default_image_style)
        
        # Restablecer las rutas de imagen almacenadas
        self.current_anverso_path = ''
        self.current_reverso_path = ''
        self.current_bandera_path = ''
        self.current_escudo_path = ''
