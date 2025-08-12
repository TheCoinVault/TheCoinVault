from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage
import matplotlib.pyplot as plt
import numpy as np
import os
from io import BytesIO

# Asegurarse de que el backend de Matplotlib sea compatible con PyQt6
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import coin_data_manager

class MplCanvas(FigureCanvas):
    """Clase para incrustar un gráfico Matplotlib en una aplicación PyQt."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Asegurarse de que el color de fondo de la figura sea transparente
        # para evitar problemas de superposición con el fondo de PyQt.
        self.fig = Figure(figsize=(width, height), dpi=dpi, facecolor='none') 
        self.axes = self.fig.add_subplot(111)
        # Ocultar el marco del eje por defecto para una apariencia más limpia si no se usa.
        self.axes.set_frame_on(False) 
        super(MplCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.updateGeometry()

class StatisticsTab(QWidget):
    def __init__(self):
        super().__init__()
        # Inicializar atributos para los QLabel de KPI antes de init_ui
        self.kpi_value_unique_coins_label = QLabel("0")
        self.kpi_value_total_coins_label = QLabel("0")
        self.kpi_value_unique_countries_label = QLabel("0")

        self.init_ui()
        # Se llama a update_statistics al inicio para cargar los datos iniciales
        self.update_statistics()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)

        title_label = QLabel("Estadísticas de mi Colección")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px; color: #2C3E50;")
        main_layout.addWidget(title_label)

        # --- Sección de KPIs (Key Performance Indicators) ---
        kpi_layout = QHBoxLayout()
        kpi_layout.setSpacing(20) # Espacio entre los KPIs
        kpi_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Pasamos las referencias de los QLabel directamente
        self.kpi_unique_coins = self._create_kpi_widget("Total de Monedas Únicas", self.kpi_value_unique_coins_label, 'moneda_oro_kpi.png')
        self.kpi_total_coins = self._create_kpi_widget("Total General de Monedas", self.kpi_value_total_coins_label, 'moneda_plata_kpi.png')
        self.kpi_unique_countries = self._create_kpi_widget("Total de Países Distintos", self.kpi_value_unique_countries_label, 'moneda_bronce_kpi.png')

        kpi_layout.addWidget(self.kpi_unique_coins)
        kpi_layout.addWidget(self.kpi_total_coins)
        kpi_layout.addWidget(self.kpi_unique_countries)
        main_layout.addLayout(kpi_layout)

        # --- Área de Gráficos (Scrollable) ---
        chart_scroll_area = QScrollArea()
        chart_scroll_area.setWidgetResizable(True)
        chart_content_widget = QWidget()
        self.chart_layout = QVBoxLayout(chart_content_widget)
        self.chart_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.chart_layout.setSpacing(30) # Espacio entre gráficos
        chart_scroll_area.setWidget(chart_content_widget)
        main_layout.addWidget(chart_scroll_area)

        # Contenedores para los gráficos (Matplotlib Canvas)
        self.canvas_pais = MplCanvas(self, width=8, height=6, dpi=100)
        self.canvas_ceca = MplCanvas(self, width=8, height=6, dpi=100)
        self.canvas_estado = MplCanvas(self, width=8, height=6, dpi=100)
        self.canvas_desmonetizada = MplCanvas(self, width=8, height=6, dpi=100)
        self.canvas_tipo = MplCanvas(self, width=8, height=6, dpi=100)
        self.canvas_orientacion = MplCanvas(self, width=8, height=6, dpi=100)

        self.chart_layout.addWidget(self.canvas_pais)
        self.chart_layout.addWidget(self.canvas_ceca)
        self.chart_layout.addWidget(self.canvas_estado)
        self.chart_layout.addWidget(self.canvas_desmonetizada)
        self.chart_layout.addWidget(self.canvas_tipo)
        self.chart_layout.addWidget(self.canvas_orientacion)

        # Etiquetas para mostrar mensajes de "No hay datos"
        self.no_data_labels = {}
        chart_types = {
            "pais": self.canvas_pais, 
            "ceca": self.canvas_ceca, 
            "estado": self.canvas_estado, 
            "desmonetizada": self.canvas_desmonetizada, 
            "tipo": self.canvas_tipo, 
            "orientacion": self.canvas_orientacion
        }
        for chart_name, canvas_widget in chart_types.items():
            no_data_label = QLabel("No hay suficientes datos para este gráfico.")
            no_data_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data_label.setStyleSheet("font-size: 16px; color: gray; font-style: italic;")
            no_data_label.hide() # Oculto por defecto
            self.no_data_labels[chart_name] = no_data_label
            # Insertar la etiqueta debajo de su gráfico correspondiente
            self.chart_layout.insertWidget(self.chart_layout.indexOf(canvas_widget) + 1, no_data_label)


    def _create_kpi_widget(self, title, value_label_ref, icon_filename):
        """
        Crea un widget para un KPI (Key Performance Indicator).
        Ahora recibe directamente la referencia del QLabel para el valor.
        """
        kpi_widget = QWidget()
        kpi_layout = QVBoxLayout(kpi_widget)
        kpi_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Solo usamos estilos básicos de PyQt que son bien soportados
        kpi_widget.setStyleSheet(
            "background-color: #ECF0F1; border-radius: 10px; padding: 15px; min-width: 200px; max-width: 250px;"
        )

        icon_label = QLabel()
        icon_path = os.path.join('assets', icon_filename)
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                icon_label.setPixmap(pixmap.scaled(50, 50, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        kpi_layout.addWidget(icon_label)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #34495E; margin-top: 5px;")
        kpi_layout.addWidget(title_label)

        # Usar la referencia del QLabel que ya es un atributo de la clase
        value_label_ref.setAlignment(Qt.AlignmentFlag.AlignCenter)
        value_label_ref.setStyleSheet("font-size: 32px; font-weight: bold; color: #2980B9; margin-top: 5px;")
        kpi_layout.addWidget(value_label_ref)

        return kpi_widget

    def update_statistics(self):
        """Actualiza todos los KPIs y gráficos con los datos actuales de la colección."""
        
        # --- Actualizar KPIs ---
        self.kpi_value_unique_coins_label.setText(str(coin_data_manager.obtener_conteo_monedas_unicas()))
        self.kpi_value_total_coins_label.setText(str(coin_data_manager.obtener_conteo_monedas_total()))
        self.kpi_value_unique_countries_label.setText(str(coin_data_manager.obtener_conteo_paises_unicos()))

        # --- Actualizar Gráficos ---
        # Pasamos el Matplotlib Canvas.ax y el Matplotlib Canvas.fig al método de trazado
        self._plot_bar_chart(self.canvas_pais.axes, self.canvas_pais.fig, coin_data_manager.obtener_distribucion_por_pais(), 
                             "Distribución por País Emisor", "País", "Número de Monedas", 'pais')
        self._plot_bar_chart(self.canvas_ceca.axes, self.canvas_ceca.fig, coin_data_manager.obtener_distribucion_por_ceca(), 
                             "Distribución por Ceca", "Ceca", "Número de Monedas", 'ceca')
        self._plot_bar_chart(self.canvas_estado.axes, self.canvas_estado.fig, coin_data_manager.obtener_distribucion_por_estado_conservacion(), 
                             "Distribución por Estado de Conservación", "Estado", "Número de Monedas", 'estado')
        self._plot_pie_chart(self.canvas_desmonetizada.axes, self.canvas_desmonetizada.fig, coin_data_manager.obtener_distribucion_desmonetizacion(), 
                             "Monedas Desmonetizadas", 'desmonetizada')
        self._plot_bar_chart(self.canvas_tipo.axes, self.canvas_tipo.fig, coin_data_manager.obtener_distribucion_por_tipo(), 
                             "Distribución por Tipo de Moneda", "Tipo", "Número de Monedas", 'tipo')
        self._plot_bar_chart(self.canvas_orientacion.axes, self.canvas_orientacion.fig, coin_data_manager.obtener_distribucion_por_orientacion(), 
                             "Distribución por Orientación", "Orientación", "Número de Monedas", 'orientacion')


    def _plot_bar_chart(self, ax, fig, data, title, xlabel, ylabel, chart_name):
        """Dibuja un gráfico de barras."""
        ax.clear()
        if data:
            # Ordenar los datos por valor de mayor a menor para mejor visualización
            sorted_data = sorted(data.items(), key=lambda item: item[1], reverse=True)
            labels = [item[0] for item in sorted_data]
            values = [item[1] for item in sorted_data]

            ax.bar(labels, values, color='#3498DB') # Color azul
            ax.set_title(title)
            ax.set_xlabel(xlabel)
            ax.set_ylabel(ylabel)
            ax.tick_params(axis='x', rotation=45, ha='right') # Rotar etiquetas para que no se superpongan
            self.no_data_labels[chart_name].hide()
        else:
            ax.text(0.5, 0.5, "No hay datos para este gráfico.", horizontalalignment='center', 
                    verticalalignment='center', transform=ax.transAxes, fontsize=14, color='gray')
            self.no_data_labels[chart_name].show() # Mostrar etiqueta de no datos
        fig.tight_layout() # Ajustar el diseño para que no se superpongan los elementos
        fig.canvas.draw_idle() # Redibujar el canvas asociado a la figura

    def _plot_pie_chart(self, ax, fig, data, title, chart_name):
        """Dibuja un gráfico circular."""
        ax.clear()
        if data and sum(data.values()) > 0: # Asegurarse de que haya datos y que la suma sea mayor que 0
            labels = list(data.keys())
            values = list(data.values())
            
            # Colores bonitos para el gráfico circular
            colors = ['#2ECC71', '#E74C3C', '#F1C40F', '#9B59B6', '#3498DB', '#1ABC9C']
            
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors[:len(labels)])
            ax.set_title(title)
            ax.axis('equal') # Asegura que el círculo sea un círculo.
            self.no_data_labels[chart_name].hide()
        else:
            ax.text(0.5, 0.5, "No hay datos para este gráfico.", horizontalalignment='center', 
                    verticalalignment='center', transform=ax.transAxes, fontsize=14, color='gray')
            self.no_data_labels[chart_name].show() # Mostrar etiqueta de no datos
        fig.tight_layout()
        fig.canvas.draw_idle() # Redibujar el canvas asociado a la figura
