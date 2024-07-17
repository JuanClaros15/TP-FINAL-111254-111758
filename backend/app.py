from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from main import db, Usuario 


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:123456789@localhost:5432/TP_FINAL'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def index():
    return "Hello World"

if __name__ == '__main__':
    app.run(debug=True)
