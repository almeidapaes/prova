from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config import config

bootstrap = Bootstrap()
moment = Moment()
db = SQLAlchemy()

DISCIPLINAS_INICIAIS = ['DSWA5', 'GPSA5', 'IHCA5', 'SODA5', 'PJIA5', 'TCOA5']


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
        from .models import Disciplina
        db.create_all()
        if Disciplina.query.count() == 0:
            db.session.add_all([Disciplina(nome=n) for n in DISCIPLINAS_INICIAIS])
            db.session.commit()

    return app
