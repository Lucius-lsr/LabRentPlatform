from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    is_provider = models.BooleanField()


class BorrowApply(models.Model):
    borrower = models.ForeignKey('User', on_delete=models.CASCADE)  # 申请人如果被删则删除申请
    target_equipment = models.ForeignKey('Equipment', on_delete=models.SET_NULL)  # 租借设备如果被删则设为空
    end_time = models.DateTimeField()  # 结束时间
    reason = models.TextField(max_length=200)
    state = models.IntegerField()  # 0为等待审核，1为审核通过，2及其余为审核拒绝


class OnShelfApply(models.Model):
    lender = models.ForeignKey('User', on_delete=models.CASCADE)  # 申请人如果被删则删除申请
    target_equipment = models.ForeignKey('Equipment', on_delete=models.SET_NULL)  # 租借设备如果被删则设为空
    remarks = models.TextField(max_length=200)
    state = models.IntegerField()  # 0为等待审核，1为审核通过，2及其余为审核拒绝


class UpgradeApply(models.Model):
    applicant = models.ForeignKey('User', on_delete=models.CASCADE)  # 申请人如果被删则删除申请
    lab_info = models.TextField(max_length=200)
    state = models.IntegerField()  # 0为等待审核，1为审核通过，2及其余为审核拒绝

