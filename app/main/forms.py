from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class ProfessorForm(FlaskForm):
    nome = StringField('Cadastre o novo Professor:', validators=[DataRequired(), Length(1, 128)])
    disciplina = SelectField('Disciplina associada:', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Cadastrar')
