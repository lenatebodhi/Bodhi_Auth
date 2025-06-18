from django.core.management.base import BaseCommand
from accounts.models import *
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Update unique_username field of BaseUser model'

    def handle(self, *args, **kwargs):
        # Calculate the date 365 days ago
        cutoff_date = datetime.now() - timedelta(days=365)
        
        # Query inactive users whose is_active is False for more than 365 days
        inactive_users = User.objects.filter(is_active=False, is_deleted=False, last_login__gt=cutoff_date)
        
        # Update is_deleted field to True for inactive users
        for user in inactive_users:
            user.is_deleted = True
            user.save()
            
        self.stdout.write(self.style.SUCCESS('Successfully updated is_deleted field for inactive users.'))