import base64
import mimetypes

import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from scissors.models import Category, Service, Staff, DateTimeSlots, ServiceDetail, Customers


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        interfaces = (relay.Node,)
        fields = '__all__'


class ServiceType(DjangoObjectType):
    created_at = graphene.Int()
    updated_at = graphene.Int()

    class Meta:
        model = Service
        interfaces = (relay.Node,)
        fields = '__all__'

    def resolve_image(self, info, **kwargs):
        if self.image:
            file_path = self.image.path
            mime_type, _ = mimetypes.guess_type(file_path)
            with open(file_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                return f"data:{mime_type or 'image/jpeg'};base64,{encoded_image}"
        return None

    def resolve_created_at(self, info, **kwargs):
        return int(self.created_at.timestamp()) if self.created_at else None
    def resolve_updated_at(self, info, **kwargs):
        return int(self.updated_at.timestamp()) if self.updated_at else None


class StaffType(DjangoObjectType):
    created_at = graphene.Int()
    updated_at = graphene.Int()
    class Meta:
        model = Staff
        interfaces = (relay.Node,)
        fields = '__all__'

    def resolve_profile_pic(self, info, **kwargs):
        print(self.profile_pic)
        if self.profile_pic:
            print("===========================")
            file_path = self.profile_pic.path
            mime_type, _ = mimetypes.guess_type(file_path)
            print(mime_type)
            with open(file_path, 'rb') as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
                return f"data:{mime_type or 'image/jpeg'};base64,{encoded_image}"
        return None
    def resolve_created_at(self, info, **kwargs):
        return int(self.created_at.timestamp()) if self.created_at else None
    def resolve_updated_at(self, info, **kwargs):
        return int(self.updated_at.timestamp()) if self.updated_at else None



class SlotType(DjangoObjectType):
    start_time = graphene.String()
    end_time = graphene.String()
    class Meta:
        model = DateTimeSlots
        fields = '__all__'
        interfaces = (relay.Node,)

    def resolve_start_time(self, info, **kwargs):
        return self.start_time.strftime("%I:%M %p")

    def resolve_end_time(self, info, **kwargs):
        return self.end_time.strftime("%I:%M %p")

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customers
        interfaces = (relay.Node,)
        fields = '__all__'

class AppointmentType(DjangoObjectType):
    class Meta:
        model = ServiceDetail
        fields = '__all__'
        interfaces = (relay.Node,)
