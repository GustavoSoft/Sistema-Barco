import sys
from PyQt5.QtWidgets import (
    QLabel, QPushButton, 
QHboxLayout, QVBoxLayout, QMessagebox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class TelaInicial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sparrow - Bem vindo")
        self.setFixedSize(900,500)
        self.init_ui()

    def init_ui(self):
        imagem_label = QLabel(self)
        pixmap = QPixmap("https://cdn-hweb.hsystem.com.br/5873d325c19a4207cc40b87c/35464b3be0044f5a8a689a425b5247a6.jpg")
        pixmap= pixmap.scaled(400, 500, Qt.keepApectRatioByExpading)
        imagem_label.setPixmap(pixmap)
        imagem_label.setAlignment(Qt.Alignment)
