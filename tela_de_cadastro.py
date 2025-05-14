import sys
from PyQt5.QtWidgets import (
    QLabel, QPushButton, 
QHboxLayout, QVBoxLayout, QMessagebox)
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt

class TelaInicial(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sparrow - Sistema de Viagem")
        self.setFixedSize(900,500)
        self.init_ui()

    def init_ui(self):
        imagem_label = QLabel(self)
        pixmap = QPixmap("https://cdn-hweb.hsystem.com.br/5873d325c19a4207cc40b87c/35464b3be0044f5a8a689a425b5247a6.jpg")
        pixmap= pixmap.scaled(400, 500, Qt.keepApectRatioByExpading)
        imagem_label.setPixmap(pixmap)
        imagem_label.setAlignment(Qt.AlignCenter)
        
        titulo = QLabel("Bem - Vindo ao Sparrow!")
        titulo.setFont(QFont("Arial", 18))

        subtitulo = QLabel("Escolha uma opcao para continuar:")
        subtitulo.setFont(QFont("Ariel",12))

        botao_cliente = QPushButton("Sou Cliente")
        botao_cliente.setStyleSheet("background-color: #0275d8; color: Whiter; padding:10X; ; font-size: 14px")
        botao_cliente.clicked.connect(self.abrir_cliente)

        botao_dono = QPushButton("Sou Dono de Barco")
        botao_dono.setStyleSheet("background-color: #0275d8; color: Whiter; padding:10X; ; font-size: 14px")
        botao_dono.clicked.connect(self.verificar_chave)
        
        layout_direito = QVBoxLayout()
        layout_direito.addWidget(titulo)
        layout_direito.addWidget(subtitulo)
        layout_direito.addSpacing(20)
        layout_direito.addWidget(botao_cliente)
        layout_direito.addWidget(botao_dono)
        layout_direito.addStretch()
        layout_principal = QHboxLayout()
        layout_principal.addWidget(imagem_label)
        layout_principal.addLayout(layout_direito)
        self.setLayout(layout_principal)
       