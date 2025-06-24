import graphene
from graphene_django.filter import DjangoFilterConnectionField

from black_scissors.core.base_query import BaseQuery
from scissors.admin import DateTimeSlotsAdmin
from scissors.graphql.filters import CategoryFilterSet, ServiceFilterSet, StaffFilterSet, SlotFilterSet
from scissors.graphql.mutations import CategoryMutation, UpdateTimeSlotsMutation, SaveServiceDetailsMutation
from scissors.graphql.types import CategoryType, ServiceType, StaffType, SlotType
from scissors.models import Category, Service, Staff, DateTimeSlots


class CategoryQuery(BaseQuery):
    categories = DjangoFilterConnectionField(CategoryType, filterset_class=CategoryFilterSet)

    @classmethod
    def resolve_categories(cls, root, info, **kwargs):
        return Category.objects.all()

class ServiceQuery(BaseQuery):
    services = DjangoFilterConnectionField(ServiceType, filterset_class=ServiceFilterSet, category_id=graphene.String())

    @classmethod
    def resolve_services(cls, root, info, **kwargs):
        return Service.objects.filter(category_id=cls.get_id(kwargs['category_id']))

class StaffQuery(BaseQuery):
    staff = DjangoFilterConnectionField(StaffType, filterset_class=StaffFilterSet)

    @classmethod
    def resolve_staff(cls, root, info, **kwargs):
        return Staff.objects.all()

class DateTimeSoltQuery(BaseQuery):
    slots = DjangoFilterConnectionField(SlotType, filterset_class=SlotFilterSet, date =graphene.Date())

    @classmethod
    def resolve_slots(cls, root, info, **kwargs):
        if 'date' in kwargs:
            return DateTimeSlots.objects.filter(date=kwargs['date'])
        return DateTimeSlots.objects.all()

class ScissorsQuery(CategoryQuery, ServiceQuery, StaffQuery, DateTimeSoltQuery):
    pass

class ScissorMutation(graphene.ObjectType):
    create_category = CategoryMutation.Field()
    update_status = UpdateTimeSlotsMutation.Field()
    book_appointment = SaveServiceDetailsMutation.Field()