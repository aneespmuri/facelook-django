from django import forms
from django.contrib import admin
from django.forms import TimeInput

from scissors.models import Category, Customers, Service, Staff, DateTimeSlots

# Register your models here.
admin.site.register(Category)
admin.site.register(Customers)
admin.site.register(Service)
admin.site.register(Staff)


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
