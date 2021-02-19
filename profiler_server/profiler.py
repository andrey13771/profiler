from app import app, db
from app.models.models import User, TabInfo, InputInfo


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'TabInfo': TabInfo, 'InputInfo': InputInfo}
