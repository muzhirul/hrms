from setup_app.models import *
from authentication.models import Authentication

def check_permission(user, menu_name, permission_type='view'):
    user = Authentication.objects.get(id=user)
    role_id = []
    for role in user.role.filter(status=True):
        role_id.append((role.id))
    menu_ids = []
    for menus in Menu.objects.filter(name=menu_name,status=True):
        menu_ids.append((menus.id))
    if permission_type == 'view':
        menu_permissions = Permission.objects.filter(role__in=role_id,menu__in=menu_ids,status=True,can_view=True)
    elif permission_type == 'create':
        menu_permissions = Permission.objects.filter(role__in=role_id,menu__in=menu_ids,status=True,can_create=True)
    elif permission_type == 'update':
        menu_permissions = Permission.objects.filter(role__in=role_id,menu__in=menu_ids,status=True,can_update=True)
    elif permission_type == 'delete':
        menu_permissions = Permission.objects.filter(role__in=role_id,menu__in=menu_ids,status=True,can_delete=True)
    if menu_permissions:
        return True
    return False

def generate_code(institution, branch, c_type):
    from datetime import datetime
    counter = SystemCounter.objects.get(institution=institution, branch=branch, code=c_type)
    prefix = counter.prefix or ""
    next_number = counter.next_number
    separator = counter.separator or ""
    if counter.counter_width:
        total_code_width = counter.counter_width
        fixed_width = len(prefix) + len(counter.separator or "")
        number_width = total_code_width - fixed_width
        number_str = str(next_number).zfill(number_width)
    else:
        number_str = str(next_number)
    
    final_code = f"{prefix}{separator}{number_str}"

    new_next_number = counter.next_number + counter.step

    counter.next_number = new_next_number
    counter.save()

    return final_code