from django.db import models
from datetime import datetime


class User(models.Model):
    username = models.CharField(max_length=100)  # 只能是学号
    email = models.EmailField()
    password = models.CharField(max_length=100)
    # phone = models.PhoneNumberField()
    is_verified = models.BooleanField(default=False, verbose_name="是否激活")
    is_provider = models.BooleanField(default=False, verbose_name="是否可以提供设备")

    def to_dict(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'is_verified': self.is_verified,
            'is_provider': self.is_provider
        }

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class EmailVerifyCode(models.Model):
    code = models.CharField(max_length=20, verbose_name="邮箱验证码")
    email = models.EmailField(max_length=200, verbose_name="验证码邮箱")
    send_type = models.IntegerField(choices=((1, 'register'), (2, 'forget'), (3, 'change')), verbose_name="验证码类型")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '邮箱验证码信息'
        verbose_name_plural = verbose_name


class Equipment(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    count = models.IntegerField(default=0)

    provider = models.ForeignKey('User', on_delete=models.CASCADE, related_name='equipments')

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'provider': self.provider.username
        }

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name


class BorrowApply(models.Model):
    borrower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_apply_set')  # 申请人如果被删则删除申请
    count = models.IntegerField(default=0)  # new: borrow number
    target_equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE,
                                         related_name='equipment_apply_set')  # 租借设备如果被删则设为空
    owner = models.ForeignKey('User', on_delete=models.CASCADE,
                                         related_name='owner_apply_set')  # 所有者如果被删则设为空
    end_time = models.DateTimeField()  # 结束时间
    reason = models.TextField(max_length=200)
    state = models.IntegerField(choices=((0, 'pending'), (1, 'accept'), (2, 'refuse'), (3, 'returned')),
                                verbose_name='申请状态')

    def to_dict(self):
        return {
            'borrower': self.borrower.username,
            'count': self.count,
            'target_equipment': self.target_equipment.name,
            'endtime': self.end_time,
            'reason': self.reason,
            'state': self.state
        }

    def __str__(self):
        return '%d: %s租赁%s' % (self.id, self.borrower.username, self.target_equipment.name)

    class Meta:
        verbose_name = '租借申请'
        verbose_name_plural = verbose_name


class OnShelfApply(models.Model):
    count = models.IntegerField(default=0)  # new: count of equipments
    target_equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)  # 租借设备如果被删则设为空
    remarks = models.TextField(max_length=200)
    state = models.IntegerField(choices=((0, 'pending'), (1, 'accept'), (2, 'refuse')), verbose_name='申请状态')

    def __str__(self):
        return self.target_equipment.name

    class Meta:
        verbose_name = '上架申请'
        verbose_name_plural = verbose_name


class UpgradeApply(models.Model):
    applicant = models.ForeignKey('User', on_delete=models.CASCADE)  # 申请人如果被删则删除申请
    lab_info = models.TextField(max_length=200)
    state = models.IntegerField(choices=((0, 'pending'), (1, 'accept'), (2, 'refuse')), verbose_name='申请状态')

    def __str__(self):
        return self.applicant.username

    class Meta:
        verbose_name = '成为提供者申请'
        verbose_name_plural = verbose_name
