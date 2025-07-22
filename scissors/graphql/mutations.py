from datetime import datetime
from pyexpat.errors import messages

import graphene
import graphql_jwt
from graphene import relay
from graphql import GraphQLError

from black_scissors.core.base_admin_mutation import BaseAdminMutation
from black_scissors.core.base_mutation import BaseMutation
from scissors.admin import DateTimeSlotsAdmin
from scissors.graphql.input import DetailInput
from scissors.graphql.types import CategoryType, SlotType, AppointmentType, UserType, PostType
from scissors.models import DateTimeSlots, Customers, ServiceDetail, Posts


class CategoryMutation(relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)

    message = graphene.String()
    category = graphene.Field(CategoryType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        return cls(message=input.get('name'))


class UpdateTimeSlotsMutation(BaseMutation):
    class Input:
        date = graphene.Date()
        start_time = graphene.String(required=True)
        end_time = graphene.String(required=True)

    time_slots = graphene.List(SlotType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        start_time = datetime.strptime(input.get('start_time'), "%I:%M %p").time()
        end_time = datetime.strptime(input.get('end_time'), "%I:%M %p").time()
        DateTimeSlots.objects.filter(date=input.get('date'), start_time=start_time,
                                     end_time=end_time).update(status=DateTimeSlots.ONHOLD)
        time_slots = DateTimeSlots.objects.filter(date=input.get('date'), start_time=start_time, end_time=end_time)
        return cls(message="Status updated", time_slots=time_slots)


class SaveServiceDetailsMutation(BaseMutation):
    class Input:
        category = graphene.String(required=True)
        service = graphene.String(required=True)
        staff = graphene.String(required=True)
        date = graphene.Date()
        start_time = graphene.String(required=True)
        end_time = graphene.String(required=True)
        basic_details = DetailInput()

    appointment_details = graphene.Field(AppointmentType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        data = {'category_id': cls.get_id(input.get('category')), 'service_id': cls.get_id(input.get('service')),
                'staff_id': cls.get_id(input.get('staff'))}
        date = input.get('date')
        time_slot = DateTimeSlots.objects.filter(date=date, start_time=datetime.strptime(input.get('start_time'),
                                                                                         "%I:%M %p").time(),
                                                 end_time=datetime.strptime(input.get('end_time'),
                                                                            "%I:%M %p").time(), staff_id=cls.get_id(input.get('staff'))).first()
        time_slot.status = DateTimeSlots.BOOKED
        time_slot.save()
        data['date_range'] = time_slot
        basic_details = input.get('basic_details')
        customer_data = {}
        for key, value in basic_details.items():
            customer_data[key] = value
        customer, created = Customers.objects.get_or_create(**customer_data)
        data['customer'] = customer
        if ServiceDetail.objects.filter(**data).exists():
            raise GraphQLError('Your Appointment already exists')
        service = ServiceDetail.objects.create(**data)
        return cls(message="Appointment Booked Successfully", appointment_details=service)


class CreatePostMutation(BaseMutation):
    class Input:
        title = graphene.String(required=True)
        subtitle = graphene.String(required=True)
        img = graphene.String()
        description = graphene.String(required=True)
        description1 = graphene.String()
        description2 = graphene.String()
        description3 = graphene.String()
        description4 = graphene.String()

    post = graphene.Field(PostType)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        title = input.get('title')
        subtitle = input.get('subtitle')
        post_img = input.get('img')
        description = input.get('description')
        data = {'title': title, 'subtitle': subtitle, 'post_img': post_img}
        descript_dict = {'description': description}
        for d in range(1, 5):
            if 'description' + str(d) in input:
                descript_dict['description' + str(d)] = input.get('description' + str(d))
        data['description'] = descript_dict
        if Posts.objects.filter(**data).exists():
            raise GraphQLError('Your Posts already exists')
        Posts.objects.create(**data)
        post = Posts.objects.filter(**data).first()
        return cls(message="Added post successfully", post=post)


# Admin login
class ObtainToken(graphql_jwt.ObtainJSONWebToken):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)
