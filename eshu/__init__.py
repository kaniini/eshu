from sanic import Sanic
from gino.ext.sanic import Gino

from sanic_jinja2 import SanicJinja2


app = Sanic()
app.config.from_envvar('ESHU_CONFIG')
app.static('/static', app.config.STATIC_DIR)

db = Gino()
db.init_app(app)


jinja = SanicJinja2(app, pkg_name='eshu')


from . import models
