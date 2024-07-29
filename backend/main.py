from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Inicializa SQLAlchemy para gestionar la base de datos
db = SQLAlchemy()

class Usuario(db.Model, UserMixin):
    # Define el nombre de la tabla en la base de datos
    __tablename__ = 'usuarios'

    # Define las columnas de la tabla 'usuarios'
    id_user = db.Column(db.Integer, primary_key=True)  # Clave primaria
    username = db.Column(db.String(150), unique=True, nullable=False)  # Nombre de usuario, único y no nulo
    password = db.Column(db.String(255), nullable=False)  # Contraseña del usuario, no nulo
    mail = db.Column(db.String(150), unique=True, nullable=False)  # Correo electrónico del usuario, único y no nulo

    # Define la relación uno-a-muchos con la tabla 'tickets'
    tickets = db.relationship('Ticket', backref='usuario', lazy=True)

    # Método que proporciona una representación legible del objeto Usuario
    def __repr__(self):
        return f"Usuario('{self.username}', '{self.mail}')"

    # Método requerido por Flask-Login para obtener el ID del usuario
    def get_id(self):
        return str(self.id_user)

class Ticket(db.Model):
    # Define el nombre de la tabla en la base de datos
    __tablename__ = 'tickets'
    
    # Define las columnas de la tabla 'tickets'
    id_ticket = db.Column(db.Integer, primary_key=True)  # Clave primaria
    titulo = db.Column(db.String(100), nullable=False)  # Título del ticket, no nulo
    descripcion = db.Column(db.Text, nullable=False)  # Descripción del ticket, no nulo
    prioridad = db.Column(db.String(10), nullable=False)  # Prioridad del ticket, no nulo
    estado = db.Column(db.String(10), default='en curso', nullable=False)  # Estado del ticket, por defecto 'en curso' y no nulo
    fecha_creacion = db.Column(db.DateTime, default=db.func.current_timestamp())  # Fecha de creación del ticket, por defecto la fecha y hora actuales
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_user'), nullable=False)  # Clave foránea que referencia a 'usuarios.id_user'

    # Método que proporciona una representación legible del objeto Ticket
    def __repr__(self):
        return f"Ticket('{self.titulo}', '{self.estado}')"
