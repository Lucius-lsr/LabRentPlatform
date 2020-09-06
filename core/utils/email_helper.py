# -*- coding: utf-8 -*-
"""
@Time    : 9/7/20 12:26 AM
@Author  : Lucius
@FileName: email_helper.py
@Software: PyCharm
"""

from ..models import EmailVerifyCode
from django.core.mail import send_mail
import uuid
import os

EMAIL_FROM = 'labrentplatform@163.com'


def send_email_code(email, send_type, host):
    # 第一步：创建邮箱验证码对象，保存数据库，用来以后做对比
    code = random_id = str(uuid.uuid4())
    verify_code = EmailVerifyCode()
    verify_code.email = email
    verify_code.send_type = send_type
    verify_code.code = code
    verify_code.save()

    # 第二步：正式的发邮件功能
    send_title = ''
    send_body = ''
    if send_type == 1:
        send_title = '欢迎注册实验室设备租赁智能管理平台：'
        send_body = '请点击以下链接进行激活您的账号：\n {}/users/user_verify/'.format(host) + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])

    if send_type == 2:
        send_title = '实验室设备租赁智能管理平台重置密码系统：'
        send_body = '请点击以下链接进行重置您的密码：\n {}/users/user_reset/'.format(host) + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])

    if send_type == 3:
        send_title = '实验室设备租赁智能管理平台修改邮箱验证码：'
        send_body = '您的验证码是：' + code
        send_mail(send_title, send_body, EMAIL_FROM, [email])
