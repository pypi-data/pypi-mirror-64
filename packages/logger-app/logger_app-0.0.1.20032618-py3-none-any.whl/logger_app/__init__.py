# -*- coding: utf-8 -*- 
# @Time     : 2020-02-07 11:26
# @Author   : binger

name = "logger_app"
version_info = (0, 0, 1, 20032618)
__version__ = ".".join([str(v) for v in version_info])
__description__ = '实现对logging的简单扩展'

from .model import LoggerApp, register_formatter_tag_mapper, FormatterRule


def get_flask_unique_request_id(use_md5=True, save=True):
    """
    获取 flask 请求时一个请求路由的唯一id
    :param use_md5: 是否md5
    :return:
    """
    from flask import request, g
    request_id = getattr(g, "_link_id_", None)
    if not request_id:
        request_id = id(request._get_current_object())
        if use_md5:
            import hashlib
            m = hashlib.md5(
                str(request_id).encode("utf-8")
            )
            m.update(request.path.encode("utf-8"))
            request_id = m.hexdigest()
        if save:
            g._link_id_ = request_id
    return request_id
