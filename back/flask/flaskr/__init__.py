import os

from flask import Flask
from .models import db

def create_app(test_config=None): # 工厂函数
    '''
        instance_relative_config: 告诉应用配置文件是相对于 instance folder 的相对路径
        实例文件夹在 flaskr 包的外面，用于存放本地数据（例如配置密钥和数据库），不应当提交到版本控制系统。
    '''
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping( # 设置初始配置
        SECRET_KEY='dev',
        JWT_SECRET='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_DATABASE_URI='sqlite:///' + os.path.join(app.instance_path, 'flaskr.sqlite'),
        SQLALCHEMY_COMMIT_ON_TEARDOWN=True,
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
        LOGIN_TOKEN_EXPIRE=2,# h
        REFRESH_TOKEN_EXPIRE=14 # d 
    )


    # 测试(如果需要的话)
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Flask不会自动创建实例文件夹，需要确保instance folder存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 注册函数
    from . import dbmanage
    dbmanage.init_app(app)

    from . import models
    models.init_app(app)

    # 注册蓝图
    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')

    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'
    
    return app