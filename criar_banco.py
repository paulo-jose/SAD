from sistema_priorizacao import database, app
from sistema_priorizacao.models import Usuario, Projeto

with app.app_context():
    database.create_all()