from eshu import app, db
from alembic.config import Config
from alembic import command
import sqlalchemy as sa


def main():
    db_engine = sa.create_engine(app.config.DB_ENDPOINT)
    db.create_all(bind=db_engine)
    db_engine.dispose()

    alembic_cfg = Config(app.config.ALEMBIC_CONFIG)
    command.stamp(alembic_cfg, 'head')


if __name__ == '__main__':
    main()


__name__ = 'init-db'
__description__ = 'Initialize the DB'
