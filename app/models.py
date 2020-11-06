import sqlalchemy as sa
from datetime import date

meta = sa.MetaData()

task = sa.Table(
    'tasks', meta,
    sa.Column('id', sa.INTEGER, primary_key=True),
    sa.Column('title', sa.String(150), unique=True, nullable=False),
    sa.Column('description', sa.Text, nullable=False),
    sa.Column('created', sa.Date, default=date.today, nullable=False),
    sa.Column('updated', sa.DateTime, default=date.today, onupdate=date.today, nullable=False)
)


async def get_tasks(conn):
    records = await conn.fetch(
        task.select().order_by(task.c.id.desc())
    )
    return records


async def get_task_by_id(conn, task_id):
    record = await conn.fetchrow(
        task.select().where(task.c.id == task_id)
    )
    if not record:
        msg = "Task with id: {} doesn't exists"
        raise RecordNotFound(msg.format(task_id))
    return record


async def create_task(conn, form):
    action = task.insert().values(title=form['title'], description=form['description'])
    await conn.execute(action)


async def delete_task(conn, task_id):
    action = task.delete().where(task.c.id == task_id)
    await conn.execute(action)


async def update_task(conn, task_id, form):
    action = task.update().where(task.c.id == task_id).values(title=form['title'], description=form['description'])
    await conn.execute(action)


class RecordNotFound(Exception):
    pass
