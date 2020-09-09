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
import django.core.exceptions
import re
import uuid
from django.http import QueryDict

from .models import User, BorrowApply, OnShelfApply, UpgradeApply, Equipment
import json

PAGE_SIZE = 10

'''------------normal user-------------'''


@csrf_exempt
def register(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'require POST'}, status=400)

    username = request.POST.get('username')
    email = request.POST.get('email')
    password = request.POST.get('password')
    if not username or not password or not email:
        return JsonResponse({'error': 'invalid parameters'}, status=401)
    if not re.match('.+', username):
        return JsonResponse({'error': 'not valid id'}, status=400)
    if not re.match('^(.+)@(.+)$', email):
        return JsonResponse({'error': 'not email'}, status=400)

    user_exist = User.objects.filter(Q(username=username) | Q(email=email))
    if user_exist:
        user_exist = user_exist.first()
        if user_exist.is_verified:  # 已经有用户
            return JsonResponse({'error': 'user exists'}, status=401)
        else:  # 已经有用户但没有验证
            try:
                send_email_code(email, 1, request.get_host())
            except ConnectionRefusedError:
                return JsonResponse({'error': 'fail to send email'}, status=500)
            else:
                user_exist.username = username
                user_exist.password = make_password(password)
                user_exist.email = email
                user_exist.save()
                return HttpResponse('验证已重新发送，请尽快前往您的邮箱激活，否则无法登陆')

    try:
        send_email_code(email, 1, request.get_host())
    except ConnectionRefusedError:
        return HttpResponse({'error': 'fail to send email'}, status=500)
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
    if request.method != 'PATCH':
        return JsonResponse({'error': 'require PATCH'}, status=400)

    data = QueryDict(request.body)

    username = data.get('username')
    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'error': 'no such a user'}, status=401)

    user = user.first()
    password_stored = user.password
    password = data.get('password')
    if not check_password(password, password_stored):
        return JsonResponse({'error': 'password is wrong'}, status=401)
    if not user.is_verified:
        return JsonResponse({'error': 'have not be verified'}, status=403)

    # has logged in
    session_username = check_username(request)
    if session_username:  # 已经登录
        if username == session_username:  # 同一用户
            # update upgrade info
            if not user.is_provider:
                apply = UpgradeApply.objects.filter(applicant=user)
                if apply and apply.first().state == 1:
                    user.is_provider = True
                    user.save()
                    apply.delete()
                    return HttpResponse('Notice, you have upgraded!')
            return JsonResponse({'error': 'has logged in'}, status=401)
        else:  # 不同用户
            session_id = request.COOKIES.get('session_id', '')
            request.session.delete(session_id)  # 删除前一个登录状态

    # success
    random_id = str(uuid.uuid4())
    request.session[random_id] = username  # 服务器写入session
    res = JsonResponse({'user': username, 'isprovider': user.is_provider})
    res.set_cookie('session_id', random_id)  # 返回给浏览器cookies

    return res


@csrf_exempt
def logout(request):
    if request.method != 'PATCH':
        return JsonResponse({'error': 'require PATCH'}, status=400)

    session_id = request.COOKIES.get('session_id', '')  # 通过session_id在数据库中找用户名
    if session_id:
        session_id_username = request.session.get(session_id, '')
        if session_id_username:
            request.session.delete(session_id)
            res = JsonResponse({'message': 'ok'})
            res.delete_cookie('session_id')
            return res
    return JsonResponse({'error': 'no valid session'}, status=401)


@csrf_exempt
def show_all_equipments(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'require GET'}, status=400)

    try:
        page = int(request.GET.get('page', ""))
    except (ValueError, TypeError):
        return JsonResponse({'error': 'invalid parameters'}, status=400)

    name = request.GET.get('name', "")

    equipment_list = Equipment.objects.filter(name__contains=name, onshelfapply__state=1)  # 上架商品才能查看

    total_page = int((len(equipment_list) + PAGE_SIZE - 1) / PAGE_SIZE)
    equipment_list = equipment_list[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]

    ret_list = [e.to_dict() for e in equipment_list]

    return JsonResponse({'page': page, 'total_page': total_page, 'posts': ret_list})


@csrf_exempt
def borrow_apply(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'require POST'}, status=400)
    username = check_username(request)
    if not username:
        return JsonResponse({'error': 'please login'}, status=401)
    borrower = User.objects.filter(username=username)
    if not borrower:
        return JsonResponse({'error': 'please login'}, status=401)
    borrower = borrower.first()

    target_id = request.POST.get('id', "")
    end_time = request.POST.get('endtime', "")
    reason = request.POST.get('reason', "")
    try:
        count = int(request.POST.get('count', ""))
    except (ValueError, TypeError):
        return JsonResponse({'error': 'invalid parameters'}, status=400)

    if not target_id or not end_time or count <= 0:
        return JsonResponse({'error': 'invalid parameters'}, status=400)

    target = Equipment.objects.filter(id=target_id, onshelfapply__state=1)  # 上架商品才能申请
    if not target:
        return JsonResponse({'error': 'invalid id'}, status=400)
    target = target.first()
    if target.count < count:
        return JsonResponse({'error': 'not enough'}, status=400)

    try:
        BorrowApply.objects.create(borrower=borrower, count=count, target_equipment=target, owner=target.provider,
                                   end_time=end_time, reason=reason, state=0)
        return JsonResponse({'message': 'ok'})
    except django.core.exceptions.ValidationError:
        return JsonResponse({'error': 'format error'}, status=400)


@csrf_exempt
def get_borrow_apply_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'require GET'}, status=400)
    username = check_username(request)
    if not username:
        return JsonResponse({'error': 'please login'}, status=401)
    borrower = User.objects.filter(username=username)
    if not borrower:
        return JsonResponse({'error': 'please login'}, status=401)
    borrower = borrower.first()

    borrow_applies = borrower.user_apply_set.all()
    ret = []
    for a in borrow_applies:
        ret.append(a.to_dict())

    return JsonResponse({'posts': ret})


@csrf_exempt
def get_borrow_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'require GET'}, status=400)
    username = check_username(request)
    if not username:
        return JsonResponse({'error': 'please login'}, status=401)
    borrower = User.objects.filter(username=username)
    if not borrower:
        return JsonResponse({'error': 'please login'}, status=401)
    borrower = borrower.first()
    current_borrow = borrower.user_apply_set.filter(state=1)
    ret = []
    for c in current_borrow:
        ret.append(c.to_dict())

    return JsonResponse({'posts': ret})


@csrf_exempt
def upgrade_apply(request):
    if request.method != 'PUT':
        return JsonResponse({'error': 'require PUT'}, status=400)
    username = check_username(request)
    if not username:
        return JsonResponse({'error': 'please login'}, status=401)
    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'error': 'please login'}, status=401)
    user = user.first()

    data = QueryDict(request.body)
    lab_info = data.get('lab_info')
    if not lab_info:
        return JsonResponse({'error': 'require lab information'}, status=400)

    try:
        if user.upgradeapply_set.all():  # 已经有申请了
            previous_apply = user.upgradeapply_set.all().first()
            if previous_apply.state == 1:
                return JsonResponse({'error': 'has upgraded'}, status=400)
            previous_apply.lab_info = lab_info
            previous_apply.state = 0
            previous_apply.save()
            return JsonResponse({'message': 'modify apply'})
        else:
            UpgradeApply.objects.create(applicant=user, lab_info=lab_info, state=0)
            return JsonResponse({'message': 'ok'})
    except (TypeError, ValueError):
        return JsonResponse({'error': 'fail to apply'}, status=401)


# Get equipment list by: username OR equipment
def search_equipment(request):
    if request.method == 'GET':
        equipment_list = []
        username = request.GET.get('username', "")
        equipment_name = request.GET.get('name', "")
        try:
            page = int(request.GET.get('page', ""))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'invalid parameters'}, status=400)
        if username:
            try:
                user = User.objects.get(username=username)
                equipment_list = user.equipments.all()
            except:
                return JsonResponse({'error': 'no this user'}, status=400)
        elif equipment_name:
            equipment_list = Equipment.objects.filter(name__contains=equipment_name, onshelfapply__state=1)  # 上架商品才能被搜索
        equipment_list = [e.to_dict() for e in equipment_list]
        total_page = int((len(equipment_list) + PAGE_SIZE - 1) / PAGE_SIZE)
        equipment_list = equipment_list[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]
        return JsonResponse({
            'page': page,
            'total_page': total_page,
            'posts': equipment_list
        })
    else:
        return JsonResponse({'error': 'require GET'}, status=400)


'''------------provider user-------------'''


def get_my_equipment_list(request):
    if request.method == 'GET':
        try:
            page = int(request.GET.get('page', ""))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'invalid parameters'}, status=400)
        username = check_username(request)
        user = User.objects.get(username=username)
        if not user.is_provider:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        equipment_list = user.equipments.all()
        equipment_list = [e.to_dict() for e in equipment_list]
        total_page = int((len(equipment_list) + PAGE_SIZE - 1) / PAGE_SIZE)
        equipment_list = equipment_list[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]
        return JsonResponse({
            'page': page,
            'total_page': total_page,
            'posts': equipment_list
        })
    else:
        return JsonResponse({'error': 'require GET'}, status=400)


@csrf_exempt
def edit_equipment(request):
    if request.method == 'PUT':
        data = QueryDict(request.body)
        equipment_id = data.get('id')
        name = data.get('name')
        description = data.get('description')
        count = data.get('count')

        custom_equipment = Equipment.objects.get(id=equipment_id)
        username = check_username(request)
        if custom_equipment and custom_equipment.provider.username == username:
            custom_equipment.name = name
            custom_equipment.name = description
            custom_equipment.name = count
            custom_equipment.save()
            return JsonResponse({'message': 'ok'})
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    else:
        return JsonResponse({'error': 'require PUT'}, status=400)


@csrf_exempt
def increase_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        add_count = request.POST.get('count', 1)

        custom_equipment = Equipment.objects.get(id=equipment_id)
        username = check_username(request)
        if custom_equipment and custom_equipment.provider.username == username:
            custom_equipment.count += int(add_count)
            custom_equipment.save()
            return JsonResponse({'message': 'ok'})
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    else:
        return JsonResponse({'error': 'require POST'}, status=400)


@csrf_exempt
def decrease_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        delete_count = request.POST.get('count', 1)

        custom_equipment = Equipment.objects.get(id=equipment_id)
        username = check_username(request)
        if custom_equipment and custom_equipment.provider.username == username:
            custom_equipment.count -= int(delete_count)
            custom_equipment.save()
            return JsonResponse({'message': 'ok'})
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    else:
        return JsonResponse({'error': 'require POST'}, status=400)


@csrf_exempt
def on_shelf_equipment(request):
    if not request.method == 'POST':
        return JsonResponse({'error': 'require POST'}, status=400)
    name = request.POST.get('name')
    description = request.POST.get('description')
    remarks = request.POST.get('remarks')
    if not name or not description or not remarks:
        return JsonResponse({'error': 'invalid parameters'}, status=400)
    try:
        count = int(request.POST.get('count'))
    except (TypeError, ValueError):
        return JsonResponse({'error': 'invalid parameters'}, status=400)
    new_equipment = Equipment(
        name=name,
        description=description,
        count=count,
        provider=User.objects.get(username=check_username(request))
    )
    new_equipment.save()
    apply = OnShelfApply(target_equipment=new_equipment, remarks=remarks, state=0)
    apply.save()
    return JsonResponse({'message': 'ok'})


@csrf_exempt
def off_shelf_equipment(request):
    if request.method == 'DELETE':
        data = QueryDict(request.body)
        equipment_id = data.get('equipment_id')
        custom_equipment = Equipment.objects.get(id=equipment_id)
        username = check_username(request)
        if custom_equipment and custom_equipment.provider.username == username:
            custom_equipment.delete()
            return JsonResponse({'message': 'ok'})
        else:
            return JsonResponse({'error': 'Permission denied'}, status=403)
    else:
        return JsonResponse({'error': 'require DELETE'}, status=400)


def show_borrow_apply_list(request):
    if request.method == 'GET':
        page = request.GET.get('page', 1)
        username = check_username(request)
        user = User.objects.get(username=username)
        borrow_apply_list = user.borrowApplies.all()
        borrow_apply_list = [b.to_dict() for b in borrow_apply_list]
        total_page = int((len(borrow_apply_list) + PAGE_SIZE - 1) / PAGE_SIZE)
        borrow_apply_list = borrow_apply_list[(page - 1) * PAGE_SIZE: page * PAGE_SIZE]
        return JsonResponse({
            'page': page,
            'total_page': total_page,
            'borrow_apply_list': borrow_apply_list
        })
    else:
        return JsonResponse({'error': 'require POST'}, status=400)


@csrf_exempt
def reply_borrow_apply(request):
    if request.method != 'PUT':
        return JsonResponse({'error': 'require PUT'}, status=400)
    data = QueryDict(request.body)
    id = data.get('id')
    try:
        flag = int(data.get('flag'))
    except (ValueError, TypeError):
        return JsonResponse({'error': 'invalid parameters'})

    if not id or not flag:
        return JsonResponse({'error': 'invalid parameters'}, status=400)
    apply = BorrowApply.objects.filter(id=id)
    if not apply:
        return JsonResponse({'error': 'apply does not exist'}, status=400)
    apply = apply.first()
    if apply.state != 0:
        return JsonResponse({'error': 'can not accept/refuse this apply'}, status=400)
    if flag != 1 and flag != 2:
        return JsonResponse({'error': 'wrong flag'}, status=400)
    if apply.target_equipment.count < apply.count:
        return JsonResponse({'error': 'not enough'}, status=400)
    if flag == 1:
        apply.target_equipment.count -= apply.count
        apply.target_equipment.save()
    apply.state = flag
    apply.save()
    return JsonResponse({'message': 'ok'})


@csrf_exempt
def get_lend_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'require GET'}, status=400)
    username = check_username(request)
    if not username:
        return JsonResponse({'error': 'please login'}, status=401)
    lender = User.objects.filter(username=username)
    if not lender:
        return JsonResponse({'error': 'please login'}, status=401)
    lender = lender.first()

    apply_list = lender.owner_apply_set.filter(Q(state=1) | Q(state=3))
    ret = []
    for apply in apply_list:
        ret.append(apply.to_dict())

    return JsonResponse({'posts': ret})


@csrf_exempt
def confirm_return(request):
    if request.method != 'PUT':
        return JsonResponse({'error': 'require PUT'}, status=400)
    data = QueryDict(request.body)
    id = data.get('id')
    if not id:
        return JsonResponse({'error': 'invalid parameters'}, status=400)
    apply = BorrowApply.objects.filter(id=id)
    if not apply:
        return JsonResponse({'error': 'apply does not exist'}, status=400)
    apply = apply.first()
    if apply.state == 1:
        apply.state = 3
        apply.target_equipment.count += apply.count
        apply.target_equipment.save()
        apply.save()
        return JsonResponse({'message': 'ok'})
    else:
        return JsonResponse({'error': 'not in the lease'}, status=400)


'''------------extra function-------------'''


def get_notification(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'require GET'}, status=400)
    username = check_username(request)

    user = User.objects.get(username=username)
    ret = []

    # as borrower
    all_borrow_apply = user.user_apply_set.filter(Q(unread=True), (Q(state=1) | Q(state=2)))
    for apply in all_borrow_apply:
        apply.unread = False
        apply.save()
        ret.append({'type': 'borrow apply', 'state': apply.state, 'apply': apply.to_dict()})

    # as provider
    equipments = user.equipments.all()
    for equipment in equipments:
        apply = equipment.onshelfapply
        if not apply.unread or apply.state == 0:
            continue
        apply.unread = False
        apply.save()
        ret.append({'type': 'onshelf apply', 'state': apply.state, 'apply': apply.to_dict()})

    # upgrade
    apply = user.upgradeapply_set.all()
    if apply:
        apply = apply.first()
        if not apply.unread or apply.state == 0:
            pass
        else:
            apply.unread = False
            apply.save()
            ret.append({'type': 'upgrade apply', 'state': apply.state})

    return JsonResponse({'notification': ret})
