# import necessary Django modules
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand

# To run the command:
# python manage.py create_manager <username> <email> <password>


class Command(BaseCommand):
    help = "Create a manager user with a specified username, email, and password"

    # Add required arguments for the command
    def add_arguments(self, parser):
        parser.add_argument("username", type=str, help="The username for the new manager user")
        parser.add_argument("email", type=str, help="The email for the new manager user")
        parser.add_argument("password", type=str, help="The password for the new manager user")

    # Handle method to execute the command
    def handle(self, *args, **options):
        # Get input arguments
        username = options["username"]
        email = options["email"]
        password = options["password"]

        # Create a new user with the given input
        user = User.objects.create_user(username=username, email=email, password=password)

        # Add the user to the manager group
        manager_group = Group.objects.get(name="manager")
        user.groups.add(manager_group)

        # Save the user
        user.save()

        # Output success message
        self.stdout.write(self.style.SUCCESS(f'Successfully created manager user "{username}"'))
