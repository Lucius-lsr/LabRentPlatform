from django.contrib import admin
from core.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_verified', 'is_provider')
    list_display_links = list_display
    search_fields = ('username', 'email')


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'provider')
    list_display_links = list_display
    search_fields = ['name']
    list_filter = ("onshelfapply__state",)


class BorrowApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'borrower', 'target_equipment', 'count', 'owner', 'end_time', 'state')
    list_display_links = list_display
    date_hierarchy = 'end_time'


class OnShelfApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'target_equipment', 'state')
    list_display_links = list_display
    list_filter = ("state",)


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(EmailVerifyCode)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(BorrowApply, BorrowApplyAdmin)
admin.site.register(UpgradeApply)
admin.site.register(OnShelfApply, OnShelfApplyAdmin)
admin.site.site_title = '设备租赁智能管理平台'
admin.site.site_header = '后台管理系统登录'
