from django.db import models
from datetime import datetime


class User(models.Model):
    username = models.CharField(max_length=100)  # 只能是学号
    email = models.EmailField()
    password = models.CharField(max_length=100)
    phone = models.PhoneNumberField()
    is_verified = models.BooleanField(default=False, verbose_name="是否激活")
    is_provider = models.BooleanField(default=False, verbose_name="是否可以提供设备")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class EmailVerifyCode(models.Model):
    code = models.CharField(max_length=20, verbose_name="邮箱验证码")
    email = models.EmailField(max_length=200, verbose_name="验证码邮箱")
    send_type = models.IntegerField(choices=((1, 'register'), (2, 'forget'), (3, 'change')), verbose_name="验证码类型")
    add_time = models.DateTimeField(default=datetime.now(), verbose_name="添加时间")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '邮箱验证码信息'
        verbose_name_plural = verbose_name


class BorrowApply(models.Model):
    borrower = models.ForeignKey('User', on_delete=models.CASCADE)  # 申请人如果被删则删除申请
    count = models.IntegerField()  # new: borrow number
    target_equipment = models.ForeignKey('Equipment', on_delete=models.SET_NULL)  # 租借设备如果被删则设为空
    end_time = models.DateTimeField()  # 结束时间
    reason = models.TextField(max_length=200)
    state = models.IntegerField(choices=((0, 'pending'), (1, 'accept'), (2, 'refuse')), verbose_name='申请状态')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '租借申请'
        verbose_name_plural = verbose_name


class OnShelfApply(models.Model):
    lender = models.ForeignKey('User', on_delete=models.CASCADE)  # 申请人如果被删则删除申请
    count = models.IntegerField()  # new: count of equipments
    target_equipment = models.ForeignKey('Equipment', on_delete=models.SET_NULL)  # 租借设备如果被删则设为空
    remarks = models.TextField(max_length=200)
    state = models.IntegerField(choices=((0, 'pending'), (1, 'accept'), (2, 'refuse')), verbose_name='申请状态')

    def __str__(self):
        return self.id

    class Meta:
        verbose_name = '上架申请'
        verbose_name_plural = verbose_name


class UpgradeApply(models.Model):
    applicant = models.ForeignKey('User', on_delete=models.CASCADE)  # 申请人如果被删则删除申请
    lab_info = models.TextField(max_length=200)
    state = models.IntegerField(choices=((0, 'pending'), (1, 'accept'), (2, 'refuse')), verbose_name='申请状态')

    def __str__(self):
        return self.applicant

    class Meta:
        verbose_name = '成为提供者申请'
        verbose_name_plural = verbose_name


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    count = models.IntegerField()

    provider = models.ForeignKey("User", on_delete=models.CASCADE, related_name='equipments')

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'provider': self.provider
        }
