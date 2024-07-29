# Importaciones necesarias para manejar rutas, consultas HTTP y crear la aplicación web
from flask import Flask, render_template, request, redirect, url_for, jsonify

# Importaciones para autenticar los usuarios
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

# Importación para la conexión con la base de datos
from flask_sqlalchemy import SQLAlchemy

# Importación para el manejo de las contraseñas
from flask_bcrypt import Bcrypt

# Importaciones de las instancias y modelos desde el módulo principal
from main import db, Usuario, Ticket

# Importaciones para funciones de seguridad
from werkzeug.security import generate_password_hash, check_password_hash

# Importación para la configuración del registro de logs
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.DEBUG)

# Creación de la aplicación Flask y configuración de carpetas para plantillas y archivos estáticos
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

# Configuración de la clave secreta y la URI de la base de datos
app.config['SECRET_KEY'] = '123456789'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456789@localhost:5432/TP_FINAL'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de la base de datos con la aplicación Flask
db.init_app(app)

# Inicialización de Bcrypt con la aplicación Flask para manejo de contraseñas
bcrypt = Bcrypt(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Vista a la que se redirige para iniciar sesión si no está autenticado

# Función de carga de usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Ruta raíz de la aplicación
@app.route('/')
def index():
    return "Hola Mundo!!"

# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Ruta para la página principal, requiere inicio de sesión
@app.route('/pagina_principal')
@login_required
def pagina_principal():
    return render_template('pagina_principal.html', username=current_user.username)

# Ruta para manejar el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Usuario.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('pagina_principal'))
    return render_template('index.html')

# Ruta para manejar el registro de nuevos usuarios
@app.route('/register', methods=['GET', 'POST'])    
def register():
    if request.method == 'POST':
        username = request.form['username']
        mail = request.form['mail']
        password = request.form['password']
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = Usuario(username=username, mail=mail, password=password_hash)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('registro.html')

# Ruta para manejar el reseteo de contraseñas
@app.route('/reset_password', methods=['GET','POST'])
def reset_password():
    if request.method == 'POST':
        username = request.form.get('username')
        mail = request.form.get('mail')
        new_password = request.form.get('new_password')
        user = Usuario.query.filter_by(mail=mail, username=username).first()
        if user:
            user.password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('recuperar_contraseña.html')

# Ruta para obtener la lista de tickets del usuario actual
@app.route('/tickets', methods=['GET'])
@login_required
def get_tickets():
    if current_user.id_user == 1:  # Si el usuario es el administrador
        tickets = Ticket.query.all()
    else:  # Si el usuario es un usuario cualquiera
        tickets = Ticket.query.filter_by(usuario_id=current_user.id_user).all()
    tickets_list = [{
        'id_ticket': ticket.id_ticket,
        'titulo': ticket.titulo,
        'descripcion': ticket.descripcion,
        'prioridad': ticket.prioridad,
        'estado': ticket.estado,
        'fecha_creacion': ticket.fecha_creacion.strftime('%d/%m/%Y %H:%M:%S'),
        'usuario': ticket.usuario.username,  
        'mail': ticket.usuario.mail,
    } for ticket in tickets]
    return jsonify(tickets_list)

# Ruta para agregar un nuevo ticket
@app.route('/ticket', methods=['POST'])
@login_required
def add_ticket():
    data = request.json
    app.logger.debug(f"Datos recibidos: {data}")
    
    new_ticket = Ticket(
        titulo=data['titulo'],
        descripcion=data['descripcion'],
        prioridad=data['prioridad'],
        estado='en curso',
        usuario_id=current_user.id_user
    )
    db.session.add(new_ticket)
    db.session.commit()
    app.logger.debug("Ticket agregado a la base de datos")

    return jsonify({'message': 'Ticket agregado exitosamente!'}), 201

# Ruta para cerrar un ticket existente
@app.route('/ticket/<int:ticket_id>/close', methods=['PATCH'])
@login_required
def close_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.usuario_id != current_user.id_user:
        return jsonify({'message': 'No autorizado'}), 403

    ticket.estado = 'finalizado'
    db.session.commit()
    return jsonify({'message': 'Ticket finalizado exitosamente!'})

# Ruta para eliminar un ticket existente
@app.route('/ticket/<int:ticket_id>', methods=['DELETE'])
@login_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if ticket.usuario_id != current_user.id_user:
        return jsonify({'message': 'No autorizado'}), 403

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({'message': 'Ticket eliminado exitosamente!'})

# Ejecuta la aplicación Flask en modo debug
if __name__ == '__main__':
    app.run(debug=True)
