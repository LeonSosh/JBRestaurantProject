from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

# run python manage.py create_manager <username> <email> <password>


class Command(BaseCommand):
    help = "Create a manager user with a specified username, email, and password"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="The username for the new manager user")
        parser.add_argument("email", type=str, help="The email for the new manager user")
        parser.add_argument("password", type=str, help="The password for the new manager user")

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]

        user = User.objects.create_user(username=username, email=email, password=password)
        manager_group = Group.objects.get(name="manager")
        user.groups.add(manager_group)
        user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created manager user "{username}"'))
