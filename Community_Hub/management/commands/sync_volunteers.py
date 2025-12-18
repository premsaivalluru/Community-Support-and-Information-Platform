from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Community_Hub.models import Volunteer
from django.contrib.auth.models import Permission


from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Permission
from Community_Hub.models import Volunteer

class Command(BaseCommand):
    help = "Creates Django admin users for all volunteers without user accounts and assigns proper permissions."

    DEFAULT_PASSWORD = "volunteer123"  # Volunteers will log in with this

    def handle(self, *args, **options):
        count = 0
        # Permissions the volunteer should have
        permission_codenames = ['view_post', 'change_post']

        for vol in Volunteer.objects.filter(user__isnull=True):
            # Create the Django user
            auth_user = User.objects.create_user(
                username=vol.username or f"volunteer_{vol.id}",
                password=self.DEFAULT_PASSWORD,
                first_name=vol.first_name,
                last_name=vol.last_name,
                is_staff=True,
                is_superuser=False
            )

            # Assign permissions
            for codename in permission_codenames:
                try:
                    perm = Permission.objects.get(codename=codename)
                    auth_user.user_permissions.add(perm)
                except Permission.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"⚠ Permission '{codename}' does not exist."))

            # Link back to Volunteer
            vol.user = auth_user
            vol.save()

            self.stdout.write(self.style.SUCCESS(f"✅ Created admin user for volunteer: {vol.username}"))
            count += 1

        if count == 0:
            self.stdout.write(self.style.WARNING("No new volunteers found without users."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Total volunteers created: {count}"))
