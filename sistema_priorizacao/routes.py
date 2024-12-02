# criar as routas do site
from flask import render_template, url_for, redirect, request, flash
from sistema_priorizacao import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from sistema_priorizacao.forms import FormLogin, FormCriarConta, FormProjeto, FormCriterio, FormEditarProjeto
from sistema_priorizacao.models import Usuario, Projeto, Criterio


@app.route("/", methods=["GET", "POST"])
def homepage():
    formLogin = FormLogin()
    error = None
    if formLogin.validate_on_submit():
        usuario = Usuario.query.filter_by(email=formLogin.email.data).first()

        if usuario and bcrypt.check_password_hash(usuario.senha, formLogin.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))
        else:
            error = "Usuario ou senha incorretos!"

    return render_template("homepage.html", form=formLogin, error=error)


@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    formCriarConta = FormCriarConta()
    if formCriarConta.validate_on_submit():
        senha = bcrypt.generate_password_hash(formCriarConta.senha.data)
        usuario = Usuario(username=formCriarConta.username.data, senha=senha, email=formCriarConta.email.data)
        database.session.add(usuario)
        database.session.commit()
        login_user(usuario, remember=True)
        flash(f"Usuário {usuario.username} criado com sucesso!", "sucesso")
        return redirect(url_for("homepage"))

    return render_template("criarconta.html", form=formCriarConta)


@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])
@login_required
def perfil(id_usuario):
    requisicao = request.form
    if int(id_usuario) == int(current_user.id):
        #usuario acessando seu perfil
        criterios = Criterio.query.all()
        form_projeto = FormProjeto()
        form_criterio = FormCriterio()
        form_editar_projeto = FormEditarProjeto()
        if form_projeto.validate_on_submit():
            if form_projeto.botao_confirmacao.data:
                projeto = Projeto(nome=form_projeto.nome_projeto.data, escopo=form_projeto.escopo_projeto.data,gerente=form_projeto.gerente_projeto.data, id_usuario=id_usuario)
                database.session.add(projeto)
                database.session.commit()
                flash(f"Projeto {projeto.nome} criado com sucesso!", "sucesso")
                return render_template("perfil.html", usuario=current_user, form=form_projeto, criterios=criterios, form_criterio=form_criterio, form_editar_projeto=form_editar_projeto)

        elif form_criterio.validate_on_submit():
            if form_criterio.botao_confirmacao.data:
                criterio = Criterio(nome=form_criterio.nome_criterio.data, detalhamento=form_criterio.descricao_criterio.data)
                database.session.add(criterio)
                database.session.commit()
                flash(f"Criterio {criterio.nome} criado com sucesso!", "sucesso")
                criterios = Criterio.query.all()
                return render_template("perfil.html", usuario=current_user, form=form_projeto, criterios=criterios, form_criterio=form_criterio, form_editar_projeto=form_editar_projeto)
            else:
                id_criterio = requisicao['id_criterio']
                criterio = Criterio.query.get(id_criterio)
                criterio.nome = requisicao['nome_criterio']
                database.session.commit()
                criterios = Criterio.query.all()
                flash(f"Criterio {criterio.nome} editado com sucesso!", "sucesso")
                return redirect(url_for("perfil", id_usuario=id_usuario, criterios=criterios, form=form_criterio))

        return render_template("perfil.html", usuario=current_user, form=form_projeto, criterios=criterios, form_criterio=form_criterio, form_editar_projeto=form_editar_projeto)
    else:
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario=usuario, form=None, form_criterio=None, form_editar_projeto=None)


@app.route("/excluir/<id_projeto>", methods=["GET", "POST"])
@login_required
def excluir(id_projeto):
    usuario = current_user
    projeto = Projeto.query.get(id_projeto)
    form_projeto = FormProjeto()
    if (projeto):
        database.session.delete(projeto)
        database.session.commit()
        flash(f"Projeto {projeto.nome} deletado com sucesso!", "sucesso")
        return redirect(url_for("perfil", id_usuario=usuario.id))
    else:
        return render_template("perfil.html", usuario=current_user, form=form_projeto)


@app.route("/editar/<id_projeto>", methods=["GET", "POST"])
@login_required
def editar(id_projeto):
    #if request.method == 'POST':
    requisicao = request.form
    usuario = current_user
    form_editar_projeto = FormEditarProjeto()
    criterios = Criterio.query.all()
    formProjetos = FormProjeto()
    formCriterio = FormCriterio()

    if form_editar_projeto.botao_editar.data:
        print(form_editar_projeto.nome_projeto)
        projeto = Projeto.query.get(id_projeto)
        projeto.nome = form_editar_projeto.nome_projeto.data
        database.session.commit()
        flash(f"Projeto {projeto.nome} editado com sucesso!", "sucesso")
        return render_template("perfil.html",  usuario=current_user, form=formProjetos, form_editar_projeto=form_editar_projeto, form_criterio=formCriterio,  criterios=criterios)
    else:
        return render_template("perfil.html", usuario=current_user, form=formProjetos, form_editar_projeto=form_editar_projeto, form_criterio=formCriterio,  criterios=criterios)


@app.route("/excluir_criterio/<id_criterio>", methods=["GET", "POST"])
@login_required
def excluir_criterio(id_criterio):
    usuario = current_user
    criterio = Criterio.query.get(id_criterio)
    criterios = Criterio.query.all()
    form_criterio = FormCriterio()
    if (criterio):
        database.session.delete(criterio)
        database.session.commit()
        flash(f"Criterio {criterio.nome} deletado com sucesso!", "sucesso")
        return redirect(url_for("perfil", id_usuario=usuario.id, criterios=criterios))
    else:
        return render_template("perfil.html", usuario=current_user, form=form_criterio, criterios=criterios)


@app.route("/editar_criterio/<id_criterio>", methods=["GET", "POST"])
@login_required
def editar_criterio(id_criterio):
    #if request.method == 'POST':
    requisicao = request.form
    usuario = current_user
    criterio = Criterio.query.get(id_criterio)
    form_criterio = FormCriterio()
    form_criterio.nome_criterio.data = criterio.nome
    if form_criterio.validate_on_submit():
        criterio.nome = requisicao['nome_criterio']
        database.session.commit()
        criterios = Criterio.query.all()
        flash(f"Criterio {criterio.nome} editado com sucesso!", "sucesso")
        return redirect(url_for("perfil", id_usuario=usuario.id, criterios=criterios, form=form_criterio))
    else:
        return render_template("editar.html", id_criterio=True, form=form_criterio)


@app.route("/atribuirpesos", methods=["GET", "POST"])
@login_required
def atribuirpesos():
    criterios = Criterio.query.all()
    projetos = Projeto.query.all()
    usuario = current_user
    cont = 0

    for criterio in criterios:
        criterio.criterios = criterios

    if len(criterios) >= 2 and len(projetos) >= 2:
        return render_template("atribuirpesos.html", usuario=usuario, criterios=criterios, cont=cont)
    else:
        flash("O numero de critério e de projetos tem que ser maior ou igual a 2", "error")
        return redirect(url_for("perfil", id_usuario=usuario.id))



@app.errorhandler(404)
def error_path(erro):
    return redirect(url_for("error", erro=erro))


@app.route("/template-logado", methods=["GET", "POST"])
@login_required
def template():
    return redirect(url_for("template-logado"))


@app.route("/ranqueamento",methods=["GET", "POST"])
@login_required
def ranqueamento():
    criterios = Criterio.query.all()
    projetos = Projeto.query.all()
    usuario = current_user
    return render_template("ranqueamento.html", usuario=usuario, projetos=projetos, criterios=criterios)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))
