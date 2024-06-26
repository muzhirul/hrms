from rest_framework import serializers
from .models import *
from setup_app.serializers import *


class AccountBankSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    institution_name = serializers.ReadOnlyField(source='institution.name')
    branch_name = serializers.ReadOnlyField(source='branch.name')
    class Meta:
        model = AccountBank
        # Exclude the 'status' field and other fields you want to exclude
        exclude = ['status']
        # exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class AccountBankViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountBank
        # Exclude the 'status' field and other fields you want to exclude
        fields = ['id','name']
        # exclude = ['created_by', 'updated_by', 'created_at', 'updated_at']

class HolidaySerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = Holiday
        exclude = ['status']

class HolidayViewSerializer(serializers.ModelSerializer):
    type = HolidayTypeViewSerializer(read_only=True)
    
    class Meta:
        model = Holiday
        exclude = ['status','institution','branch','created_by','updated_by','created_at','updated_at']

class LeaveTypeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveType
        exclude = ['status','institution','branch']

class LeaveTypeListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = LeaveType
        fields = ['id','leave_type_code','name']

class LeaveTypeViewSerializer(serializers.ModelSerializer):
    created_username = serializers.ReadOnlyField(source='created_by.username')
    updated_username = serializers.ReadOnlyField(source='created_by.username')
    
    class Meta:
        model = LeaveType
        exclude = ['status','institution','branch']

class LeaveTypeView2Serializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = ['id','leave_type_code','name']
        # exclude = ['status','institution','branch']