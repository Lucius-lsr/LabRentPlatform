from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.hashers import make_password, check_password
from core.models import *
from core.utils.email_helper import send_email_code
from core.utils.session_helper import check_username
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from datetime import datetime
import re
import uuid

from .models import User, BorrowApply, OnShelfApply, UpgradeApply, Equipment
from django.http import HttpResponse
import json
# Create your views here.

'''------------normal user-------------'''


@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'require POST'})

    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if not username or not password or not email:
        return JsonResponse({'error': 'invalid parameters'})
    if not re.match('\d{10}', username):
        return JsonResponse({'error': 'not student id'})
    if not re.match('^(.+)@mail(s?).tsinghua.edu.cn$', email):
        return JsonResponse({'error': 'not tsinghua email'})

    user_exist = User.objects.filter(Q(username=username) | Q(email=email))
    if user_exist:
        user_exist = user_exist.first()
        if user_exist.is_verified:  # 已经有用户
            return JsonResponse({'error': 'user exists'})
        else:  # 已经有用户但没有验证
            try:
                send_email_code(email, 1, request.get_host())
            except ConnectionRefusedError:
                return JsonResponse({'error': 'fail to send email'})
            else:
                user_exist.username = username
                user_exist.password = make_password(password)
                user_exist.email = email
                user_exist.save()
                return HttpResponse('验证已重新发送，请尽快前往您的邮箱激活，否则无法登陆')

    try:
        send_email_code(email, 1, request.get_host())
    except ConnectionRefusedError:
        return HttpResponse('请尽快前往您的邮箱激活，否则无法登陆')
    else:
        user = User()
        user.username = username
        user.password = make_password(password)
        user.email = email
        user.save()
        return HttpResponse('请尽快前往您的邮箱激活，否则无法登陆')


@csrf_exempt
def user_verify(request, code):
    if code:
        email_ver_list = EmailVerifyCode.objects.filter(code=code)
        if email_ver_list:
            email_ver = email_ver_list.first()
            email = email_ver.email
            user_list = User.objects.filter(email=email)
            if user_list:
                user = user_list.first()
                if not user.is_verified:
                    if (datetime.now() - email_ver.add_time.replace(tzinfo=None)).total_seconds() > 3600:  # 有效时间1h
                        email_ver.delete()
                        return HttpResponse('验证已过期，验证失效')
                    else:
                        user.is_verified = True
                        user.save()
                        email_ver.delete()
                        return HttpResponse('验证成功！')
                else:
                    email_ver.delete()
                    return HttpResponse('用户已注册，验证失效')

    return HttpResponse('验证失败')


@csrf_exempt
def login(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'require POST'})

    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'error': 'no such a user'})

    user = user.first()
    password_stored = user.password
    password = request.POST.get('password')
    if not check_password(password, password_stored):
        return JsonResponse({'error': 'password is wrong'})

    # has logged in
    session_id = request.COOKIES.get('session_id', '')  # 通过session_id在数据库中找用户名
    if session_id:
        session_id_username = request.session.get(session_id, '')
        if session_id_username:
            return JsonResponse({'error': 'has logged in'})

    # success
    random_id = str(uuid.uuid4())
    request.session[random_id] = username  # 服务器写入session
    res = JsonResponse({'user': username})
    res.set_cookie('session_id', random_id)  # 返回给浏览器cookies

    return res


@csrf_exempt
def logout(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'require POST'})

    session_id = request.COOKIES.get('session_id', '')  # 通过session_id在数据库中找用户名
    if session_id:
        session_id_username = request.session.get(session_id, '')
        if session_id_username:
            request.session.delete(session_id)
            res = JsonResponse({'user': session_id_username})
            res.delete_cookie('session_id')
            return res
    return JsonResponse({'error': 'no valid session'})


def show_equipment(request):
    username = check_username(request)
    pass


def borrow_apply(request):
    username = check_username(request)
    pass


def get_borrow_apply_list(request):
    username = check_username(request)
    pass


def get_borrow_list(request):
    username = check_username(request)
    pass


def upgrade_apply(request):
    username = check_username(request)
    pass


def search_equipment(request):
    if request.method == 'GET':
        equipment_list = []
        username = request.GET.get('username', "")
        equipment_name = request.GET.get('name', "")
        if username:
            user = User.objects.get(username=username)
            equipment_list = user.equipments.all()
        elif equipment_name:
            equipment_list = Equipment.objects.filter(name__contains=equipment_name)
        equipment_list = [e.to_dict() for e in equipment_list]
        return HttpResponse(json.dumps(equipment_list), content_type="json")


'''------------provider user-------------'''


def edit_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        count = request.POST.get('count')

        custom_equipment = Equipment.objects.get(id=equipment_id)
        custom_equipment.name = name
        custom_equipment.name = description
        custom_equipment.name = count
        custom_equipment.save()
        return HttpResponse(json.dumps({
            'message': 'ok'
        }), content_type="json")


def add_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        add_count = request.POST.get('addcount', 1)
        custom_equipment = Equipment.objects.get(id=equipment_id)
        custom_equipment.count += add_count
        custom_equipment.save()
        return HttpResponse(json.dumps({
            'message': 'ok'
        }), content_type="json")


def delete_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        delete_count = request.POST.get('deletecount', 1)
        custom_equipment = Equipment.objects.get(id=equipment_id)
        custom_equipment.count -= delete_count
        custom_equipment.save()
        return HttpResponse(json.dumps({
            'message': 'ok'
        }), content_type="json")


def on_shelf_equipment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        count = request.POST.get('count')
        Equipment(
            name=name,
            description=description,
            count=count
        ).save()
        return HttpResponse(json.dumps({
            'message': 'ok'
        }), content_type="json")


def off_shelf_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        Equipment.objects.get(id=equipment_id).delete()
        return HttpResponse(json.dumps({
            'message': 'ok'
        }), content_type="json")


def show_borrow_apply_list(request):
    pass


def reply_borrow_apply(request):
    pass


def get_lend_list(request):
    pass


def confirm_return(request):
    pass
