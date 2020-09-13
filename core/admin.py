from django.contrib import admin
from core.models import *
from django.contrib.admin.models import LogEntry
from django.db.models import Count, Sum
from django.db.models import Q
from django.db.models.functions import Coalesce


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
    list_display = ('id', 'target_equipment', 'provider', 'remarks', 'state')
    list_display_links = ('id', 'target_equipment',)
    list_filter = ("state",)
    list_editable = ['state']

    def provider(self, obj):
        return obj.target_equipment.provider

    provider.short_description = "提供者"


class UpgradeApplyAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'lab_info', 'address', 'phone', 'state')
    list_display_links = ('id', 'applicant',)
    list_filter = ("state",)
    list_editable = ['state']


class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'content', 'is_read')


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ['content_type', 'object_repr', 'object_id', 'action_time', 'action_flag', 'user', 'change_message']


class SummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/summary.html'

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        user = {
            'normal': Count('id', filter=Q(is_provider=False)),
            'provider': Count('id', filter=Q(is_provider=True)),
        }

        apply = {
            'pending': Count('id', filter=Q(user_apply_set__state=0)),
            'accept': Count('id', filter=Q(user_apply_set__state=1)),
            'refuse': Count('id', filter=Q(user_apply_set__state=2)),
            'return': Count('id', filter=Q(user_apply_set__state=3)),
        }

        rent = {
            'on_rent': Coalesce(Sum('user_apply_set__count', distinct=True, filter=Q(user_apply_set__state=1)), 0),
            'all': Coalesce(Sum('equipments__count', filter=Q(is_provider=True), distinct=True), 0),
        }

        shelf = {
            'pending': Count('equipments__onshelfapply', filter=Q(equipments__onshelfapply__state=0)),
            'accept': Count('equipments__onshelfapply', filter=Q(equipments__onshelfapply__state=1)),
            'refuse': Count('equipments__onshelfapply', filter=Q(equipments__onshelfapply__state=2)),
        }

        response.context_data['user'] = dict(qs.aggregate(**user))
        response.context_data['apply'] = dict(qs.aggregate(**apply))
        response.context_data['rent'] = dict(qs.aggregate(**rent))
        response.context_data['shelf'] = dict(qs.aggregate(**shelf))

        return response


class UserLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'request_type', 'request_query', 'status')

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(BorrowApply, BorrowApplyAdmin)
admin.site.register(UpgradeApply, UpgradeApplyAdmin)
admin.site.register(OnShelfApply, OnShelfApplyAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(UserLog, UserLogAdmin)
admin.site.site_title = '设备租赁智能管理平台'
admin.site.site_header = '后台管理系统'
