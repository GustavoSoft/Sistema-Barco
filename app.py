from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

from extensions import db
from models import Usuario

app = Flask(__name__)
app.secret_key = "chave-secreta-sparrow"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:13245@localhost/sparrow_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET'])  # Se ainda quiser manter a rota
def escolha_cadastro():
    return redirect(url_for('home'))  # Redireciona para a home já que o modal está lá

@app.route('/cadastro-cliente', methods=['POST'])
def cadastro_cliente():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    senha_hash = generate_password_hash(senha)

    novo_cliente = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        tipo='cliente'
    )

    try:
        db.session.add(novo_cliente)
        db.session.commit()
        flash(f'Cliente cadastrado com sucesso: {nome}', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('E-mail já cadastrado. Tente outro.', 'error')

    return redirect(url_for('home'))

@app.route('/cadastro-barco', methods=['POST'])
def cadastro_barco():
    chave = request.form.get('chave')
    if chave != 'SPARROW123':
        flash("Chave inválida! Solicite presencialmente.", "error")
        return redirect(url_for('home'))
    nome = request.form['nome']
    capacidade = request.form['capacidade']
    dono = request.form['dono']
    flash(f'Barco cadastrado: {nome} - Capacidade: {capacidade} - Dono: {dono}', 'success')
    return redirect(url_for('home'))

@app.route('/login-cliente', methods=['POST'])
def login_cliente():
    email = request.form['email']
    senha = request.form['senha']
    flash(f'Login de cliente: {email}', 'success')
    return redirect(url_for('home'))

@app.route('/login-barco', methods=['POST'])
def login_barco():
    chave = request.form['chave']
    if chave != 'SPARROW123':
        flash('Chave inválida para login de dono de barco.', 'error')
    else:
        flash('Login do Dono do Barco realizado com sucesso!', 'success')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)

