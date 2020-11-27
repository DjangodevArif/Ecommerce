from django.core.management.base import BaseCommand
from ecom.models import CartItem

class Command(BaseCommand):
    def handle(self, *args, **options):
        CartItem.objects.all().delete()
        