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
    dono_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

class Viagem(db.Model):
    __tablename__ = 'viagens'
    id = db.Column(db.Integer, primary_key=True)
    barco_id = db.Column(db.Integer, db.ForeignKey('barcos.id'), nullable=False)
    origem = db.Column(db.String(100), nullable=False)
    destino = db.Column(db.String(100), nullable=False)
    data_partida = db.Column(db.Date, nullable=False)
    hora_partida = db.Column(db.Time, nullable=False)
    preco_passagem = db.Column(db.Numeric(10,2), nullable=False)

class Passagem(db.Model):
    __tablename__ = 'passagens'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    viagem_id = db.Column(db.Integer, db.ForeignKey('viagens.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    data_compra = db.Column(db.DateTime, default=datetime.utcnow)
