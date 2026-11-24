from datetime import datetime, timezone

from flask import current_app, flash, redirect, render_template, url_for

from . import main
from .forms import ProfessorForm
from .. import db
from ..models import Disciplina, Professor


@main.route('/')
def index():
    return render_template('index.html',
                           nome=current_app.config['FLASKY_NAME'],
                           prontuario=current_app.config['FLASKY_PRONTUARIO'],
                           current_time=datetime.now(timezone.utc))


@main.route('/professores', methods=['GET', 'POST'])
def professores():
    form = ProfessorForm()
    form.disciplina.choices = [(d.id, d.nome) for d in Disciplina.query.order_by(Disciplina.id).all()]
    if form.validate_on_submit():
        professor = Professor(nome=form.nome.data.strip(), disciplina_id=form.disciplina.data)
        db.session.add(professor)
        db.session.commit()
        flash('Professor cadastrado com sucesso!')
        return redirect(url_for('.professores'))
    lista = Professor.query.order_by(Professor.id).all()
    return render_template('professores.html', form=form, professores=lista)


# Módulos não desenvolvidos: exibem apenas "Não disponível".
@main.route('/disciplinas')
@main.route('/alunos')
@main.route('/cursos')
@main.route('/ocorrencias')
def nao_disponivel():
    return render_template('nao_disponivel.html', current_time=datetime.now(timezone.utc))
