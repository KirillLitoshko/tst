from aiohttp import web
import aiohttp_jinja2

from app import models


def redirect(router, route_name):
    location = router[route_name].url_for()
    return web.HTTPFound(location)


@aiohttp_jinja2.template('index.html')
async def index(request):
    async with request.app['psql'].acquire() as conn:
        tasks = await models.get_tasks(conn)
        return {'tasks': tasks}


@aiohttp_jinja2.template('detail.html')
async def task_detail(request):
    async with request.app['psql'].acquire() as conn:
        task_id = request.match_info['task_id']
        try:
            task = await models.get_task_by_id(conn, int(task_id))
        except models.RecordNotFound as exc:
            raise web.HTTPNotFound(text=str(exc))
        return {'task': task}


@aiohttp_jinja2.template('create_edit.html')
async def task_create(request):
    if request.method == "POST":
        form = await request.post()
        async with request.app['psql'].acquire() as conn:
            await models.create_task(conn, form)
            response = redirect(request.app.router, 'index')
            raise response
    return {}


@aiohttp_jinja2.template('create_edit.html')
async def task_update(request):
    if request.method == 'GET':
        async with request.app['psql'].acquire() as conn:
            task_id = request.match_info['task_id']
            try:
                task = await models.get_task_by_id(conn, int(task_id))
            except models.RecordNotFound as exc:
                raise web.HTTPNotFound(text=str(exc))
            return {'task': task}
    if request.method == 'POST':
        form = await request.post()
        async with request.app['psql'].acquire() as conn:
            task_id = request.match_info['task_id']
            await models.update_task(conn, int(task_id), form)
            response = redirect(request.app.router, 'index')
            raise response


async def task_delete(request):
    async with request.app['psql'].acquire() as conn:
        task_id = request.match_info['task_id']
        await models.delete_task(conn, int(task_id))
        response = redirect(request.app.router, 'index')
        raise response
