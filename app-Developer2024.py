from flask import Flask, render_template
from routes.empresa_routes import empresa_bp
from routes.usuario_routes import usuario_bp

app = Flask(__name__)

# Registro dos blueprints (rotas separadas)
app.register_blueprint(empresa_bp)
app.register_blueprint(usuario_bp)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
