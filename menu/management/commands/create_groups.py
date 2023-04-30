from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Create manager and customer groups with relevant permissions'

    def handle(self, *args, **options):
        # Create manager group
        manager_group, created = Group.objects.get_or_create(name='manager')

        # Assign permissions to the manager group
        manager_permissions = Permission.objects.filter(
            content_type__app_label='menu',
            codename__in=['add_dish', 'change_dish', 'delete_dish', 'add_category', 'change_category',
                          'delete_category', 'add_delivery', 'change_delivery', 'delete_delivery']
        )
        manager_group.permissions.set(manager_permissions)
        manager_group.save()

        # Create customer group
        customer_group, created = Group.objects.get_or_create(name='customer')

        # Assign any necessary permissions to the customer group
        customer_permissions = Permission.objects.filter(
            content_type__app_label='menu',
            codename__in=[]
        )
        customer_group.permissions.set(customer_permissions)
        customer_group.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully created manager and customer groups with relevant permissions'))
