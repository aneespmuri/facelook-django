from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

# Create your models here.

class TblUser(AbstractUser, PermissionsMixin):
    token_version = models.IntegerField(default=0)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'tbl_user'

class Category(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField()
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'services'

    def __str__(self):
        return self.name

class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='staff_profiles/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'staffs'

    def __str__(self):
        return self.name

class Customers(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class DateTimeSlots(models.Model):
    FREE = 'free'
    ONHOLD = 'onhold'
    BOOKED = 'booked'
    choice_fields = (
        (FREE, 'Free'),
        (ONHOLD, 'On Hold'),
        (BOOKED, 'Booked'),
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=10, choices=choice_fields, default=FREE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'datetime_slots'

    def __str__(self):
        return f"{self.date}\n({self.start_time}-{self.end_time})"

class ServiceDetail(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE, null=True)
    date_range = models.ForeignKey(DateTimeSlots, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'service_detail'