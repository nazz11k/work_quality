from rest_framework import serializers
from .models import *
from datetime import datetime


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        lookup_field = 'telegram_id'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        lookup_field = 'telegram_id'


class FirstClientCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstClientCheck
        fields = '__all__'


class CustomerLoyaltyIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerLoyaltyIndex
        fields = '__all__'


class CustomerShopFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerShopFeedback
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        lookup_field = 'id'


class ProductFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeedback
        fields = '__all__'


class RefundFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundFeedback
        fields = '__all__'


class RepairFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairFeedback
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
        lookup_field = 'id'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
        lookup_field = 'id'


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = '__all__'
        lookup_field = 'id'


class WorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = '__all__'
        lookup_field = 'id'


class NomenclatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nomenclature
        fields = '__all__'
        lookup_field = 'id'