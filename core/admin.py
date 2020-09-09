from django.contrib import admin
from core.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_verified', 'is_provider')


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'provider')


class BorrowApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'borrower', 'target_equipment', 'count', 'owner', 'end_time', 'state')


class OnShelfApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'target_equipment', 'state')


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(EmailVerifyCode)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(BorrowApply, BorrowApplyAdmin)
admin.site.register(UpgradeApply)
admin.site.register(OnShelfApply, OnShelfApplyAdmin)
