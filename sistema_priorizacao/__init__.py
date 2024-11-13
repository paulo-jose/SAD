from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///projetos.db"
app.config["SECRET_KEY"] = "e397bfcd3ebede6ceeaf2ed5880ecb3d"
app.config["UPLOAD_FOLDER"] = "static/documentacao"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "homepage"


from sistema_priorizacao import routes