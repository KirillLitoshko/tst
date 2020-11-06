from app import views
from app.settings import STATIC_URL, STATIC_ROOT


def setup_routes(app):
    app.router.add_get('/', views.index, name='index')
    app.router.add_get('/{task_id}', views.task_detail, name='task_detail')
    app.router.add_get('/{task_id}/delete', views.task_delete, name='task_delete')
    app.router.add_get('/{task_id}/update', views.task_update, name='task_update')
    app.router.add_post('/{task_id}/update', views.task_update, name='task_update')
    app.router.add_get('/task/create', views.task_create, name='task_create')
    app.router.add_post('/task/create', views.task_create, name='task_create')
    app.router.add_static(STATIC_URL, path=STATIC_ROOT, name='static')
