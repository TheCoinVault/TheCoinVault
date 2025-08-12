from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon
import os
import sys
import uuid # Necesario para generar nombres de archivo únicos para imágenes

# Importar los módulos de las pestañas
from add_coin_tab import AddCoinTab
from collection_view_tab import CollectionViewTab
from search_coin_tab import SearchCoinTab
from statistics_tab import StatisticsTab
import coin_data_manager # Importar el módulo de gestión de datos de monedas

class TheCoinVaultApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Coin Vault - Gestión de Colección de Monedas")
        self.setGeometry(100, 100, 1200, 800) # Ajustar el tamaño inicial de la ventana
        # Establecer el ícono de la aplicación. Asegúrate de que 'icono_app.png' exista en la carpeta 'assets'.
        self.setWindowIcon(QIcon(os.path.join('assets', 'icono_app.png'))) 
        
        # Cargar la colección de monedas al iniciar la aplicación
        # Al reiniciar el proyecto, no habrá un archivo the_coin_vault_collection.json,
        # así que la colección se inicializará vacía.
        coin_data_manager.cargar_coleccion()
        
        self.init_ui()

    def init_ui(self):
        """Inicializa la interfaz de usuario, incluyendo las pestañas y sus conexiones."""
        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        # Establecer el orden correcto de las pestañas según lo solicitado
        self.tab_mi_coleccion = CollectionViewTab()
        self.tab_widget.addTab(self.tab_mi_coleccion, "Mi Colección")

        self.tab_anadir_moneda = AddCoinTab()
        self.tab_widget.addTab(self.tab_anadir_moneda, "Añadir Moneda")

        # Eliminado modify_delete_tab.py del constructor de TheCoinVaultApp
        # y de las pestañas porque ahora se manejará desde search_coin_tab.py
        
        self.tab_buscar_moneda = SearchCoinTab()
        self.tab_widget.addTab(self.tab_buscar_moneda, "Buscar Moneda")

        self.tab_estadisticas = StatisticsTab()
        self.tab_widget.addTab(self.tab_estadisticas, "Estadísticas")

        # Conectar señales para actualizar las tablas en otras pestañas
        # cuando se añaden, modifican o eliminan monedas.
        self.tab_anadir_moneda.coin_added.connect(self.update_all_tabs_data)
        # La señal de data_changed ahora viene de SearchCoinTab
        self.tab_buscar_moneda.data_changed.connect(self.update_all_tabs_data)

        # Cargar los datos iniciales en todas las pestañas después de que se hayan configurado.
        # Se usa QTimer.singleShot para diferir la ejecución ligeramente,
        # asegurando que la UI tenga tiempo de renderizarse completamente.
        self.update_all_tabs_data()

    def update_all_tabs_data(self):
        """
        Actualiza los datos en todas las pestañas que muestran la colección.
        Se usa QTimer.singleShot para evitar problemas de actualización durante
        la construcción inicial de la UI y para asegurar que los datos estén cargados.
        """
        QTimer.singleShot(100, self.tab_mi_coleccion.load_coins_to_table)
        QTimer.singleShot(100, self.tab_buscar_moneda.load_initial_data) 
        QTimer.singleShot(100, self.tab_estadisticas.update_statistics)


if __name__ == '__main__':
    # =====================================================================
    # Configuración inicial de directorios y archivos de marcador de posición
    # =====================================================================
    # Asegurarse de que el directorio 'assets' exista para los iconos/imágenes de la app y KPIs
    assets_dir = 'assets'
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)
    
    # Asegurarse de que el subdirectorio 'imagenes_monedas' exista dentro de 'assets'
    # Aquí se guardarán las imágenes de las monedas cargadas por el usuario.
    coin_images_dir = os.path.join(assets_dir, 'imagenes_monedas')
    if not os.path.exists(coin_images_dir):
        os.makedirs(coin_images_dir)

    # Rutas para los archivos de imagen de marcador de posición de KPIs y el icono de la app
    # Estos se crearán si no existen para evitar errores visuales al inicio.
    placeholder_paths = [
        os.path.join(assets_dir, 'icono_app.png'),
        os.path.join(assets_dir, 'moneda_oro_kpi.png'),
        os.path.join(assets_dir, 'moneda_plata_kpi.png'),
        os.path.join(assets_dir, 'moneda_bronce_kpi.png')
    ]
    
    for p_path in placeholder_paths:
        if not os.path.exists(p_path):
            try:
                # Intenta crear una imagen de marcador de posición usando Pillow.
                # Asegúrate de haber instalado Pillow (pip install Pillow).
                from PIL import Image
                # Crear una imagen muy pequeña de 1x1 píxel para que ocupe poco espacio
                img = Image.new('RGB', (1, 1), color = 'red') # Pequeño cuadro rojo
                img.save(p_path)
            except ImportError:
                print(f"Advertencia: La librería 'Pillow' no está instalada. No se pueden crear imágenes de marcador de posición para {p_path}.")
                print("Por favor, instala Pillow con: pip install Pillow")
            except Exception as e:
                print(f"Error al crear imagen de marcador de posición {p_path}: {e}")

    # =====================================================================
    # Inicio de la aplicación PyQt6
    # =====================================================================
    app = QApplication(sys.argv)
    ventana = TheCoinVaultApp()
    ventana.show()
    sys.exit(app.exec())
