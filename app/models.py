from . import db


class Disciplina(db.Model):
    __tablename__ = 'disciplinas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(64), unique=True, nullable=False)
    professores = db.relationship('Professor', backref='disciplina', lazy='dynamic')

    def __repr__(self):
        return f'<Disciplina {self.nome}>'


class Professor(db.Model):
    __tablename__ = 'professores'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(128), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('disciplinas.id'), nullable=False)

    def __repr__(self):
        return f'<Professor {self.nome}>'
