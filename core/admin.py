from django.contrib import admin
from core.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_verified', 'is_provider')
    list_display_links = ('id', 'username',)
    search_fields = ('username', 'email')


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'description', 'provider', 'state_display')
    list_display_links = ('id', 'name',)
    search_fields = ['name']
    list_filter = ("onshelfapply__state",)

    def state_display(self, obj):
        return obj.onshelfapply
    state_display.short_description = "上架情况"


class BorrowApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'borrower', 'target_equipment', 'count', 'owner', 'end_time', 'state')
    list_display_links = ('id', 'borrower', 'target_equipment',)
    list_filter = ("state",)
    date_hierarchy = 'end_time'


class OnShelfApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'target_equipment', 'provider','remarks', 'state')
    list_display_links = ('id', 'target_equipment',)
    list_filter = ("state",)
    list_editable = ['state']

    def provider(self, obj):
        return obj.target_equipment.provider
    provider.short_description = "提供者"


class UpgradeApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'lab_info', 'state')
    list_display_links = ('id', 'applicant',)
    list_filter = ("state",)
    list_editable = ['state']


# Register your models here.
admin.site.register(User, UserAdmin)
# admin.site.register(EmailVerifyCode)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(BorrowApply, BorrowApplyAdmin)
admin.site.register(UpgradeApply, UpgradeApplyAdmin)
admin.site.register(OnShelfApply, OnShelfApplyAdmin)
admin.site.site_title = '设备租赁智能管理平台'
admin.site.site_header = '后台管理系统登录'
