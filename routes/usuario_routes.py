from flask import Blueprint, render_template, request

usuario_bp = Blueprint('usuario', __name__, url_prefix='/usuario')

@usuario_bp.route('/cadastro')
def formulario_usuario():
    return render_template('cadastro_usuario.html')

@usuario_bp.route('/cadastro', methods=['POST'])
def cadastrar_usuario():
    nome = request.form['nome']
    email = request.form['email']
    return f"Usuário '{nome}' com email '{email}' cadastrado!"
