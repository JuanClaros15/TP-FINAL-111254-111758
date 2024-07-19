#para manejo de rutas, consultas HTTP y crear aplicacion web
from flask import Flask, render_template, request, redirect, url_for, flash
#autenticar los usuarios
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
#conexion con la base de datos
from flask_sqlalchemy import SQLAlchemy
#manejo de las contraseñas
from flask_bcrypt import Bcrypt 
#para las instancias 
from main import db, Usuario

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')  
app.config['SECRET_KEY'] = '123456789'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456789@localhost:5432/TP_FINAL'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Ruta a la página de login

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def index():
    return "Hello World"

@app.route('/pagina_principal')
@login_required
def pagona_principal():
    return render_template('pagina_principal.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            flash('Inicio de sesión exitoso!', 'success')
            return redirect(url_for('pagona_principal'))  # Redirige a la página principal después del login
        else:
            flash('Inicio de sesión fallido. Por favor, verifica tu usuario y contraseña.', 'danger')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
