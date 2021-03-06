# 公共错误码
CODE_UNDEFINED = -1
CODE_OK = 0
CODE_SYSTEM_ERROR = 1
CODE_PARAM_WRONG = 2
CODE_NOT_LOGINED = 29
CODE_USER_NOT_EXISTS = 3
CODE_TOKEN_GEN_ERROR = 4
CODE_PASSWORD_ERROR = 5
CODE_TOKEN_ERROR = 6
CODE_NOT_AUTH = 29
CODE_CREATE_UPSTREAM_ERROR = 7
CODE_CREATE_ROUTE_ERROR = 8

MESSAGES = {
    CODE_UNDEFINED: "未定义",
    CODE_OK: "成功",
    CODE_SYSTEM_ERROR: "系统错误",
    CODE_PARAM_WRONG: "参数错误",
    CODE_NOT_LOGINED: "token已过期",
    CODE_USER_NOT_EXISTS: "用户不存在",
    CODE_TOKEN_GEN_ERROR: "生成token失败",
    CODE_PASSWORD_ERROR: "密码错误",
    CODE_TOKEN_ERROR: "解析token失败",
    CODE_NOT_AUTH: "未授权",
    CODE_CREATE_UPSTREAM_ERROR: "创建Upstream失败",
    CODE_CREATE_ROUTE_ERROR: "创建Route失败"
}
