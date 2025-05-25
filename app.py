from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask import session
from datetime import datetime
from models import db, Barco, Viagem, Compra

from extensions import db
from models import Usuario

app = Flask(__name__)
app.secret_key = "chave-secreta-sparrow"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:13245@localhost/sparrow_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_request
def criar_tabelas():
    db.create_all()

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
    email = request.form['email']
    senha = request.form['senha']
    senha_hash = generate_password_hash(senha)

    from models import Usuario

    novo_dono = Usuario(
        nome=nome,
        email=email,
        senha_hash=senha_hash,
        tipo='dono_barco'
    )

    try:
        db.session.add(novo_dono)
        db.session.commit()
        flash(f'Dono do barco cadastrado com sucesso: {nome}', 'success')
    except IntegrityError:
        db.session.rollback()
        flash('E-mail já cadastrado. Tente outro.', 'error')

    return redirect(url_for('home'))

@app.route('/login-cliente', methods=['POST'])
def login_cliente():
    email = request.form['email']
    senha = request.form['senha']

    cliente = Usuario.query.filter_by(email=email, tipo='cliente').first()

    if cliente and check_password_hash(cliente.senha_hash, senha):
        session['usuario_id'] = cliente.id
        session['usuario_nome'] = cliente.nome
        session['usuario_tipo'] = cliente.tipo
        flash(f'Login de cliente realizado com sucesso, {cliente.nome}!', 'success')
    else:
        flash('Credenciais inválidas ou tipo de usuário incorreto.', 'error')

    return redirect(url_for('home'))


@app.route('/login-barco', methods=['POST'])
def login_barco():
    email = request.form['email']
    senha = request.form['senha']
    chave = request.form['chave']

    if chave != 'SPARROW123':
        flash('Chave inválida para login de dono de barco.', 'error')
        return redirect(url_for('home'))

    from models import Usuario
    dono = Usuario.query.filter_by(email=email, tipo='dono_barco').first()

    if dono and check_password_hash(dono.senha_hash, senha):
        session['usuario_id'] = dono.id
        session['usuario_nome'] = dono.nome
        session['usuario_tipo'] = dono.tipo
        flash(f'Login do Dono do Barco realizado com sucesso, {dono.nome}!', 'success')
    else:
        flash('Credenciais inválidas ou tipo de usuário incorreto.', 'error')

    return redirect(url_for('home'))

@app.route('/gerenciar-viagens')
def gerenciar_viagens():
    return render_template('inserir_viagens.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logout realizado com sucesso.", "success")
    return redirect(url_for('home'))


@app.route('/cadastrar-viagem', methods=['POST'])
def cadastrar_viagem():
    if 'usuario_id' not in session or session.get('usuario_tipo') != 'dono_barco':
        flash('Apenas donos de barco podem cadastrar viagens.', 'error')
        return redirect(url_for('home'))

    nome_barco = request.form['nomeBarco']
    capacidade = request.form['capacidade']
    data_partida = datetime.strptime(request.form['dataSaida'], '%Y-%m-%d').date()
    data_chegada = request.form['dataChegada']
    data_chegada = datetime.strptime(data_chegada, '%Y-%m-%d').date() if data_chegada else None
    origem = request.form['localPartida']
    destino = request.form['localChegada']
    hora_partida = datetime.strptime(request.form['horario'], '%H:%M').time()
    preco = request.form['preco']

    usuario_id = session['usuario_id']

    # Verifica se o barco já existe
    barco = Barco.query.filter_by(nome=nome_barco, usuario_id=usuario_id).first()
    if not barco:
        barco = Barco(nome=nome_barco, capacidade=capacidade, usuario_id=usuario_id)
        db.session.add(barco)
        db.session.commit()

    nova_viagem = Viagem(
        barco_id=barco.id,
        origem=origem,
        destino=destino,
        data_partida=data_partida,
        data_chegada=data_chegada,
        hora_partida=hora_partida,
        preco_passagem=preco
    )

    db.session.add(nova_viagem)
    db.session.commit()

    # Buscar todas as viagens deste dono de barco
    viagens = Viagem.query.join(Barco).filter(Barco.usuario_id == usuario_id).all()

    return render_template('inserir_viagens.html', viagens=viagens)

@app.route('/editar-viagem/<int:id>', methods=['GET', 'POST'])
def editar_viagem(id):
    viagem = Viagem.query.get_or_404(id)

    # Verifica se o dono é o usuário logado
    if viagem.barco.usuario_id != session.get('usuario_id'):
        flash('Permissão negada.', 'error')
        return redirect(url_for('painel_gerenciamento'))

    if request.method == 'POST':
        viagem.origem = request.form['origem']
        viagem.destino = request.form['destino']
        viagem.data_partida = datetime.strptime(request.form['data_partida'], '%Y-%m-%d')
        viagem.preco_passagem = float(request.form['preco_passagem'])

        db.session.commit()
        flash('Viagem atualizada com sucesso!', 'success')
        return redirect(url_for('painel_gerenciamento'))

    return render_template('editar_viagem.html', viagem=viagem)


@app.route('/painel-gerenciamento')
def painel_gerenciamento():
    if 'usuario_id' not in session or session.get('usuario_tipo') != 'dono_barco':
        flash('Acesso negado.', 'error')
        return redirect(url_for('home'))

    usuario_id = session['usuario_id']
    viagens = Viagem.query.join(Barco).filter(Barco.usuario_id == usuario_id).all()
    return render_template('painel_gerenciamento.html', viagens=viagens)

@app.route('/remover-viagem/<int:id>', methods=['POST'])
def remover_viagem(id):
    viagem = Viagem.query.get_or_404(id)

    # Verifica se o dono é o usuário logado
    if viagem.barco.usuario_id != session.get('usuario_id'):
        flash('Permissão negada.', 'error')
        return redirect(url_for('painel_gerenciamento'))

    db.session.delete(viagem)
    db.session.commit()
    flash('Viagem removida com sucesso!', 'success')
    return redirect(url_for('painel_gerenciamento'))


@app.route('/listar-viagens')
def listar_viagens():
    partida = request.args.get('partida')
    destino = request.args.get('destino')
    mes = request.args.get('mes')

    query = Viagem.query.join(Barco)

    if partida:
        query = query.filter(Viagem.origem.ilike(f"%{partida}%"))
    if destino:
        query = query.filter(Viagem.destino.ilike(f"%{destino}%"))
    if mes:
        try:
            # Extrai apenas o número do mês do formato 'YYYY-MM'
            mes_numero = int(mes.split('-')[1])
            query = query.filter(db.extract('month', Viagem.data_partida) == mes_numero)
        except (IndexError, ValueError):
            pass  # Ignora se o valor estiver malformado

    viagens = query.all()

    resultados = []
    for v in viagens:
        resultados.append({
            "nome": v.barco.nome,
            "partida": v.origem,
            "destino": v.destino,
            "data": v.data_partida.strftime("%Y-%m-%d"),
            "horario": v.hora_partida.strftime("%H:%M"),
            "preco": float(v.preco_passagem),
            "tipo": "Barco"  # Pode personalizar se quiser
        })

    return render_template("listar_viagens.html", resultados=resultados, viagens=viagens)

@app.route('/comprar', methods=['POST'])
def comprar_passagem():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    usuario_id = session['usuario_id']
    viagem_id = request.form['viagem_id']
    nome_passageiro = request.form['nome_passageiro']
    documento = request.form['documento']

    nova_compra = Compra(
        usuario_id=usuario_id,
        viagem_id=viagem_id,
        nome_passageiro=nome_passageiro,
        documento=documento
    )
    db.session.add(nova_compra)
    db.session.commit()

    return redirect(url_for('ver_passagens'))

@app.route('/ver-passagens')
def ver_passagens():
    if 'usuario_id' not in session:
        return redirect(url_for('index'))

    usuario_id = session['usuario_id']
    compras = Compra.query.filter_by(usuario_id=usuario_id).all()
    return render_template('ver_passagens.html', compras=compras)

@app.route('/cancelar-compra', methods=['POST'])
def cancelar_compra():
    compra_id = request.form.get('compra_id')
    compra = Compra.query.get(compra_id)

    if compra and compra.usuario_id == session.get('usuario_id'):
        db.session.delete(compra)
        db.session.commit()

    return redirect(url_for('ver_passagens'))


if __name__ == '__main__':
    app.run(debug=True)

