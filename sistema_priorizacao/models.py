# criar as estrutura do banco de dados

from sistema_priorizacao import database, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))

class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    projetos = database.relationship("Projeto", backref="usuario", lazy=True)

class Projeto(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    id_usuario = database.Column(database.Integer, database.ForeignKey('usuario.id'), nullable=False)
    #criterios = database.relationship("Criterio", backref="projeto", lazy=True)

class Criterio(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    nome = database.Column(database.String, nullable=False)
    #id_projeto = database.Column(database.Integer, database.ForeignKey('projeto.id'), nullable=False)