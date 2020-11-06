from app import models
from app.settings import get_config, CONFIG_PATH

import sqlalchemy as sa

DSN = "postgresql://{username}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = sa.MetaData()
    meta.create_all(bind=engine, tables=[models.task])


def drop_tables(engine):
    meta = sa.MetaData()
    meta.drop_all(bind=engine, tables=[models.task])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(models.task.insert(), [
        {'title': 'first task',
         'description': 'kahfk jabkjbakj vnaskj ndaksjd nkasjnd kjasnd kjasn dkjasn dkasnjkd'},

        {'title': 'second task',
         'description': 'kahfk jabkjbakj vnaskj ndaksjd nkasjnd kjasnd kjasn dkjasn dkasnjkd'},

        {'title': 'third task',
         'description': 'kahfk jabkjbakj vnaskj ndaksjd nkasjnd kjasnd kjasn dkjasn dkasnjkd'}
    ])


if __name__ == '__main__':
    db_url = DSN.format(**get_config(CONFIG_PATH)['postgres'])
    engine = sa.create_engine(db_url)

    create_tables(engine)
    sample_data(engine)

    # drop_tables(engine)
