from sanic import Blueprint
from .. import app, db, jinja


index_bp = Blueprint('index')


@index_bp.route('/')
async def index(request):
    return jinja.render('index.html', request)

