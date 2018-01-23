from sanic import Blueprint
from .. import app, db, jinja


user_bp = Blueprint('user')


@user_bp.route('/user/login')
async def login(request):
    return jinja.render('login.html', request)


@user_bp.route('/user/create')
async def create(request):
    return jinja.render('signup.html', request)
