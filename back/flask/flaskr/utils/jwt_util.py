import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_jwt(payload, expiry, secret=None):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 密钥
    :return: jwt
    """
    _payload = {'exp': expiry}
    _payload.update(payload)

    if not secret:
        secret = current_app.config['JWT_SECRET']

    token = jwt.encode(_payload, secret, algorithm='HS256')
    return token


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    if not secret:
        secret = current_app.config['JWT_SECRET']

    try:
        payload = jwt.decode(token, secret, algorithm=['HS256'])
    except jwt.PyJWTError:
        payload = None

    return payload

def generate_refresh_token(user_id, secret=None):
    if not secret:
        secret = current_app.config['JWT_SECRET']
    
    refresh_payload = {
        "user_id": user_id,
        "is_refresh": True
    }
    expires = datetime.utcnow() + timedelta(days=current_app.config["REFRESH_TOKEN_EXPIRE"])
    refresh_token = generate_jwt(payload=refresh_payload, expiry=expires, secret=secret)
    return refresh_token

def generate_access_token(user_id, secret=None):
    if not secret:
        secret = current_app.config['JWT_SECRET']
    
    login_payload = {
        "user_id": user_id,
        "is_refresh": False
    }
    expire_2h = datetime.utcnow() + timedelta(hours=current_app.config["LOGIN_TOKEN_EXPIRE"])
    secret = current_app.config["JWT_SECRET"]
    token = generate_jwt(payload=login_payload, expiry=expire_2h, secret=secret)
    return token