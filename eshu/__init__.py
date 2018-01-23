import asyncio
import aioredis
from sanic import Sanic
from gino.ext.sanic import Gino

from .aioredis_session import RedisSessionInterface
from sanic_jinja2 import SanicJinja2


app = Sanic()
app.config.from_envvar('ESHU_CONFIG')
app.static('/static', app.config.STATIC_DIR)

db = Gino()
db.init_app(app)


from . import locale
class EshuJinja(SanicJinja2):
    # XXX - implement me for real
    def fake_trans(self, text, *args, **kwargs):
        return locale.translate(text, locale.DefaultLocale)


jinja = EshuJinja(app, pkg_name='eshu')


class RedisPool:
    _pool = None

    async def get_redis_pool(self):
        if not self._pool:
            self._pool = await aioredis.create_redis_pool(app.config.REDIS_ENDPOINT)

        return self._pool


redispool = RedisPool()
session = RedisSessionInterface(redispool.get_redis_pool)


@app.middleware('request')
async def add_session_to_request(request):
    await session.open(request)


@app.middleware('response')
async def save_session(request, response):
    await session.save(request, response)


from . import models
from . import blueprints
