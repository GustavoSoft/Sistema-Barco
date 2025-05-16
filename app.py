from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "chave-secreta-sparrow"

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
    flash(f'Cliente cadastrado: {nome} ({email})', 'success')
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

if __name__ == '__main__':
    app.run(debug=True)

