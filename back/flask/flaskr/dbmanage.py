import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from .models import db

'''
g 是一个特殊对象，独立于每一个请求。在处理请求过程中，它可以用于储存可能多个函数都会用到的数据。
'''

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None: db.close()

def init_db(): # 根据schema.sql初始化数据库
    db = get_db()
    with current_app.open_resource('schema.sql') as f: # 路径相对于/flaskr
        db.executescript(f.read().decode('utf8'))


@click.command('init-db') # 成为flask cli的指令
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app): # 在应用实例中注册函数
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

