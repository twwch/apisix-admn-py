from passlib.hash import ldap_sha1 as sha1


def get_sha_password(origin_pwd):
    return sha1.encrypt(origin_pwd)


def fill_login_name(name):
    """用户登录的登录名可填入手机号、邮箱、邮箱前缀， 这里对邮箱前缀补充完整为邮箱"""
    # 手机号码和邮箱原样返回
    if not name:
        return name
    if name[0] == '1' or name.find('@') != -1:
        return name
    return name + "@xiaoduotech.com"
