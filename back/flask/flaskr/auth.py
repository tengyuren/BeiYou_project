import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.dbmanage import get_db
from flask import request, current_app, g
from .utils.jwt_util import verify_jwt, generate_access_token, generate_refresh_token

from .models import db
from .models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request # 每次调用auth前都会检查
def load_logged_in_user():
    # 1.获取请求头中的token信息 [登录token，刷新token] 规定：前端通过Authorization字段携带token
    token = request.headers.get("Authorization")
    key = current_app.config["JWT_SECRET"]
    # 2.进行token校验  载荷信息有可能为空：token为空，token错误，token过期
    payload = verify_jwt(token, key)
    g.user_id = None
    g.is_refresh = False
    # +权限
    if payload:
        # 3.从载荷字典中提取用户身份信息
        g.user_id = payload.get("user_id")
        g.is_refresh = payload.get("is_refresh", False)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.json['username'].strip()
        password = request.json['password'].strip()

        error = None
        if not username: error = 'Username is required.'
        elif not password: error = 'Password is required.'

        user = User.query.filter_by(username=username).first()
        if user is None: error = '不存在该账号'
        elif not check_password_hash(user.password, password):error = '密码错误'

        if error is None:
            access_token = generate_access_token(user.id)
            refresh_token = generate_refresh_token(user.id)
            return jsonify({
                "code": 20000,
                "msg": "登录成功",
                "access_token": access_token,
                "refresh_token": refresh_token
            })

        return jsonify({ "msg": error })
    else:
        return jsonify({
            "msg": "method not allow"
        })

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.json['username']
        password = request.json['password']

        error = None
        if not username: error = 'Username is required.'
        elif not password: error = 'Password is required.'
        elif User.query.filter_by(username=username).first() is not None: error = "该用户已存在"

        if error is None:
            user = User(username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return jsonify({
                "code": 20000,
                "msg": "用户注册成功"
            }) 

        return jsonify({
            "msg": error
        })
    else:
        return jsonify({
            "msg": "method not allow"
        })



def refresh_token():
    user_id = g.user_id
    is_refresh = g.is_refresh
    if user_id and is_refresh:
        access_token, _ = self._generator_token(user_id)
        return jsonify({
            "code": 20000,
            "access_token": access_token
        })
    else:
        return jsonify({
            "code": 403,
            "msg": "wrong refresh token"
        })

@bp.route('/logout',methods=('GET', 'POST'))
def logout():
    return jsonify({
        "code": 20000,
        "msg": "退出成功"
    })

def get_userinfo():
    pass

def login_required(view): # 登录装饰器
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user_id is None:  # 401 权限认证失败
            return jsonify({
                "code": 50008,
                "msg": "用户未登录，请登录"
            })
        elif g.user_id is not None and g.is_refresh:
            return jsonify({
                "code": 50014,
                "msg": "登录已过期，请重新登录"
            })
        return view(**kwargs)
    return wrapped_view


