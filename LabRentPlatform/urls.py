"""LabRentPlatform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 普通用户
    path('api/v1/register', views.register),
    re_path(r'^users/user_verify/(.+)$', views.user_verify),
    path('api/v1/login', views.login),
    path('api/v1/logout', views.logout),
    path('api/v1/post', views.show_all_equipments),
    path('api/v1/apply', views.borrow_apply),
    path('api/v1/applylist', views.get_borrow_apply_list),
    path('api/v1/rentlist', views.get_borrow_list),
    path('api/v1/upgrade', views.upgrade_apply),
    path('api/v1/search)', views.search_equipment),

    # 提供者
    path('api/v2/equipmentlist', views.get_my_equipment_list),
    path('api/v2/edit', views.edit_equipment),
    path('api/v2/increase', views.increase_equipment),
    path('api/v2/decrease', views.decrease_equipment),
    path('api/v2/onshelf', views.on_shelf_equipment),
    path('api/v2/offshelf', views.off_shelf_equipment),
    path('api/v2/borrowapplylist', views.get_borrow_apply_list),
    path('api/v2/whether/agree', views.reply_borrow_apply),
    path('api/v2/searchrent', views.get_lend_list),
    path('api/v2/confirm', views.confirm_return),

]
