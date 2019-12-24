# dailin：用来测试一些代码
# 这是没有任何用的文件

import datetime
import time
import jwt


def _encode_token(user_id: str, terminal: str):
    """
    生成认证Token
    :param user_id: 数据库中的if
    :param terminal: terminal_{登陆时间}
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=1),  # 过期时间
            'iat': datetime.datetime.utcnow(),  # 签发时间
            'iss': 'ken',  # 签发人
            'data': {
                'id': user_id,
                'terminal': terminal
            }
        }
        return jwt.encode(
            payload,
            "1213123123",
            algorithm='HS256'
        ).decode("utf-8")
    except Exception as e:
        return e


if __name__ == '__main__':
    token = _encode_token("dailin", "123")
    time.sleep(3)
    token1 = jwt.decode(token, "1213123123", options={'verify_exp': False})
    # token1 = jwt.decode(token, "1213123123", leeway = datetime.timedelta(seconds=0))
    print(token)

    print()
    print(token1)
