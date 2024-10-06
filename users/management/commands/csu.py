from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create_superuser(email="admin@example.com", password="0013")
        user.is_active = True
        user.save()
