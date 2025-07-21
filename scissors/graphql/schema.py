import graphene
import graphql_jwt
from graphene_django.filter import DjangoFilterConnectionField

from black_scissors.core.base_admin_query import BaseAdminQuery
from black_scissors.core.base_query import BaseQuery
# from scissors.admin import DateTimeSlotsAdmin
from scissors.graphql.filters import CategoryFilterSet, ServiceFilterSet, StaffFilterSet, SlotFilterSet, \
    ServiceDetailFilterSet
from scissors.graphql.mutations import CategoryMutation, UpdateTimeSlotsMutation, SaveServiceDetailsMutation, \
    ObtainToken, CreatePostMutation
from scissors.graphql.types import CategoryType, ServiceType, StaffType, SlotType, AppointmentType, PostType
from scissors.models import Category, Service, Staff, DateTimeSlots, ServiceDetail, Posts


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

class PostQuery(BaseQuery):
    posts = DjangoFilterConnectionField(PostType)

    @classmethod
    def resolve_posts(cls, root, info, **kwargs):
        return Posts.objects.all()


class ScissorMutation(graphene.ObjectType):
    create_category = CategoryMutation.Field()
    update_status = UpdateTimeSlotsMutation.Field()
    book_appointment = SaveServiceDetailsMutation.Field()
    create_post = CreatePostMutation.Field()
    admin_login = ObtainToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

# admin

class AdminServiceDetailQuery(BaseAdminQuery):
    detail = DjangoFilterConnectionField(AppointmentType,filterset_class=ServiceDetailFilterSet, status=graphene.String())

    @classmethod
    def resolve_detail(cls, root, info, **kwargs):
        cls.handle_admin_query(info.context)
        if 'status' in kwargs:
            return ServiceDetail.objects.filter(date_range__status=kwargs['status'])
        return ServiceDetail.objects.all()

class ScissorsQuery(CategoryQuery, ServiceQuery, StaffQuery, DateTimeSoltQuery, PostQuery, AdminServiceDetailQuery):
    pass
