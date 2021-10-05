import datetime
import time
import jwt

from config.log import logger

key = "dsfghjhkgfdssfgkj,mll;klk;p;l,"


def get_token(custom):
    try:
        exp = datetime.datetime.now() + datetime.timedelta(days=3)
        token_dict = {
            'exp': int(exp.timestamp()),  # 过期时间
            'iss': 'xiaoduoai',  # 签名
            'iat': int(time.time()),
            'sub': 'jwt_token',
            'custom': custom
        }
        headers = {
            'alg': "HS256",  # 声明所使用的算法
            "typ": "JWT"
        }
        jwt_token = jwt.encode(token_dict, key, algorithm="HS256", headers=headers).decode('utf-8')
        return jwt_token
    except Exception as e:
        logger.error("生成token失败", e)
        return ""


def check_token(token):
    try:
        token_info = jwt.decode(token, key)
        if not token_info:
            return False, "token校验失败", {}
        if token_info.get("exp", 0) < int(time.time()):
            return False, "token校验失败", {}
        return True, "", token_info
    except Exception as e:
        return False, str(e), {}
