import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QRadioButton, QButtonGroup, QLabel, QLineEdit, QPushButton,
    QComboBox
)
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from math import pi, cos, sin
import cmath as c


def Trig2Cart(modul, argument):
    x = modul * cos(argument)
    y = modul * sin(argument)
    return x + 1j * y


def DeseneazaLista(ListaZ, culoare='blue', marime=10):
    for z in ListaZ:
        x = z.real
        y = z.imag
        plt.scatter(x, y, color=culoare, s=marime)


def DeseneazaCerc(z0, r, NumarPuncte=100):
    ListaZ = []
    for k in range(NumarPuncte):
        theta = 2 * pi * k / NumarPuncte
        z = z0 + Trig2Cart(r, theta)
        ListaZ.append(z)
    return ListaZ


def DeseneazaSegment(z1, z2, NumarPuncte=100):
    ListaZ = []
    for k in range(NumarPuncte):
        t = k / NumarPuncte
        z = (1 - t) * z1 + t * z2
        ListaZ.append(z)
    return ListaZ


def DeseneazaPatrat(z0, l, NumarPuncte=100):
    ListaZ = []
    corners = [z0, z0 + l, z0 + l + 1j * l, z0 + 1j * l, z0]
    for i in range(4):
        segment = DeseneazaSegment(corners[i], corners[i + 1], NumarPuncte // 4)
        ListaZ.extend(segment)
    return ListaZ


def DeseneazaSectorCircular(z0, r, theta1, theta2, NumarPuncte=100):
    ListaZ = []
    ListaZ.append(z0)
    for k in range(NumarPuncte):
        theta = theta1 + (theta2 - theta1) * k / NumarPuncte
        z = z0 + Trig2Cart(r, theta)
        ListaZ.append(z)
    ListaZ.append(z0)
    return ListaZ


def translatie(ListaZ, b):
    return [z + b for z in ListaZ]


def omotetie(ListaZ, a):
    return [a * z for z in ListaZ]


def rotatie(ListaZ, angle):
    Elait = Trig2Cart(1, angle)
    return [z * Elait for z in ListaZ]


def simetrie(ListaZ):
    return [z.conjugate() for z in ListaZ]


def inversiune(ListaZ):
    return [1 / z if z != 0 else 0 for z in ListaZ]


def puterea2(ListaZ):
    return [z ** 2 + 7 - 1j * 5 for z in ListaZ]


def exponential(ListaZ):
    return [c.exp(z) for z in ListaZ]


def puterea3(ListaZ):
    return [z ** 3 for z in ListaZ]


class Aplicatie(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Transformari complexe')
        self.setGeometry(100, 100, 800, 600)

        font = QFont("Arial", 10)

        self.figura = QButtonGroup(self)
        self.segment_radio = QRadioButton("Segment")
        self.cerc_radio = QRadioButton("Cerc")
        self.patrat_radio = QRadioButton("Patrat")
        self.sector_radio = QRadioButton("Sector Circular")
        self.figura.addButton(self.segment_radio)
        self.figura.addButton(self.cerc_radio)
        self.figura.addButton(self.patrat_radio)
        self.figura.addButton(self.sector_radio)

        self.transformatii = QComboBox()
        self.transformatii.addItems([
            "Translatie", "Omotetie", "Rotatie", "Simetrie",
            "Inversiune", "Puterea2", "Exponential", "Puterea3"
        ])

        self.numar_input = QLineEdit()

        self.aplica = QPushButton("Aplica Transformare")
        self.aplica.clicked.connect(self.aplica_transformare)

        self.deseneaza = QPushButton("Deseneaza Figura")
        self.deseneaza.clicked.connect(self.draw)

        for widget in [self.segment_radio, self.cerc_radio, self.patrat_radio, self.sector_radio, self.transformatii,
                       self.numar_input, self.aplica, self.deseneaza]:
            widget.setFont(font)

        layout = QVBoxLayout()
        sectie_figura = QHBoxLayout()
        sectie_figura.addWidget(self.segment_radio)
        sectie_figura.addWidget(self.cerc_radio)
        sectie_figura.addWidget(self.patrat_radio)
        sectie_figura.addWidget(self.sector_radio)

        parametru = QHBoxLayout()

        parametru.addWidget(QLabel("Numar complex:"))
        parametru.addWidget(self.numar_input)

        layout.addLayout(sectie_figura)
        layout.addWidget(self.deseneaza)
        layout.addWidget(QLabel("Alege transformarea:"))
        layout.addWidget(self.transformatii)
        layout.addLayout(parametru)
        layout.addWidget(self.aplica)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.setStyleSheet("""
            QRadioButton {
                margin-right: 15px;
                color: #fff;
            }

            QComboBox {
                padding: 5px;
                color: #fff;
            }
            QComboBox:items {
                color: #fff;
            }
            QListView{
                color: rgb(110,209,255);
            } 
            QWidget {
                background: #262D37;
            }
            QLabel {
                color: #fff;
            } 
            QLineEdit {
                padding: 1px;
                color: #fff;
                border-style: solid;
                border: 2px solid #fff;
                border-radius: 8px;
            }
            QPushButton {
                color: white;
                background: #0577a8;
                border: 1px #DADADA solid;
                padding: 5px 10px;
                border-radius: 2px;
                font-weight: bold;
                font-size: 9pt;
                outline: none;
            }
            QPushButton:hover {
                border: 1px #C6C6C6 solid;
                background: #0892D0;
            }


        """)

        self.ListaZ = []
        self.ListaInitiala = []
    def plot(self, ListaZ):
        self.ax.clear()
        DeseneazaLista(ListaZ)
        self.ax.axhline(y=0, color='r', linestyle='-')
        self.ax.axvline(x=0, color='r', linestyle='-')
        self.ax.set_aspect('equal')
        self.canvas.draw()
    def draw(self):
        if self.segment_radio.isChecked():
            self.ListaZ = DeseneazaSegment(-2 - 1j, -1 + 3j, 100)
        elif self.cerc_radio.isChecked():
            self.ListaZ = DeseneazaCerc(2 + 3j, 1, 100)
        elif self.patrat_radio.isChecked():
            self.ListaZ = DeseneazaPatrat(1 + 1j, 2, 100)
        elif self.sector_radio.isChecked():
            self.ListaZ = DeseneazaSectorCircular(1 + 1j, 2, 0, pi / 2, 100)

        self.ListaInitiala = self.ListaZ.copy()
        self.plot(self.ListaZ)

    def aplica_transformare(self):
        transformatie = self.transformatii.currentText()
        try:
            complex_number = complex(self.numar_input.text()) if self.numar_input.text() else 0.0 + 0.0j

            if transformatie == "Translatie":
                self.ListaZ = translatie(self.ListaZ, complex_number)
            elif transformatie == "Omotetie":
                self.ListaZ = omotetie(self.ListaZ, complex_number)
            elif transformatie == "Rotatie":
                grade = complex_number.real
                radiani = grade * pi / 180
                self.ListaZ = rotatie(self.ListaZ, radiani)
            elif transformatie == "Simetrie":
                self.ListaZ = simetrie(self.ListaZ)
            elif transformatie == "Inversiune":
                self.ListaZ = inversiune(self.ListaZ)
            elif transformatie == "Puterea2":
                self.ListaZ = puterea2(self.ListaZ)
            elif transformatie == "Exponential":
                self.ListaZ = exponential(self.ListaZ)
            elif transformatie == "Puterea3":
                self.ListaZ = puterea3(self.ListaZ)

            self.plot(self.ListaZ)
        except ValueError as e:
            print(f"Error: {e}")




app = QApplication(sys.argv)
main_win = Aplicatie()
main_win.show()
sys.exit(app.exec_())
