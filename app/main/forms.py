from flask_wtf import FlaskForm
from wtforms import RadioField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

from .. import DISCIPLINAS_ASSOCIADAS

ESCOLHAS_DISCIPLINA = [(d, d) for d in DISCIPLINAS_ASSOCIADAS]
SEMESTRES = [(f'{n}º semestre', f'{n}º semestre') for n in range(1, 7)]


class ProfessorForm(FlaskForm):
    name = StringField('Cadastre o novo Professor:', validators=[DataRequired()])
    role = SelectField('Disciplina associada:', choices=ESCOLHAS_DISCIPLINA)
    submit = SubmitField('Cadastrar')


class DisciplinaForm(FlaskForm):
    name = StringField('Cadastre a nova disciplina e o semestre associado:', validators=[DataRequired()])
    semester = RadioField(choices=SEMESTRES)
    submit = SubmitField('Cadastrar')


class AlunoForm(FlaskForm):
    name = StringField('Cadastre o novo Aluno:', validators=[DataRequired()])
    role = SelectField('Disciplina associada:', choices=ESCOLHAS_DISCIPLINA)
    submit = SubmitField('Cadastrar')


class CursoForm(FlaskForm):
    coursename = StringField('Qual é o nome do curso?', validators=[DataRequired()])
    coursedescription = TextAreaField('Descrição (250 caracteres)', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')
