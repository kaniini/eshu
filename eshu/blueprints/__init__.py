from .. import app
from .index import index_bp


app.blueprint(index_bp)
