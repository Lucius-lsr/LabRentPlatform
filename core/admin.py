from django.contrib import admin
from core.models import *

# Register your models here.

admin.site.register(User)
admin.site.register(EmailVerifyCode)
admin.site.register(Equipment)
admin.site.register(BorrowApply)
admin.site.register(UpgradeApply)
admin.site.register(OnShelfApply)
