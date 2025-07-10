from django import forms
from django.contrib import admin
from django.forms import TimeInput

from scissors.models import Category, Customers, Service, Staff, DateTimeSlots, ServiceDetail

# Register your models here.
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Staff)
# admin.site.register(ServiceDetail)

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ['get_name','email','phone_no','notes']

    def get_name(self, obj):
        return obj
    def has_change_permission(self, request, obj=None):
        return False

class DateTimeSlotsForm(forms.ModelForm):
    class Meta:
        model = DateTimeSlots
        fields = '__all__'
        widgets = {
            'start_time': TimeInput(format='%I:%M %p'),
            'end_time': TimeInput(format='%I:%M %p'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ['%I:%M %p']
        self.fields['end_time'].input_formats = ['%I:%M %p']

@admin.register(DateTimeSlots)
class DateTimeSlotsAdmin(admin.ModelAdmin):
    form = DateTimeSlotsForm
    list_display = ['date', 'start_time', 'end_time', 'status']

@admin.register(ServiceDetail)
class ServiceDetailAdmin(admin.ModelAdmin):
    list_display = ['get_category','get_service','get_customer','get_staff','get_date_time', 'get_status']
    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_service(self, obj):
        return obj.service

    def get_category(self, obj):
        return obj.category

    def get_customer(self,obj):
        return obj.customer

    def get_staff(self,obj):
        return obj.staff

    def get_date_time(self,obj):
        return obj.date_range

    def get_status(self, obj):
        return obj.date_range.status

    get_service.short_description = 'Service'
    get_category.short_description = 'Category'
    get_customer.short_description = 'Customer'
    get_staff.short_description = 'Staff'
    get_date_time.short_description = 'Slot'
    get_status.short_description = 'Status'

    search_fields = ['service__name', 'customer__first_name']
