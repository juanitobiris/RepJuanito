import sys
import mysql.connector
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem
from datetime import datetime

# Configuración de la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="control_trabajo"
)
cursor = conexion.cursor()

# Crear tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS registros (
        id INT AUTO_INCREMENT PRIMARY KEY,
        fecha DATE NOT NULL,
        hora_inicio TIME,
        hora_fin TIME
    )
''')
conexion.commit()


class ControlTrabajo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Control de Trabajo")
        self.setGeometry(100, 100, 400, 300)

        self.boton_inicio = QPushButton("Iniciar Jornada")
        self.boton_inicio.clicked.connect(self.iniciar_jornada)

        self.boton_fin = QPushButton("Finalizar Jornada")
        self.boton_fin.clicked.connect(self.finalizar_jornada)

        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.setHorizontalHeaderLabels(["Fecha", "Hora Inicio", "Hora Fin"])

        layout = QVBoxLayout()
        layout.addWidget(self.boton_inicio)
        layout.addWidget(self.boton_fin)
        layout.addWidget(QLabel("Registros:"))
        layout.addWidget(self.tabla)
        self.setLayout(layout)

        self.mostrar_registros()

    def iniciar_jornada(self):
        fecha_actual = datetime.now().date()
        hora_actual = datetime.now().time().strftime('%H:%M:%S')
        cursor.execute("INSERT INTO registros (fecha, hora_inicio) VALUES (%s, %s)", (fecha_actual, hora_actual))
        conexion.commit()
        self.mostrar_registros()

    def finalizar_jornada(self):
        fecha_actual = datetime.now().date()
        hora_actual = datetime.now().time().strftime('%H:%M:%S')
        cursor.execute("UPDATE registros SET hora_fin = %s WHERE fecha = %s AND hora_fin IS NULL",
                       (hora_actual, fecha_actual))
        conexion.commit()
        self.mostrar_registros()

    def mostrar_registros(self):
        cursor.execute("SELECT fecha, hora_inicio, hora_fin FROM registros")
        registros = cursor.fetchall()
        self.tabla.setRowCount(len(registros))
        for i, registro in enumerate(registros):
            for j, dato in enumerate(registro):
                self.tabla.setItem(i, j, QTableWidgetItem(str(dato)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ControlTrabajo()
    ventana.show()
    sys.exit(app.exec())