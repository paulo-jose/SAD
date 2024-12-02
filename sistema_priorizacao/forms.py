#criar formularios do site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo
from sistema_priorizacao.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Fazer Login")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    username = StringField("Nome de usuário", validators=[DataRequired()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators=[DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            return ValidationError("E-mail já cadastrado, faça login para continuar")

class FormProjeto(FlaskForm):
    nome_projeto = StringField("Nome do Projeto", validators=[DataRequired()])
    escopo_projeto = StringField("Escopo do Projeto", validators=[DataRequired()])
    gerente_projeto = StringField("Gerente do Projeto", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Cadastrar Projeto")
    botao_editar = SubmitField("Editar Projeto")

class FormEditarProjeto(FlaskForm):
    id_projeto = StringField("Nome do Projeto", validators=[DataRequired()])
    nome_projeto = StringField("Nome do Projeto", validators=[DataRequired()])
    escopo_projeto = TextAreaField("Escopo do Projeto", validators=[DataRequired()])
    gerente_projeto = StringField("Gerente do Projeto", validators=[DataRequired()])
    botao_editar = SubmitField("Editar Projeto")


class FormCriterio(FlaskForm):
    id_criterio = StringField("Nome do Critério")
    nome_criterio = StringField("Nome do Critério", validators=[DataRequired()])
    descricao_criterio = StringField("Descrição/Justificativa", validators=[DataRequired()])
    botao_confirmacao = SubmitField("Cadastrar Critério")
    botao_editar = SubmitField("Editar Criterio")


