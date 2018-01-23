from .. import app
from .index import index_bp
from .user import user_bp


app.blueprint(index_bp)
app.blueprint(user_bp)
