import sys
from PyQt5.QtWidgets import (
    QLabel, QPushButton, QWidget, QApplication, QLineEdit,
    QHBoxLayout, QVBoxLayout, QMessageBox)
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
        layout_principal = QHBoxLayout()
        layout_principal.addWidget(imagem_label)
        layout_principal.addLayout(layout_direito)
        self.setLayout(layout_principal)

    def abrir_cliente(self):
        self.cadastro_cliente = TelaCadastroCliente()
        self.cadastro_cliente.show()

    def verificar_chave(self):
        chave, ok = QMessageBox.getText(self, "Chave de Acesso", "Digite sua chave de acesso")
        if ok and chave == "SPARROW123":
            QMessageBox.information(self,"Acesso Liberado", "Acesso permitido. Tela de cadastro de barco em contrucão")
        else:
            QMessageBox.warning(self, "Acesso Negado", "Voce precisa obter uma chave presecialmente na nossa sede.")

        if __name__=="__main__":
            app = QApplication(sys.argv)
            janela = TelaInicial()
            janela.show()
            sys.exit(app.exec_())   

class TelaCadastroCliente(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadastro de clinte")
        self.setFixedSize(300,250)

        layout = QVBoxLayout()

        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-mail")

        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setPlaceholderText(QLineEdit.Password)
        
        botao_cadastrar = QPushButton("Cadastrar")
        botao_cadastrar.clicked.connect(self.cadastrar_cliente)

        layout.addWidget(QLabel("Cadastro de cliente"))
        layout.addWidget(self.nome_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.senha_input)
        layout.addWidget(botao_cadastrar)

        self.setLayout(layout)
    
    def cadastro_cliente(self):
        nome = self.nome_input.text()
        email = self.email_input.text()
        senha = self.senha_input.text()

        QMessageBox.information(self, "Sucesso", f"Cliente cadastrado:\nNome: {nome}\nE-mail: {email}")

class TelaCadastroBarco(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cadrastro de Bancos")
        self.setFixedSize(300,250)

        layout = QVBoxLayout()

        self.nome_barco_input = QLineEdit()
        self.nome_barco_input.setPlaceholderText("Nome do Barco")

        self.capacidade_input = QLineEdit()
        self.capacidade_input.setPlaceholderText("Capacidade")
        
        self.dono_input = QLineEdit()
        self.dono_input.setPlaceholderText("Nome do Dono")

        botao_Cadastrar = QPushButton("Cadastrar")
        botao_Cadastrar.clicked.connect(self.cadastrar_barco)

        layout.addWidget(QLabel("Cadastro de Barco"))
        layout.addWidget(self.nome_barco_input)
        layout.addWidget(self.capacidade_input)
        layout.addWidget(self.dono_input)
        layout.addWidget(botao_Cadastrar)

        self.setLayout(layout)

    def cadastrar_barco(self):
        nome = self.nome_barco_input.text()
        capacidade = self.capacidade_input.text()
        dono = self.dono_input.text()

        QMessageBox.box.information(self, "Barco Cadastrado",f"Nome: {nome}\nCapacidade; {capacidade}\nDono: {dono}")

        
