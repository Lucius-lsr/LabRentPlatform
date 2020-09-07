# -*- coding: utf-8 -*-
"""
@Time    : 9/7/20 9:59 AM
@Author  : Lucius
@FileName: session_helper.py
@Software: PyCharm
"""


def check_username(request):
    session_id = request.COOKIES.get('session_id', '')  # 通过session_id在数据库中找用户名
    if session_id:
        session_id_username = request.session.get(session_id, '')
        if session_id_username:
            return session_id_username
    return None