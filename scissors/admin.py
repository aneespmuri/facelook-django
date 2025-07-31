import csv
from datetime import timedelta, datetime

from django import forms
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.helpers import AdminForm
from django.contrib.admin.views.main import ChangeList
from django.db import models
from django.db.models import DateField
from django.db.models.functions import Cast
from django.forms import TimeInput
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

from scissors.forms import BulkCreateSlotsForm
from scissors.models import Category, Customers, Service, Staff, DateTimeSlots, ServiceDetail

# Register your models here.
admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Staff)

# Filters

class SpecificDateFilter(SimpleListFilter):
    title = 'Specific Date'
    parameter_name = 'specific_date'

    def lookups(self, request, model_admin):
        return [('dummy', 'dummy')]

    def choices(self, changelist):
        yield {
            'selected': not self.value(),
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
            'display': 'All',
        }

    def queryset(self, request, queryset):
        date_str = request.GET.get(self.parameter_name)

        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                return queryset.annotate(
                    date_only=Cast('date_range__date', output_field=DateField())
                ).filter(date_only=date)
            except ValueError:
                return queryset.none()
        return queryset

class SpecificDateSlotFilter(SimpleListFilter):
    title = 'Specific Date'
    parameter_name = 'specific_date'

    def lookups(self, request, model_admin):
        return [('dummy', 'dummy')]

    def choices(self, changelist):
        yield {
            'selected': not self.value(),
            'query_string': changelist.get_query_string(remove=[self.parameter_name]),
            'display': 'All',
        }

    def queryset(self, request, queryset):
        date_str = request.GET.get(self.parameter_name)

        if date_str:
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d').date()
                return queryset.filter(date=date)
            except ValueError:
                return queryset.none()
        return queryset

class StaffFilter(SimpleListFilter):
    title = 'Staff'
    parameter_name = 'staff'

    def lookups(self, request, model_admin):
        return [(staff.id, staff.name) for staff in Staff.objects.all()]

    def queryset(self, request, queryset):
        staff_id = self.value()
        if staff_id:
            return queryset.filter(staff__id=staff_id)
        return queryset
# admin.site.register(ServiceDetail)

@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'email', 'phone_no', 'notes']

    def get_name(self, obj):
        return obj

    def has_change_permission(self, request, obj=None):
        return False

    list_per_page = 20

@admin.register(DateTimeSlots)
class DateTimeSlotsAdmin(admin.ModelAdmin):
    list_display = ['date', 'formatted_start_time', 'formatted_end_time', 'status', 'staff', 'appointment_status']
    list_editable = ['appointment_status']

    class Media:
        js = ('js/admin_date.js',)

    def has_add_permission(self, request):
        return False

    def formatted_start_time(self, obj):
        return obj.start_time.strftime('%I:%M %p')

    def get_full_queryset(self, request):
        modeladmin = self
        cl = ChangeList(
            request, modeladmin.model, modeladmin.list_display,
            modeladmin.list_display_links, modeladmin.list_filter,
            modeladmin.date_hierarchy, modeladmin.search_fields,
            modeladmin.list_select_related, modeladmin.list_per_page,
            modeladmin.list_max_show_all, modeladmin.list_editable,
            modeladmin
        )
        return cl.get_queryset(request)

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = ['date', 'start_time', 'end_time', 'status', 'staff', 'appointment_status']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={meta.model_name}_export.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([
                obj.date,
                obj.start_time.strftime('%I:%M %p'),
                obj.end_time.strftime('%I:%M %p'),
                obj.status,
                obj.staff,
                obj.appointment_status
            ])

        return response

    def export_as_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{self.model._meta.model_name}_export.pdf"'

        doc = SimpleDocTemplate(response, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        elements.append(Paragraph(f"{self.model._meta.verbose_name_plural.title()} Report", styles['Title']))
        elements.append(Spacer(1, 12))

        # Table header
        data = [['Date', 'Start Time', 'End Time', 'Status', 'Staff', 'Appointment Status']]

        # Table rows
        for obj in queryset:
            data.append([
                obj.date.strftime('%Y-%m-%d'),
                obj.start_time.strftime('%I:%M %p'),
                obj.end_time.strftime('%I:%M %p'),
                str(obj.status),
                str(obj.staff),
                str(obj.appointment_status)
            ])

        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))

        elements.append(table)
        doc.build(elements)
        return response

    export_as_csv.short_description = "Export Selected as CSV"
    export_as_pdf.short_description = "Export Selected as PDF"

    formatted_start_time.short_description = 'Start Time'

    def formatted_end_time(self, obj):
        return obj.end_time.strftime('%I:%M %p')

    formatted_end_time.short_description = 'End Time'


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

    def get_queryset(self, request):
        return DateTimeSlots.objects.all().order_by('-created_at')

    def bulk_create_view(self, request):
        context = self.admin_site.each_context(request)

        if request.method == 'POST':
            form = BulkCreateSlotsForm(request.POST)
            if form.is_valid():
                staff = form.cleaned_data['staff']
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']
                start_time = form.cleaned_data['start_time'].replace(second=0, microsecond=0)
                end_time = form.cleaned_data['end_time'].replace(second=0, microsecond=0)
                status = form.cleaned_data['status']
                appointment_status = form.cleaned_data['appointment_status']

                delta_days = (end_date - start_date).days + 1
                slots = []

                for day_offset in range(delta_days):
                    current_date = start_date + timedelta(days=day_offset)

                    current_slot_start = datetime.combine(current_date, start_time)
                    slot_end_datetime = datetime.combine(current_date, end_time)

                    while current_slot_start < slot_end_datetime:
                        current_slot_end = current_slot_start + timedelta(minutes=30)

                        if not DateTimeSlots.objects.filter(
                                staff=staff,
                                date=current_date,
                                start_time=current_slot_start.time(),
                                end_time=current_slot_end.time()
                        ).exists():
                            slots.append(
                                DateTimeSlots(
                                    staff=staff,
                                    date=current_date,
                                    start_time=current_slot_start.time(),
                                    end_time=current_slot_end.time(),
                                    status=status,
                                    appointment_status=appointment_status,
                                )
                            )

                        current_slot_start = current_slot_end

                if slots:
                    DateTimeSlots.objects.bulk_create(slots)
                    self.message_user(request, f"✅ Created {len(slots)} new slots.")
                else:
                    self.message_user(request, "⚠ No new slots were created. All time slots already exist.",
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
            'add': True,
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

    def save_model(self, request, obj, form, change):
        if 'appointment_status' in form.changed_data and obj.appointment_status == 'cancelled':
            obj.status = 'free'
        super().save_model(request, obj, form, change)

    list_filter = (StaffFilter, SpecificDateSlotFilter)
    list_per_page = 20
    actions = ['export_as_csv', 'export_as_pdf']


@admin.register(ServiceDetail)
class ServiceDetailAdmin(admin.ModelAdmin):

    class Media:
        js = ('js/admin_date.js',)
    list_display = ['get_category', 'get_service', 'get_customer', 'get_staff', 'get_date_time', 'get_status','get_appointment_status']

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False

    def get_service(self, obj):
        return obj.service

    def get_appointment_status(self, obj):
        return obj.date_range.appointment_status

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
    get_appointment_status.short_description = 'Appointment Status'

    search_fields = ['service__name', 'customer__first_name']

    list_filter = (StaffFilter, SpecificDateFilter)
    list_per_page = 20
