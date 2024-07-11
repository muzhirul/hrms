from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from hrms.utils import CustomResponse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from django.contrib.auth import authenticate
from hrms.pagination import CustomPagination
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from setup_app.models import Role,Permission,Menu
from staff.models import *
from setup_app.models import ContractType
from django.db.models import Q
from django.contrib.sites.shortcuts import get_current_site
from datetime import datetime
from django.db.models import Count
from django.db.models import F

# Create your views here.

class UserV4LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer4(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        SITE_PROTOCOL = 'http://'
        if request.is_secure():
            SITE_PROTOCOL = 'https://'
        current_site = get_current_site(request).domain
        if user is None:
            return Response({
                'code':401,
                'message': 'Invalid credentials',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        if not user.is_verified:
            return Response({
                'code':401,
                'message': 'Account is not verfied',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
            
        refresh = RefreshToken.for_user(user)
        user_serializer = LoginSerializer4(user)
        user_data = user_serializer.data
        user_data['user'] = {}

        if Staff.objects.filter(user=user_data['id']).exists():
            user_info = Staff.objects.get(user=user_data['id'])
            user_data['user']['first_name'] = user_info.first_name
            user_data['user']['last_name'] = user_info.last_name
            user_data['user']['username'] = user_info.staff_id
            if user_info.photo:
                user_data['user']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
            else:
                user_data['user']['image'] = None
            if user_info.role:
                user_data['user']['role'] = user_info.role.name
            else:
                user_data['user']['role'] = None
        
        # if Student.objects.filter(user=user_data['id']).exists():
        #     user_info = Student.objects.get(user=user_data['id'])
        #     user_data['user']['first_name'] = user_info.first_name
        #     user_data['user']['last_name'] = user_info.last_name
        #     user_data['user']['username'] = user_info.student_no
        #     if user_info.photo:
        #         user_data['user']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
        #     else:
        #         user_data['user']['image'] = None
        #     user_data['user']['role'] = 'Student'

        # elif Staff.objects.filter(user=user_data['id']).exists():
        #     user_info = Staff.objects.get(user=user_data['id'])
        #     user_data['user']['first_name'] = user_info.first_name
        #     user_data['user']['last_name'] = user_info.last_name
        #     user_data['user']['username'] = user_info.staff_id
        #     if user_info.photo:
        #         user_data['user']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
        #     else:
        #         user_data['user']['image'] = None
        #     user_data['user']['role'] = user_info.role.name

        # elif Guardian.objects.filter(user=user_data['id']).exists():
        #     user_info = Guardian.objects.get(user=user_data['id'])
        #     user_data['user']['first_name'] = user_info.first_name
        #     user_data['user']['last_name'] = user_info.last_name
        #     user_data['user']['username'] = user_info.guardian_no
        #     if user_info.photo:
        #         user_data['user']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
        #     else:
        #         user_data['user']['image'] = None
        #     user_data['user']['role'] = 'Guardian'
        
        menu_info = {}
        role_id = []
        user_data['menus'] = []
        for role in user.role.all():
            role_id.append((role.id))
        parent_id = []
        for parent in Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role__in=role_id,status=True).values_list('menu__parent', flat=True).distinct():
            if parent:
                parent_id.append(parent)
        main_menus = []
        parent_menus = Menu.objects.filter(id__in=parent_id,parent_id__isnull=True,status=True).order_by('sl_no')
        for parent_menu in parent_menus:
            main_menu = {}
            main_menu['id'] = parent_menu.id
            main_menu['name'] = parent_menu.name
            if parent_menu.icon:
                main_menu['icon'] = SITE_PROTOCOL+current_site + '/media/'+str(parent_menu.icon)
            else:
                main_menu['icon'] = ''
            main_menu['icon_text'] = parent_menu.icon_text
            main_menu['order'] = parent_menu.sl_no
            child_id = []
            permissions = Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role__in=role_id,menu__parent= parent_menu.id,status=True).values_list('menu__id', flat=True).distinct()
            for permission in permissions:
                child_id.append(permission)
            child_menus = Menu.objects.filter(id__in=child_id,parent_id__isnull=False,status=True).order_by('sl_no')
            main_menu['sub_menu'] = []
            menu_child = []
            
            for child_menu in child_menus:
                sub_memu = {}
                sub_memu['id'] = child_menu.id
                sub_memu['name'] = child_menu.name
                if child_menu.slug:
                    sub_memu['slug'] = '/'+parent_menu.slug+'/'+child_menu.slug
                sub_memu['order'] = child_menu.sl_no
                sub_memu['permission'] = []
                userPermission = []
                user_permissions = Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role__in=role_id,menu= child_menu.id,status=True)
                for user_permission in user_permissions:
                    if user_permission.can_create:
                        userPermission.append('create')
                    if user_permission.can_view:
                        userPermission.append('view')
                    if user_permission.can_update:
                        userPermission.append('update')
                    if user_permission.can_delete:
                        userPermission.append('delete')
                userPermission = set(userPermission)
                sub_memu['permission'] = userPermission
                menu_child.append(sub_memu)
            main_menu['sub_menu'] = menu_child
            main_menus.append(main_menu)
        user_data['menus'] = main_menus        
        user_data['token'] = {}
        user_data['token']['refresh'] = str(refresh)
        user_data['token']['access'] = str(refresh.access_token)
        
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':user_data},status=status.HTTP_200_OK)

class DashboardView(generics.ListAPIView):
    # Requires a valid JWT token for access
    permission_classes = [permissions.IsAuthenticated]
    def list(self, request, *args, **kwargs):
        dashboard_data = {}
        dashboard_data['basic_info'] = {}
        day_name = datetime.now().date().strftime('%A').lower()
        current_date = datetime.now().date()
        print(day_name)
        print(current_date)
        SITE_PROTOCOL = 'http://'
        if request.is_secure():
            SITE_PROTOCOL = 'https://'
        current_site = get_current_site(request).domain
        institution_id = self.request.user.institution
        branch_id = self.request.user.branch

        ''' For Staff user '''
       
        if Staff.objects.filter(user=self.request.user.id,institution=institution_id, branch=branch_id,status=True).exists():
            user_info = Staff.objects.get(user=self.request.user.id,status=True)
            dashboard_data['basic_info']['first_name'] = user_info.first_name
            dashboard_data['basic_info']['last_name'] = user_info.last_name
            dashboard_data['basic_info']['username'] = user_info.staff_id
            # dashboard_data['basic_info']['nid'] = user_info.nid
            dashboard_data['basic_info']['role'] = user_info.role.name
            dashboard_data['basic_info']['shift'] = user_info.shift.name
            if user_info.photo:
                dashboard_data['basic_info']['image'] = SITE_PROTOCOL+current_site + '/media/'+str(user_info.photo)
            else:
                dashboard_data['basic_info']['image'] = None

            dashboard_data['admin'] ={}
            total_admin = Staff.objects.filter(institution=institution_id, branch=branch_id,status=True,role__name__iexact='hr admin').count()
            dashboard_data['admin']['name'] = 'Total Admin'
            dashboard_data['admin']['count'] = total_admin

            dashboard_data['staff'] ={}
            total_staff = Staff.objects.filter(institution=institution_id, branch=branch_id,status=True).count()
            dashboard_data['staff']['name'] = 'Total Staff'
            dashboard_data['staff']['count'] = total_staff

            dashboard_data['department'] ={}
            total_dept = Department.objects.filter(institution=institution_id, branch=branch_id,status=True).count()
            dashboard_data['department']['name'] = 'Total Department'
            dashboard_data['department']['count'] = total_dept


            total_emp = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,attn_date=current_date).count()
            total_present = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,attn_date=current_date,attn_type__name__iexact='present').count()
            total_absent = ProcessAttendanceDaily.objects.filter(status=True,is_active=True,attn_date=current_date,attn_type__name__iexact='absent').count()
            dashboard_data['present'] = {}
            dashboard_data['present']['name']='Staff Present'
            dashboard_data['present']['count']=total_present
            dashboard_data['present']['total']=total_emp

            dashboard_data['absent'] = {}
            dashboard_data['absent']['name']='Staff Absent'
            dashboard_data['absent']['count']=total_absent
            dashboard_data['absent']['total']=total_emp

            dept_wise_emp = Department.objects.annotate(total_emp=Count('staff')).order_by('name')
            dashboard_data['dept_wise_emp'] = []  
            dept_wise_emps = []
            for department in dept_wise_emp:
                dept_wise_emp = {}
                dept_wise_emp['name'] = department.name
                dept_wise_emp['value'] = department.total_emp
                dept_wise_emps.append(dept_wise_emp)
            dashboard_data['dept_wise_emp'] = dept_wise_emps

            dashboard_data['staff_directory'] = []
           
            # emp_informations =  Staff.objects.select_related('staffpayroll').select_related('department').order_by('doj').values('first_name', 'last_name', 'doj', 'department__name', 'staffpayroll__contract_type')
            emp_informations = Staff.objects.select_related('department').order_by('doj').values('id','staff_id','first_name', 'last_name', 'doj', 'department__name',)
            # emp_informations = Staff.objects.filter(status=True).filter(department__status=True).filter(staffpayroll__status=True, staffpayroll__is_active=True).select_related('staffpayroll', 'department').values('first_name', 'last_name', 'doj', 'department__name','staffpayroll__contract_type').order_by('doj')
            # emp_informations = Staff.objects.filter(status=True).select_related('department','staffpayroll').values('first_name', 'last_name', 'doj', 'department__name','staffpayroll__remarks').order_by('doj')
            staff_directorys = []
            for staff in emp_informations:
                staff_directory = {}
                staff_pk = staff['id']
                payroll_count = StaffPayroll.objects.filter(status=True,is_active=True,staff=staff_pk).order_by('start_date').count()
                staff_directory['staff_id'] = staff['staff_id']
                staff_directory['first_name'] = staff['first_name']
                staff_directory['last_name'] = staff['last_name']
                staff_directory['joining_date'] = staff['doj']
                staff_directory['department'] = staff['department__name']
                if payroll_count > 0:
                    staff_status =StaffPayroll.objects.filter(status=True,is_active=True,staff=staff_pk).order_by('start_date').last()
                    staff_directory['type'] = staff_status.contract_type.name
                else:
                    staff_directory['type'] = None
                current_attn = ProcessAttendanceDaily.objects.filter(status=True,staff=staff_pk,attn_date=current_date).last()
                staff_directory['attn_status'] = current_attn.attn_type.name
                staff_directorys.append(staff_directory)
            dashboard_data['staff_directory'] = staff_directorys 

            # dashboard_data['notice_board'] = []   
            # notice_boards = []
            # for notice in NoticeBoard.objects.filter(status=True,is_active=True,institution=institution_id, branch=branch_id,notice_for=user_info.role).order_by('-notice_date'):
            #     notice_board = {}
            #     notice_board['title'] = notice.title
            #     notice_board['publish_date'] = notice.publish_date
            #     if notice.attachment:
            #         notice_board['file'] = SITE_PROTOCOL+current_site + '/media/'+str(notice.attachment)
            #     else:
            #         notice_board['file'] = None
            #     notice_boards.append(notice_board)
            # dashboard_data['notice_board'] = notice_boards
            # For Attendance List
            # dashboard_data['attendance_list'] = []
            # if ProcessAttendanceDaily.objects.filter(staff=user_info,status=True,is_active=True,institution=institution_id, branch=branch_id).exists():
            #     attn_lists = []
            #     for std_attn in ProcessAttendanceDaily.objects.filter(staff=user_info,status=True,is_active=True,institution=institution_id, branch=branch_id).order_by('-attn_date')[:30]:
            #         attn_list = {}
            #         if std_attn.in_time:
            #             in_time = (std_attn.in_time.time())
            #         else:
            #             in_time = None
            #         if std_attn.out_time:
            #             out_time = (std_attn.out_time.time())
            #         else:
            #             out_time = None
            #         attn_list['date'] = std_attn.attn_date
            #         attn_list['shift'] = std_attn.shift.name
            #         attn_list['in_time'] = in_time
            #         attn_list['out_time'] = out_time
            #         attn_list['status'] = std_attn.attn_type.name
            #         attn_lists.append(attn_list)
            #     dashboard_data['attendance_list'] = attn_lists
            # # For Student Leave Transaction
            # dashboard_data['leave_app_list'] = []
            # if StaffLeaveTransaction.objects.filter(apply_by=user_info,status=True,institution=institution_id, branch=branch_id).exists():
            #     leave_lists = []
            #     for leave_trns in StaffLeaveTransaction.objects.filter(apply_by=user_info,status=True,institution=institution_id, branch=branch_id).order_by('-start_date')[:30]:
            #         leave_list = {}
            #         leave_list['start_date'] = leave_trns.start_date
            #         leave_list['end_date'] = leave_trns.end_date
            #         leave_list['duration'] = leave_trns.day_count
            #         leave_list['leave_type'] = leave_trns.leave_type.name
            #         leave_list['reason'] = leave_trns.reason_for_leave
            #         if leave_trns.app_status:
            #             leave_list['status'] = leave_trns.app_status.title
            #         else:
            #             leave_list['status'] = None
            #         leave_lists.append(leave_list)
            #     dashboard_data['leave_app_list'] = leave_lists        
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':dashboard_data},status=status.HTTP_200_OK)


class UserV3LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer3(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is None:
            return Response({
                'code':401,
                'message': 'Invalid credentials',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        # if not user.is_active:
        #     raise forms.ValidationError('Account disabled, contact admin')
        if not user.is_verified:
            return Response({
                'code':401,
                'message': 'Account is not verfied',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
            
        refresh = RefreshToken.for_user(user)
        user_serializer = LoginSerializer3(user)
        user_data = user_serializer.data
        menu_info = {}
        for role in user.role.all():
            for parent in Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role=role).values_list('menu__parent', flat=True).distinct():
                parent_name = Menu.objects.get(id=parent,parent_id__isnull=True)
                app_name = parent_name.name
                if app_name not in menu_info:
                    menu_info[app_name] = {}
                for child in Permission.objects.filter(Q(can_create=True) | Q(can_view=True) | Q(can_update=True) | Q(can_delete=True), role=role, menu__parent= parent).distinct():
                    model_name = child.menu.name
                    menu_info[app_name][model_name] = []
        user_data['menus'] = menu_info        
        user_data['token'] = {}
        user_data['token']['refresh'] = str(refresh)
        user_data['token']['access'] = str(refresh.access_token)
        
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':user_data},status=status.HTTP_200_OK)

class UserV2LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer2(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )

        if user is None:
            return Response({
                'code':401,
                'message': 'Invalid credentials',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        # if not user.is_active:
        #     raise forms.ValidationError('Account disabled, contact admin')
        if not user.is_verified:
            return Response({
                'code':401,
                'message': 'Account is not verfied',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        user_serializer = LoginSerializer2(user)
        user_data = user_serializer.data
        
        permission_info = {}
        for group in user.groups.all():
            for content_type_id  in Permission.objects.filter(group=group).values_list('content_type_id', flat=True).distinct():
                content_type = ContentType.objects.get(id=content_type_id)
                app_label = content_type.app_label
                model_name = content_type.model
                if app_label not in permission_info:
                    permission_info[app_label] = {}
                permissions = Permission.objects.filter(content_type=content_type,group=group)
                permission_names = [permission.codename for permission in permissions]
                permission_info[app_label][model_name] = permission_names
        user_data['menus'] = permission_info
        user_data['token'] = {}
        user_data['token']['refresh'] = str(refresh)
        user_data['token']['access'] = str(refresh.access_token)
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':user_data},status=status.HTTP_200_OK)

class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        # if not user:
        #     raise forms.ValidationError('Invalid Credentials')
        # content_type = ContentType.objects.all()
        # print(content_type)
        if user is None:
            return Response({
                'code':401,
                'message': 'Invalid credentials',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        # if not user.is_active:
        #     raise forms.ValidationError('Account disabled, contact admin')
        if not user.is_verified:
            return Response({
                'code':401,
                'message': 'Account is not verfied',
                'error':[],
                'data': None
                }, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        user_serializer = LoginSerializer(user)
        user_data = user_serializer.data
        
        """
        group_data = []
        # Include detailed permission data for each group
        group_data = []
        for group in user.groups.all():
            group_permissions = Permission.objects.filter(group=group)
            group_data.append({
                'name': group.name,
                'permissions': [
                    {
                        'id': permission.id,
                        'name': permission.name,
                        'codename': permission.codename,
                    }
                    for permission in group_permissions
                ]
            })

        user_data['groups'] = group_data
        """
        user_data['token'] = {}
        user_data['token']['refresh'] = str(refresh)
        user_data['token']['access'] = str(refresh.access_token)
        return Response({
            'code':200,
            'message':'Success',
            'error':[],
            'data':user_data},status=status.HTTP_200_OK)
    
