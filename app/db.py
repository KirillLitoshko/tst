import asyncpgsa


async def init_pg(app):
    dsn = construct_db_url(app['config']['postgres'])
    engine = await asyncpgsa.create_pool(dsn=dsn)
    app['psql'] = engine


async def close_pg(app):
    app['psql'].close()
    await app['psql'].wait_closed()


def construct_db_url(config):
    dsn = "postgresql://{username}:{password}@{host}:{port}/{database}"
    return dsn.format(**config)
