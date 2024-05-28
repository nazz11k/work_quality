from rest_framework import generics
from django.utils.timezone import now, timedelta

from .models import *
from .serializers import *


class EmployeeViewSet(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetailViewSet(generics.RetrieveUpdateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'telegram_id'


class ClientViewSet(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset = Client.objects.all()
        phone = self.request.query_params.get('phone', None)
        if phone is not None:
            queryset = queryset.filter(phone=phone)
        return queryset

    def perform_create(self, serializer):
        data = self.request.data
        schedule = Schedule()
        schedule.poll_type = 'first_poll'
        schedule.client = serializer.save()
        schedule.is_sent = False
        schedule.datetime_to_send = now() + timedelta(seconds=120)
        schedule.save()



class ClientDetailViewSet(generics.RetrieveUpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'telegram_id'


class FirstClientCheckViewSet(generics.ListCreateAPIView):
    queryset = FirstClientCheck.objects.all()
    serializer_class = FirstClientCheckSerializer


class CustomerLoyaltyIndexViewSet(generics.ListCreateAPIView):
    queryset = CustomerLoyaltyIndex.objects.all()
    serializer_class = CustomerLoyaltyIndexSerializer


class CustomerShopFeedbackViewSet(generics.ListCreateAPIView):
    queryset = CustomerShopFeedback.objects.all()
    serializer_class = CustomerShopFeedbackSerializer


class ServiceViewSet(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.all()
        client = self.request.query_params.get('client', None)
        if client is not None:
            queryset = queryset.filter(client=client)
        return queryset

    def perform_create(self, serializer):
        self.request.data._mutable = True
        data = self.request.data
        if data.get('time_gap1', None) is not None:
            time_gap1 = int(data.get('time_gap1', None))
            self.request.data.pop('time_gap1', None)
        if data.get('time_gap2', None) is not None:
            time_gap2 = int(data.get('time_gap2', None))
            self.request.data.pop('time_gap2', None)
        service = serializer.save()
        if service.serviceType == 'Покупка' or service.serviceType == 'Покупка(франшиза)':
            schedule1 = Schedule()
            schedule1.poll_type = 'shop_poll'
            schedule1.client = service.client
            schedule1.service = service
            schedule1.datetime_to_send = now() + timedelta(seconds=time_gap1)
            schedule1.is_sent = False
            schedule1.save()
            schedule2 = Schedule()
            schedule2.poll_type = 'product_poll'
            schedule2.client = service.client
            schedule2.service = service
            schedule2.datetime_to_send = now() + timedelta(seconds=time_gap2)
            schedule2.is_sent = False
            schedule2.save()
        elif service.serviceType == 'Повернення':
            schedule = Schedule()
            schedule.poll_type = 'refund_poll'
            schedule.client = service.client
            schedule.service = service
            schedule.datetime_to_send = now() + timedelta(seconds=time_gap1)
            schedule.is_sent = False
            schedule.save()
        elif service.serviceType == 'Ремонт':
            schedule = Schedule()
            schedule.poll_type = 'repair_poll'
            schedule.client = service.client
            schedule.service = service
            schedule.datetime_to_send = now() + timedelta(seconds=time_gap1)
            schedule.is_sent = False
            schedule.save()


class ServiceDetailViewSet(generics.RetrieveUpdateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'


class ProductFeedbackViewSet(generics.ListCreateAPIView):
    queryset = ProductFeedback.objects.all()
    serializer_class = ProductFeedbackSerializer


class RefundFeedbackViewSet(generics.ListCreateAPIView):
    queryset = RefundFeedback.objects.all()
    serializer_class = RefundFeedbackSerializer


class RepairFeedbackViewSet(generics.ListCreateAPIView):
    queryset = RepairFeedback.objects.all()
    serializer_class = RepairFeedbackSerializer


class CityViewSet(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = City.objects.all()
        region_id = self.request.query_params.get('region', None)
        name = self.request.query_params.get('name', None)
        name = name.replace('_', ' ') if name is not None else None
        if region_id is not None:
            queryset = queryset.filter(region_id=region_id)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


class CityDetailViewSetById(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'id'


class CityDetailViewSetByName(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    lookup_field = 'name'


class RegionViewSet(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class RegionDetailViewSetById(generics.RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    lookup_field = 'id'


class RegionDetailViewSetByName(generics.RetrieveAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    lookup_field = 'name'


class ScheduleViewSet(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def get_queryset(self):
        queryset = Schedule.objects.all()
        queryset = queryset.filter(is_sent=False)
        queryset = queryset.filter(datetime_to_send__lt=now())
        for schedule in queryset:
            schedule.is_sent = True
            schedule.save()
        return queryset


class RegionsWithWorkplacesViewSet(generics.ListAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

    def get_queryset(self):
        queryset = Region.objects.all()
        workplaces = Workplace.objects.all()
        workplaces_cities = [workplace.city for workplace in workplaces]
        workplaces_cities = list(set(workplaces_cities))
        cities_regions = [city.region for city in workplaces_cities]
        cities_regions = list(set(cities_regions))
        queryset = queryset.filter(id__in=[region.id for region in cities_regions])
        return queryset


class CitiesWithWorkplacesViewSet(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer

    def get_queryset(self):
        queryset = City.objects.all()
        workplaces = Workplace.objects.all()
        workplaces_cities = [workplace.city for workplace in workplaces]
        workplaces_cities = list(set(workplaces_cities))
        queryset = queryset.filter(id__in=[city.id for city in workplaces_cities])

        region = self.request.query_params.get('region', None)
        if region is not None:
            queryset = queryset.filter(region=region)
        return queryset


class WorkplaceViewSet(generics.ListCreateAPIView):
    queryset = Workplace.objects.all()
    serializer_class = WorkplaceSerializer

    def get_queryset(self):
        queryset = Workplace.objects.all()
        city = self.request.query_params.get('city', None)
        if city is not None:
            queryset = queryset.filter(city=city)
        return queryset


class NomenclatureViewSet(generics.ListCreateAPIView):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer

    def get_queryset(self):
        queryset = Nomenclature.objects.all()
        name = self.request.query_params.get('name', None)
        name_part = self.request.query_params.get('name_part', None)
        if name_part is not None:
            queryset = queryset.filter(name__icontains=name_part)
        if name is not None:
            queryset = queryset.filter(name=name)
        return queryset


class NomenclatureDetailViewSet(generics.RetrieveUpdateAPIView):
    queryset = Nomenclature.objects.all()
    serializer_class = NomenclatureSerializer
    lookup_field = 'id'


class MonthlyPollCreateViewSet(generics.ListAPIView):
    serializer_class = ScheduleSerializer
    queryset = Schedule.objects.all()

    def get_queryset(self):
        clients = Client.objects.all()
        for client in clients:
            schedule = Schedule()
            schedule.poll_type = 'monthly_poll'
            schedule.client = client
            schedule.is_sent = False
            schedule.datetime_to_send = now() + timedelta(seconds=120)
            schedule.save()
        return Schedule.objects.all()
