from sanic import Sanic
from gino.ext.sanic import Gino


app = Sanic()
app.config.from_envvar('ESHU_CONFIG')

db = Gino()
db.init_app(app)


from . import models
