from extensions import db
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.Enum('cliente', 'dono_barco'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

class Barco(db.Model):
    __tablename__ = 'barcos'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    capacidade = db.Column(db.Integer, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=True)
    viagens = db.relationship('Viagem', backref='barco', lazy=True) # RELACIONAMENTO: um barco pode ter várias viagens


class Viagem(db.Model):
    __tablename__ = 'viagens'
    id = db.Column(db.Integer, primary_key=True)
    barco_id = db.Column(db.Integer, db.ForeignKey('barcos.id'), nullable=False)
    origem = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    data_partida = db.Column(db.Date, nullable=False)
    data_chegada = db.Column(db.Date, nullable=True)
    hora_partida = db.Column(db.Time, nullable=False)
    preco_passagem = db.Column(db.Float(10, 2), nullable=False)

class Compra(db.Model):
    __tablename__ = 'compras'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    viagem_id = db.Column(db.Integer, db.ForeignKey('viagens.id'), nullable=False)
    nome_passageiro = db.Column(db.String(100), nullable=False)
    documento = db.Column(db.String(50), nullable=False)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuario', backref='compras')
    viagem = db.relationship('Viagem', backref='compras')

