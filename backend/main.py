from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    mail = db.Column(db.String(150), unique=True, nullable=False)
    super_user= db.Column(db.Boolean, default=False)
