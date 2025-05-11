from flask import Blueprint, render_template, request
empresa_bp = Blueprint('empresa', __name__, url_prefix='/empresa')

@empresa_bp.route('/cadastro')
def formulario_empresa():
    return render_template('cadastro_empresa.html')

@empresa_bp.route('/cadastro', methods=['POST'])
def cadastrar_empresa():
    nome = request.form['nome']
    codigo_acesso = request.form['codigo']
    # Aqui você gravaria no banco, depois retorno simples:
    return f"Empresa '{nome}' cadastrada com código '{codigo_acesso}'"
