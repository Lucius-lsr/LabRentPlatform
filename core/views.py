from django.shortcuts import render

from .models import User, BorrowApply, OnShelfApply, UpgradeApply, Equipment
from django.http import HttpResponse
import json
# Create your views here.

'''------------normal user-------------'''


def register(request):
    pass


def login(request):
    pass


def logout(request):
    pass


def show_equipment(request):
    pass


def borrow_apply(request):
    pass


def get_borrow_apply_list(request):
    pass


def get_borrow_list(request):
    pass


def upgrade_apply(request):
    pass


def search_equipment(request):
    if request.method == 'GET':
        equipment_list = []
        username = request.GET.get('username', "")
        equipment_name = request.GET.get('name', "")
        if username:
            user = User.objects.get(username=username)
            equipment_list = user.equipments.all()
        elif equipment_name:
            equipment_list = Equipment.objects.filter(name__contains=equipment_name)
        equipment_list = [e.to_dict() for e in equipment_list]
        return HttpResponse(json.dumps(equipment_list), content_type="json")


'''------------provider user-------------'''


def edit_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        name = request.POST.get('name')
        description = request.POST.get('description')
        count = request.POST.get('count')

        custom_equipment = Equipment.objects.get(id=equipment_id)
        custom_equipment.name = name
        custom_equipment.name = description
        custom_equipment.name = count
        custom_equipment.save()
        return HttpResponse(json.dumps({
            'message': 'ok'
        }), content_type="json")


def add_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        add_count = request.POST.get('addcount', 1)
        custom_equipment = Equipment.objects.get(id=equipment_id)
        custom_equipment.count += add_count
        custom_equipment.save()
        return HttpResponse(json.dumps({
            'message': 'ok'
        }), content_type="json")


def delete_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        delete_count = request.POST.get('deletecount', 1)
        custom_equipment = Equipment.objects.get(id=equipment_id)
        custom_equipment.count -= delete_count
        custom_equipment.save()
        return HttpResponse(json.dumps({
            'message': 'ok'
        }), content_type="json")


def on_shelf_equipment(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        count = request.POST.get('count')
        Equipment(
            name=name,
            description=description,
            count=count
        ).save()
        return HttpResponse(json.dumps({
            'message': 'ok'
        }), content_type="json")


def off_shelf_equipment(request):
    if request.method == 'POST':
        equipment_id = request.POST.get('id')
        Equipment.objects.get(id=equipment_id).delete()
        return HttpResponse(json.dumps({
            'message': 'ok'
        }), content_type="json")


def show_borrow_apply_list(request):
    pass


def reply_borrow_apply(request):
    pass


def get_lend_list(request):
    pass


def confirm_return(request):
    pass
