import django_filters

from scissors.models import Category, Service, Staff, DateTimeSlots


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
    class Meta:
        model = DateTimeSlots
        fields = {
            'id': ['exact'], }