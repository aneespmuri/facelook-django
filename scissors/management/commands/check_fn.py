from django.core.management import BaseCommand
from django.db.models import Count

from scissors.models import Customers, ServiceDetail


class Command(BaseCommand):
    def handle(self, *args, **options):
        customers = Customers.objects.prefetch_related('servicedetail_set').all()
        for i in customers:
            print(i)