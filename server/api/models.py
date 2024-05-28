from django.db import models


class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)


class Workplace(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, default=' ')
    type = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)


class Employee(models.Model):
    telegram_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)


class Client(models.Model):
    telegram_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)


class Nomenclature(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()


class Service(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    serviceType = models.CharField(max_length=100)
    payment = models.CharField(max_length=100, blank=True, null=True)
    warranty = models.BooleanField(blank=True, null=True)
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)


class FirstClientCheck(models.Model):
    telegram_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    source = models.CharField(max_length=100)
    comment = models.CharField(max_length=1000, blank=True, null=True)
    datetime_started = models.DateTimeField()
    datetime_finished = models.DateTimeField(auto_now_add=True)


class CustomerLoyaltyIndex(models.Model):
    telegram_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    answer1 = models.IntegerField()
    answer2 = models.IntegerField()
    answer3 = models.IntegerField()
    datetime_sended = models.DateTimeField()
    datetime_started = models.DateTimeField()
    datetime_finished = models.DateTimeField(auto_now_add=True)


class CustomerShopFeedback(models.Model):
    telegram_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    answer1 = models.IntegerField(null=True, blank=True)
    answer2 = models.IntegerField(null=True, blank=True)
    answer3 = models.IntegerField(null=True, blank=True)
    answer4 = models.IntegerField(null=True, blank=True)
    answer5 = models.CharField(max_length=1000, null=True, blank=True)
    answer6 = models.IntegerField(null=True, blank=True)
    answer7 = models.IntegerField(null=True, blank=True)
    answer8 = models.IntegerField(null=True, blank=True)
    answer9 = models.IntegerField(null=True, blank=True)
    answer10 = models.IntegerField(null=True, blank=True)
    answer11 = models.CharField(max_length=1000, null=True, blank=True)
    datetime_sended = models.DateTimeField()
    datetime_started = models.DateTimeField()
    datetime_finished = models.DateTimeField(auto_now_add=True)


class ProductFeedback(models.Model):
    telegram_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    answer1 = models.IntegerField(null=True, blank=True)
    answer2 = models.CharField(max_length=1000, null=True, blank=True)
    datetime_sended = models.DateTimeField()
    datetime_started = models.DateTimeField()
    datetime_finished = models.DateTimeField(auto_now_add=True)


class RefundFeedback(models.Model):
    telegram_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    answer1 = models.CharField(max_length=1000, null=True, blank=True)
    answer2 = models.CharField(max_length=1000, null=True, blank=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    datetime_sended = models.DateTimeField()
    datetime_started = models.DateTimeField()
    datetime_finished = models.DateTimeField(auto_now_add=True)


class RepairFeedback(models.Model):
    telegram_id = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    answer1 = models.IntegerField(null=True, blank=True)
    answer2 = models.IntegerField(null=True, blank=True)
    answer3 = models.IntegerField(null=True, blank=True)
    answer4 = models.IntegerField(null=True, blank=True)
    answer5 = models.CharField(max_length=1000, null=True, blank=True)
    datetime_sended = models.DateTimeField()
    datetime_started = models.DateTimeField()
    datetime_finished = models.DateTimeField(auto_now_add=True)


class Schedule(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True, blank=True)
    poll_type = models.CharField(max_length=100)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_to_send = models.DateTimeField()
    is_sent = models.BooleanField()
