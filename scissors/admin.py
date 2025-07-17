from datetime import timedelta

from django import forms
from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME, AdminForm
from django.db import models
from django.forms import TimeInput
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse

from scissors.forms import BulkCreateSlotsForm
from scissors.models import Category, Customers, Service, Staff, DateTimeSlots, ServiceDetail

# Register your models here.
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Staff)


# admin.site.register(ServiceDetail)

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'email', 'phone_no', 'notes']

    def get_name(self, obj):
        return obj

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(DateTimeSlots)
class DateTimeSlotsAdmin(admin.ModelAdmin):
    list_display = ['date', 'start_time', 'end_time', 'status']

    def has_add_permission(self, request):
        return False

    formfield_overrides = {
        models.TimeField: {
            'widget': TimeInput(format='%I:%M %p', attrs={'placeholder': '04:00 PM', 'class': 'vTimeField'}),
            'input_formats': ['%I:%M %p'],
        },
    }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                'bulk-create/',
                self.admin_site.admin_view(self.bulk_create_view),
                name='datetimeslots_bulk_create'
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['bulk_create_url'] = reverse('admin:datetimeslots_bulk_create')
        return super().changelist_view(request, extra_context=extra_context)

    def bulk_create_view(self, request):
        context = self.admin_site.each_context(request)

        if request.method == 'POST':
            form = BulkCreateSlotsForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                start_time = form.cleaned_data['start_time'].replace(second=0, microsecond=0)
                end_time = form.cleaned_data['end_time'].replace(second=0, microsecond=0)
                status = form.cleaned_data['status']

                delta = (end_date - start_date).days + 1
                slots = [
                    DateTimeSlots(
                        date=start_date + timedelta(days=i),
                        start_time=start_time.replace(second=0, microsecond=0),
                        end_time=end_time.replace(second=0, microsecond=0),
                        status=status
                    )
                    for i in range(delta)
                    if not DateTimeSlots.objects.filter(
                        date=start_date + timedelta(days=i),
                        start_time=start_time.replace(second=0, microsecond=0),
                        end_time=end_time.replace(second=0, microsecond=0)
                    ).exists()
                ]
                if len(slots) > 0:
                    DateTimeSlots.objects.bulk_create(slots)
                    self.message_user(request, f"✅ Created {len(slots)} new slots.")
                else:
                    self.message_user(request,
                                      f"⚠ No new slots were created. Same slot exist with {start_date.strftime('%B %d, %Y')} .",
                                      level='warning')
                return redirect('..')
        else:
            form = BulkCreateSlotsForm()

        admin_form = AdminForm(
            form,
            fieldsets=[(None, {'fields': list(form.fields)})],
            prepopulated_fields={}
        )

        context.update({
            'title': 'Bulk Create DateTime Slots',
            'adminform': admin_form,
            'form': form,
            'add': True,  # Important for 'Save' button display
            'change': False,
            'is_popup': False,
            'save_as': False,
            'has_view_permission': True,
            'has_add_permission': True,
            'has_change_permission': True,
            'has_delete_permission': False,
            'opts': self.model._meta,
            'original': None,
            'media': form.media,
            'has_editable_inline_admin_formsets': False,
        })

        return TemplateResponse(request, 'admin/change_form.html', context)


@admin.register(ServiceDetail)
class ServiceDetailAdmin(admin.ModelAdmin):
    list_display = ['get_category', 'get_service', 'get_customer', 'get_staff', 'get_date_time', 'get_status']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_service(self, obj):
        return obj.service

    def get_category(self, obj):
        return obj.category

    def get_customer(self, obj):
        return obj.customer

    def get_staff(self, obj):
        return obj.staff

    def get_date_time(self, obj):
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
