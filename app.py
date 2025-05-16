from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "chave-secreta-sparrow"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/cadastro')
def escolha_cadastro():
    return render_template("escolha_cadastro.html")

@app.route('/cadastro-cliente', methods=['GET', 'POST'])
def cadastro_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        flash(f'Cliente cadastrado: {nome} ({email})', 'success')
        return redirect(url_for('home'))
    return render_template("cadastro_cliente.html")

@app.route('/cadastro-barco', methods=['GET', 'POST'])
def cadastro_barco():
    if request.method == 'POST':
        chave = request.form.get('chave')
        if chave != 'SPARROW123':
            flash("Chave inválida! Solicite presencialmente.", "error")
            return redirect(url_for('escolha_cadastro'))
        nome = request.form['nome']
        capacidade = request.form['capacidade']
        dono = request.form['dono']
        flash(f'Barco cadastrado: {nome} - Capacidade: {capacidade} - Dono: {dono}', 'success')
        return redirect(url_for('home'))
    return render_template("cadastro_barco.html")

if __name__ == '__main__':
    app.run(debug=True)

