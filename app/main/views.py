from datetime import datetime, timezone

from flask import current_app, flash, redirect, render_template, url_for

from . import main
from .forms import AlunoForm, CursoForm, DisciplinaForm, ProfessorForm
from .. import db
from ..models import Aluno, Curso, Disciplina, Professor


def _disciplina_por_nome(nome):
    return Disciplina.query.filter_by(nome=nome).order_by(Disciplina.id).first()


@main.route('/')
def index():
    return render_template('index.html',
                           nome=current_app.config['FLASKY_NAME'],
                           prontuario=current_app.config['FLASKY_PRONTUARIO'],
                           current_time=datetime.now(timezone.utc))


@main.route('/professores', methods=['GET', 'POST'])
def professores():
    form = ProfessorForm()
    if form.validate_on_submit():
        db.session.add(Professor(nome=form.name.data,
                                 disciplina=_disciplina_por_nome(form.role.data)))
        db.session.commit()
        flash('Professor cadastrado com sucesso!')
        return redirect(url_for('.professores'))
    lista = Professor.query.order_by(Professor.id).all()
    return render_template('professores.html', form=form, professores=lista)


@main.route('/disciplinas', methods=['GET', 'POST'])
def disciplinas():
    form = DisciplinaForm()
    if form.validate_on_submit():
        db.session.add(Disciplina(nome=form.name.data, semestre=form.semester.data))
        db.session.commit()
        flash('Disciplina cadastrada com sucesso!')
        return redirect(url_for('.disciplinas'))
    lista = Disciplina.query.order_by(Disciplina.id).all()
    return render_template('disciplinas.html', form=form, disciplinas=lista)


@main.route('/alunos', methods=['GET', 'POST'])
def alunos():
    form = AlunoForm()
    if form.validate_on_submit():
        db.session.add(Aluno(nome=form.name.data,
                             disciplina=_disciplina_por_nome(form.role.data)))
        db.session.commit()
        flash('Estudante cadastrado com sucesso!')
        return redirect(url_for('.alunos'))
    lista = Aluno.query.order_by(Aluno.id).all()
    return render_template('alunos.html', form=form, alunos=lista)


@main.route('/cursos', methods=['GET', 'POST'])
def cursos():
    form = CursoForm()
    if form.validate_on_submit():
        db.session.add(Curso(nome=form.coursename.data,
                             descricao=form.coursedescription.data))
        db.session.commit()
        flash('Curso cadastrado com sucesso!')
        return redirect(url_for('.cursos'))
    lista = Curso.query.order_by(Curso.id).all()
    return render_template('cursos.html', form=form, cursos=lista)


# Módulo não desenvolvido: exibe apenas "Não disponível".
@main.route('/ocorrencias', methods=['GET', 'POST'])
def nao_disponivel():
    return render_template('nao_disponivel.html', current_time=datetime.now(timezone.utc))
