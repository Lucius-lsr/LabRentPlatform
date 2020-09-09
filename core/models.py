from django.db import models
from datetime import datetime


class User(models.Model):
    username = models.CharField(max_length=100, verbose_name="用户名")  # 只能是学号
    email = models.EmailField(verbose_name="邮箱")
    password = models.CharField(max_length=100)
    # phone = models.PhoneNumberField()
    is_verified = models.BooleanField(default=False, verbose_name="是否激活")
    is_provider = models.BooleanField(default=False, verbose_name="是否升级")

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'is_verified': self.is_verified,
            'is_provider': self.is_provider
        }

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户详情'
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
    name = models.CharField(max_length=50, verbose_name="名称")
    description = models.CharField(max_length=500, verbose_name="简介")
    count = models.IntegerField(default=0, verbose_name="数量")

    provider = models.ForeignKey('User', on_delete=models.CASCADE, related_name='equipments', verbose_name="所有者")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'count': self.count,
            'provider': self.provider.username
        }

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '设备详情'
        verbose_name_plural = verbose_name


class BorrowApply(models.Model):
    borrower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='user_apply_set', verbose_name='申请人')
    count = models.IntegerField(default=0, verbose_name='申请数量')  # new: borrow number
    target_equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='equipment_apply_set',
                                         verbose_name='申请设备')
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name='owner_apply_set', verbose_name='所有者')
    end_time = models.DateTimeField(verbose_name='归还时间')  # 归还时间
    reason = models.TextField(max_length=200, verbose_name='申请理由')
    state = models.IntegerField(choices=((0, '等待确认'), (1, '已租借'), (2, '已拒绝'), (3, '已归还')), verbose_name='租借状态')

    def to_dict(self):
        return {
            'id': self.id,
            'borrower': self.borrower.username,
            'count': self.count,
            'target_equipment': self.target_equipment.to_dict(),
            'endtime': self.end_time,
            'reason': self.reason,
            'state': self.state
        }

    def __str__(self):
        return '%s租赁%s' % (self.borrower.username, self.target_equipment.name)

    class Meta:
        verbose_name = '租借申请'
        verbose_name_plural = verbose_name


class OnShelfApply(models.Model):
    target_equipment = models.OneToOneField(Equipment, on_delete=models.CASCADE, verbose_name='设备')
    remarks = models.TextField(max_length=200, verbose_name='上架理由')
    state = models.IntegerField(choices=((0, '等待确认'), (1, '已上架'), (2, '已拒绝')), verbose_name='上架状态')

    def __str__(self):
        dic = {0: '等待确认', 1: '已上架', 2: '已拒绝'}
        return dic[self.state]

    class Meta:
        verbose_name = '上架申请'
        verbose_name_plural = verbose_name


class UpgradeApply(models.Model):
    applicant = models.OneToOneField('User', on_delete=models.CASCADE, verbose_name='申请人')  # 申请人如果被删则删除申请
    lab_info = models.TextField(max_length=200, verbose_name='申请理由')
    state = models.IntegerField(choices=((0, '等待确认'), (1, '已升级'), (2, '已拒绝')), verbose_name='升级状态')

    def __str__(self):
        return self.applicant.username

    class Meta:
        verbose_name = '升级申请'
        verbose_name_plural = verbose_name
