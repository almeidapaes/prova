from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text

from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

# Disciplinas fixas exibidas nos campos "Disciplina associada"
DISCIPLINAS_ASSOCIADAS = ['DSWA5', 'GPSA5', 'IHCA5', 'SODA5', 'PJIA5', 'TCOA5']


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        _preparar_banco()

    return app


def _preparar_banco():
    from .models import Disciplina
    db.create_all()

    # Bancos criados pela versão anterior: "nome" era UNIQUE e não havia "semestre".
    # Recria a tabela preservando os ids (os professores apontam para eles).
    insp = inspect(db.engine)
    colunas = [c['name'] for c in insp.get_columns('disciplinas')]
    if 'semestre' not in colunas or insp.get_unique_constraints('disciplinas'):
        semestre = 'semestre' if 'semestre' in colunas else 'NULL'
        with db.engine.begin() as conn:
            conn.execute(text('CREATE TABLE disciplinas_nova (id INTEGER NOT NULL PRIMARY KEY, '
                              'nome VARCHAR(64) NOT NULL, semestre VARCHAR(32))'))
            conn.execute(text(f'INSERT INTO disciplinas_nova (id, nome, semestre) '
                              f'SELECT id, nome, {semestre} FROM disciplinas'))
            conn.execute(text('DROP TABLE disciplinas'))
            conn.execute(text('ALTER TABLE disciplinas_nova RENAME TO disciplinas'))

    for nome in DISCIPLINAS_ASSOCIADAS:
        if Disciplina.query.filter_by(nome=nome).first() is None:
            db.session.add(Disciplina(nome=nome, semestre='5º semestre'))
    Disciplina.query.filter(Disciplina.nome.in_(DISCIPLINAS_ASSOCIADAS),
                            Disciplina.semestre.is_(None)).update(
        {'semestre': '5º semestre'}, synchronize_session=False)
    db.session.commit()
