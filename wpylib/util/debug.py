"""
@File: debug.py
@Date: 2024/1/13 14:07
"""
import platform
import sys

if sys.version_info.major >= 3:
    from shlex import quote
else:
    from pipes import quote


def to_curl(request, compressed=False, verify=True):
    """
    :param request:请求对象
    :param compressed: 是否压缩
    :param verify: 是否开启验证
    """
    parts = [
        ('curl', None),
        ('-X', request.method),
    ]

    for k, v in sorted(request.headers.items()):
        parts += [('-H', '{0}: {1}'.format(k, v))]

    if request.body:
        body = request.body
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        parts += [('-d', body)]

    if compressed:
        parts += [('--compressed', None)]

    if not verify:
        parts += [('--insecure', None)]

    parts += [(None, request.url)]

    flat_parts = []
    for k, v in parts:
        if k:
            flat_parts.append(quote(k))
        if v:
            flat_parts.append(quote(v))

    return ' '.join(flat_parts)


def is_debugging():
    """
    当前是否是在调试
    """
    # 在DEBUG, 且是mac电脑, 且当前项目目录是以/Users/开头
    # 比如在IDE中点击调试按钮时, sys.gettrace()才不为空, is_debugging()才会返回True
    # 但是在IDE中点击运行按钮时, sys.gettrace()就会为空, is_debugging()就会返回False
    return sys.gettrace() is not None and platform.system() == "Darwin" and __file__.startswith("/Users/")


def pretty_print_request(response):
    """
    打印请求
    :param: req 请求对象
    """
    req = response.request
    print("\n=========================Curl Request=========================")
    print(to_curl(req))
    print("=========================Request Start==========================")
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------request body-----------',
        req.method + ': ' + req.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))
    print('-----------response body-----------')
    print(response.text)
    print("=========================Request End============================\n")
