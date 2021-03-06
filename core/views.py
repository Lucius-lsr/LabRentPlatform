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
import math

from .models import User, BorrowApply, OnShelfApply, UpgradeApply, Equipment, Message
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
        return JsonResponse({'error': '无效的参数'}, status=401)
    if not re.match('.+', username):
        return JsonResponse({'error': '无效的用户名'}, status=400)
    if not re.match('^(.+)@(.+)$', email):
        return JsonResponse({'error': '无效的邮箱'}, status=400)

    user_exist = User.objects.filter(Q(username=username) | Q(email=email))
    if user_exist:
        user_exist = user_exist.first()
        if user_exist.is_verified:  # 已经有用户
            return JsonResponse({'error': '用户已存在'}, status=401)
        else:  # 已经有用户但没有验证
            try:
                send_email_code(email, 1, request.get_host())
            except ConnectionRefusedError:
                return JsonResponse({'error': '邮件发送失败'}, status=400)
            else:
                user_exist.username = username
                user_exist.password = make_password(password)
                user_exist.email = email
                user_exist.save()
                return HttpResponse('验证已重新发送，请尽快前往您的邮箱激活，否则无法登陆')

    try:
        send_email_code(email, 1, request.get_host())
    except ConnectionRefusedError:
        return HttpResponse({'error': '邮件发送失败'}, status=400)
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
                    if (datetime.now() - email_ver.add_time.replace(tzinfo=None)).total_seconds() > 3600 * 24:  # 有效时间1d
                        test = (datetime.now() - email_ver.add_time.replace(tzinfo=None)).total_seconds()
                        email_ver.delete()
                        return HttpResponse(test)
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
        return JsonResponse({'error': '用户不存在'}, status=401)

    user = user.first()
    password_stored = user.password
    password = data.get('password')
    if not check_password(password, password_stored):
        return JsonResponse({'error': '密码错误'}, status=401)
    if not user.is_verified:
        return JsonResponse({'error': '用户尚未激活'}, status=403)

    # update upgrade info
    apply = UpgradeApply.objects.filter(applicant=user)
    if not user.is_provider:
        if apply and apply.first().state == 1:
            user.is_provider = True
            user.save()
            apply.delete()
            return HttpResponse('Notice, you have upgraded!')
    elif apply:
        apply.delete()

    # has logged in
    session_username = check_username(request)
    if session_username:  # 已经登录
        if username == session_username:  # 同一用户
            return JsonResponse({'error': '已经登录'}, status=400)
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
def borrow_apply(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'require POST'}, status=400)
    username = check_username(request)
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
        return JsonResponse({'error': '无效的参数'}, status=400)

    if not target_id or not end_time or count <= 0:
        return JsonResponse({'error': '无效的参数'}, status=400)

    target = Equipment.objects.filter(id=target_id, onshelfapply__state=1)  # 上架商品才能申请
    if not target:
        return JsonResponse({'error': '无效的参数'}, status=400)
    target = target.first()
    if target.count < count:
        return JsonResponse({'error': '数量不足'}, status=400)
    if target.provider.id == borrower.id:
        return JsonResponse({'error': '不能租借自己的设备'}, status=400)

    try:
        BorrowApply.objects.create(borrower=borrower, count=count, target_equipment=target, owner=target.provider,
                                   end_time=end_time, reason=reason, state=0)
        return JsonResponse({'message': 'ok'})
    except django.core.exceptions.ValidationError:
        return JsonResponse({'error': '错误，可能是时间格式问题'}, status=400)


@csrf_exempt
def get_borrow_apply_list(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'require GET'}, status=400)
    username = check_username(request)
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
    user = User.objects.filter(username=username)
    if not user:
        return JsonResponse({'error': 'please login'}, status=401)
    user = user.first()

    data = QueryDict(request.body)
    lab_info = data.get('lab_info')
    address = data.get('address')
    phone = data.get('phone')
    if not lab_info or not address or not phone:
        return JsonResponse({'error': '请填写实验室信息'}, status=400)

    try:
        if user.upgradeapply_set.all():
            previous_apply = user.upgradeapply_set.all().first()
            previous_apply.lab_info = lab_info
            previous_apply.address = address
            previous_apply.phone = phone
            previous_apply.state = 0
            previous_apply.save()
            return JsonResponse({'message': 'modify apply'})
        else:
            UpgradeApply.objects.create(applicant=user, lab_info=lab_info, address=address, phone=phone, state=0)
            return JsonResponse({'message': 'ok'})
    except (TypeError, ValueError):
        return JsonResponse({'error': '申请失败'}, status=401)


# Get equipment list by: username OR equipment
def search_equipment(request):
    username = check_username(request)
    if request.method == 'GET':
        equipment_list = []
        username = request.GET.get('username', "")
        equipment_name = request.GET.get('name', "")
        try:
            page = int(request.GET.get('page', ""))
        except (ValueError, TypeError):
            return JsonResponse({'error': '无效的参数'}, status=400)
        if username:
            try:
                user = User.objects.get(username=username)
                equipment_list = user.equipments.all()
            except:
                return JsonResponse({'error': '用户不存在'}, status=400)
        elif equipment_name:
            equipment_list = Equipment.objects.filter(name__contains=equipment_name, onshelfapply__state=1)  # 上架商品才能被搜索
        else:
            equipment_list = Equipment.objects.filter(onshelfapply__state=1)  # 上架商品才能被搜索
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
            return JsonResponse({'error': '无效的参数'}, status=400)
        username = check_username(request)
        try:
            user = User.objects.get(username=username)
        except:
            return JsonResponse({'error': 'please login'}, status=401)
        if not user.is_provider:
            return JsonResponse({'error': '不是提供者'}, status=403)

        equipment_list = user.equipments.filter(onshelfapply__state=0)
        pending_ = []
        for e in equipment_list:
            dic = e.to_dict()
            dic['state'] = 0
            pending_.append(dic)

        equipment_list = user.equipments.filter(onshelfapply__state=1)
        accept_ = []
        for e in equipment_list:
            dic = e.to_dict()
            dic['state'] = 1
            accept_.append(dic)

        equipment_list = pending_ + accept_

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
        user = User.objects.get(username=username)
        if not user.is_provider:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        if custom_equipment and custom_equipment.provider.username == username:
            custom_equipment.name = name
            custom_equipment.description = description
            custom_equipment.count = count
            custom_equipment.save()
            return JsonResponse({'message': 'ok'})
        else:
            return JsonResponse({'error': '请求被拒绝'}, status=403)
    else:
        return JsonResponse({'error': 'require PUT'}, status=400)


@csrf_exempt
def increase_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        add_count = request.POST.get('count', 1)

        custom_equipment = Equipment.objects.get(id=equipment_id)
        username = check_username(request)
        user = User.objects.get(username=username)
        if not user.is_provider:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        if custom_equipment and custom_equipment.provider.username == username:
            custom_equipment.count += int(add_count)
            custom_equipment.save()
            return JsonResponse({'message': 'ok'})
        else:
            return JsonResponse({'error': '请求被拒绝'}, status=403)
    else:
        return JsonResponse({'error': 'require POST'}, status=400)


@csrf_exempt
def decrease_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        delete_count = request.POST.get('count', 1)

        custom_equipment = Equipment.objects.get(id=equipment_id)
        username = check_username(request)
        user = User.objects.get(username=username)
        if not user.is_provider:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        if custom_equipment and custom_equipment.provider.username == username:
            custom_equipment.count -= int(delete_count)
            custom_equipment.count = max(0, custom_equipment.count)
            custom_equipment.save()
            return JsonResponse({'message': 'ok'})
        else:
            return JsonResponse({'error': '请求被拒绝'}, status=403)
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
        return JsonResponse({'error': '无效的参数'}, status=400)
    try:
        count = int(request.POST.get('count'))
    except (TypeError, ValueError):
        return JsonResponse({'error': '无效的参数'}, status=400)
    username = check_username(request)
    user = User.objects.get(username=username)
    if not user.is_provider:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    new_equipment = Equipment(
        name=name,
        description=description,
        count=count,
        provider=User.objects.get(username=username)
    )
    new_equipment.save()
    apply = OnShelfApply(target_equipment=new_equipment, remarks=remarks, state=0)
    apply.save()
    return JsonResponse({'message': 'ok'})


@csrf_exempt
def off_shelf_equipment(request):
    if request.method == 'POST':
        try:
            equipment_id = request.POST.get('equipment_id', '')
            custom_equipment = Equipment.objects.get(id=equipment_id)
        except:
            return JsonResponse({'error': '设备不存在'}, status=400)
        username = check_username(request)
        user = User.objects.get(username=username)
        if not user.is_provider:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        if custom_equipment and custom_equipment.provider.username == username:
            custom_equipment.delete()
            return JsonResponse({'message': 'ok'})
        else:
            return JsonResponse({'error': '请求被拒绝'}, status=403)
    else:
        return JsonResponse({'error': 'require POST'}, status=400)


def show_borrow_apply_list(request):
    if request.method == 'GET':
        username = check_username(request)
        user = User.objects.get(username=username)
        if not user.is_provider:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        borrow_apply_list = user.owner_apply_set.all()
        borrow_apply_list = [b.to_dict() for b in borrow_apply_list]
        return JsonResponse({
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
        return JsonResponse({'error': '无效的参数'})

    if not id or not flag:
        return JsonResponse({'error': '无效的参数'}, status=400)
    apply = BorrowApply.objects.filter(id=id)
    if not apply:
        return JsonResponse({'error': '租借请求不存在'}, status=400)
    apply = apply.first()
    username = check_username(request)
    user = User.objects.get(username=username)
    if not user.is_provider:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    if apply.owner.username != username:
        return JsonResponse({'error': 'not your equipment'}, status=400)
    if apply.state != 0:
        return JsonResponse({'error': '设备状态不匹配'}, status=400)
    if flag != 1 and flag != 2:
        return JsonResponse({'error': '无效的状态'}, status=400)
    if apply.target_equipment.count < apply.count:
        return JsonResponse({'error': '数量不足'}, status=400)
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
    user = User.objects.get(username=username)
    if not user.is_provider:
        return JsonResponse({'error': 'Permission denied'}, status=403)
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
        return JsonResponse({'error': '无效的参数'}, status=400)
    apply = BorrowApply.objects.filter(id=id)
    if not apply:
        return JsonResponse({'error': '租借请求不存在'}, status=400)
    apply = apply.first()
    username = check_username(request)
    user = User.objects.get(username=username)
    if not user.is_provider:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    if apply not in user.owner_apply_set.all():
        return JsonResponse({'error': '不是您的设备'}, status=400)
    if apply.state == 1:
        apply.state = 3
        apply.target_equipment.count += apply.count
        apply.target_equipment.save()
        apply.save()
        return JsonResponse({'message': 'ok'})
    else:
        return JsonResponse({'error': '不在租借状态'}, status=400)


@csrf_exempt
def send_message(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'require POST'}, status=400)
    receiver_name = request.POST.get('receiver_name', "")
    if not receiver_name:
        return JsonResponse({'error': 'No receiver'}, status=400)
    username = check_username(request)
    sender = User.objects.get(username=username)
    content = request.POST.get('content', '')
    try:
        receiver = User.objects.get(username=receiver_name)
    except:
        return JsonResponse({"error": "发送对象不存在"}, status=400)
    Message(
        sender=sender,
        receiver=receiver,
        content=content
    ).save()
    return JsonResponse({'message': 'ok'})


def get_messages(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'require GET'}, status=400)
    username = check_username(request)
    all_messages = Message.objects.filter(Q(sender__username=username) | Q(receiver__username=username)).order_by('id')
    all_messages = [x.to_dict() for x in all_messages]
    new_messages = [x for x in all_messages if x['receiver'] == username and x['is_read'] == False]
    return JsonResponse({
        'total': len(all_messages),
        'new_message': len(new_messages),
        'messages': all_messages
    })


'''------------extra function-------------'''


@csrf_exempt
def read_messages(request):
    if request.method != 'PUT':
        return JsonResponse({'error': 'require PUT'}, status=400)
    username = check_username(request)
    new_messages = Message.objects.filter(Q(receiver__username=username) & Q(is_read=False))
    for m in new_messages:
        m.is_read = True
        m.save()
    return JsonResponse({'message': 'ok'})


def get_notification(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'require GET'}, status=400)
    username = check_username(request)

    user = User.objects.get(username=username)
    ret = []

    # as borrower
    all_borrow_apply = user.user_apply_set.filter(Q(unread=True), (Q(state=1) | Q(state=2)))
    for apply in all_borrow_apply:
        # apply.unread = False
        apply.save()
        ret.append({'type': 'borrow apply', 'state': apply.state, 'apply': apply.to_dict()})

    # as provider
    equipments = user.equipments.all()
    for equipment in equipments:
        try:
            apply = equipment.onshelfapply
        except:
            continue
        if not apply.unread or apply.state == 0:
            continue
        # apply.unread = False
        apply.save()
        ret.append({'type': 'onshelf apply', 'state': apply.state, 'apply': apply.to_dict()})

    # upgrade
    apply = user.upgradeapply_set.all()
    if apply:
        apply = apply.first()
        if not apply.unread or apply.state == 0:
            pass
        else:
            # apply.unread = False
            apply.save()
            ret.append({'type': 'upgrade apply', 'state': apply.state})

    return JsonResponse({'notification': ret})
