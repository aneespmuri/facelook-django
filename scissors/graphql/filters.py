import django_filters

from scissors.models import Category, Service, Staff, DateTimeSlots, ServiceDetail


class CategoryFilterSet(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            'id': ['exact'], }


class ServiceFilterSet(django_filters.FilterSet):
    class Meta:
        model = Service
        fields = {
            'id': ['exact'], }


class StaffFilterSet(django_filters.FilterSet):
    class Meta:
        model = Staff
        fields = {
            'id': ['exact'], }


class SlotFilterSet(django_filters.FilterSet):
    slot_id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')

    class Meta:
        model = DateTimeSlots
        fields = []


class ServiceDetailFilterSet(django_filters.FilterSet):
    class Meta:
        model = ServiceDetail
        fields = {
            'id': ['exact'], }
