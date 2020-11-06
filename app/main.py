import jinja2
from aiohttp import web
from aiohttp_jinja2 import setup as setup_template

from app.settings import get_config, CONFIG_PATH, TEMPLATE_PATH
from app.db import init_pg, close_pg
from app.routes import setup_routes


async def init_app(config):
    app = web.Application()
    app['config'] = config
    setup_routes(app)
    setup_template(app, loader=jinja2.FileSystemLoader(TEMPLATE_PATH))
    app.on_startup.append(init_pg)
    app.on_cleanup.append(close_pg)
    return app


def main():
    config = get_config(CONFIG_PATH)
    app = init_app(config)
    web.run_app(app, host=config['host'], port=config['port'])


if __name__ == '__main__':
    main()
