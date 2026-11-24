import os

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'))

from app import create_app, db  # noqa: E402
from app.models import Disciplina, Professor  # noqa: E402

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Disciplina=Disciplina, Professor=Professor)
