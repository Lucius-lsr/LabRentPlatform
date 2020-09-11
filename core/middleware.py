# -*- coding: utf-8 -*-
"""
@Time    : 9/11/20 11:37 PM
@Author  : Lucius
@FileName: middleware.py
@Software: PyCharm
"""

from django.http import HttpResponse, JsonResponse

from .utils.session_helper import check_username
from .models import UserLog, User


class CheckLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        list_path = request.path.split('/')
        query_path = ['register', 'login', 'user_verify', 'admin']
        exempt = False
        for query in query_path:
            for path in list_path:
                if query == path:
                    exempt = True

        if not exempt:
            username = check_username(request)  # 检查登录状态
            if not username:
                return JsonResponse({'error': 'please login'}, status=401)

        response = self.get_response(request)

        return response


class UserLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if 'admin' in request.path.split('/'):
            return response

        username = check_username(request)
        user = User.objects.filter(username=username)
        if user:
            user = user.first()
            param = request.path.split('/')[-1]
            request_query = ''
            if '?' in param:
                request_type = param.split('?')[0]
                request_query = param.split('?')[1]
            else:
                request_type = param
            request_body = str(request.body)[2:-1]
            status = response.status_code

            UserLog.objects.create(user=user, request_type=request_type, request_query=request_query,
                                   request_body=request_body, status=status)

        return response
