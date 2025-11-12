"""Management command to create user accounts for employees."""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from employees.models import Employee


class Command(BaseCommand):
    help = 'Create user accounts for all employees that do not have one'

    def add_arguments(self, parser):
        parser.add_argument(
            '--default-password',
            type=str,
            default='employee123',
            help='Default password for new employee accounts (default: employee123)',
        )

    def handle(self, *args, **options):
        default_password = options['default_password']
        employees_without_users = Employee.objects.filter(user__isnull=True)
        
        if not employees_without_users.exists():
            self.stdout.write(self.style.SUCCESS('All employees already have user accounts!'))
            return
        
        created_count = 0
        for employee in employees_without_users:
            # Create username from email
            username = employee.email.split('@')[0]
            
            # Check if username already exists, append number if needed
            original_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            # Create user account
            user = User.objects.create_user(
                username=username,
                email=employee.email,
                password=default_password,
                first_name=employee.first_name,
                last_name=employee.last_name,
            )
            
            # Link to employee
            employee.user = user
            employee.save()
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(
                    f'Created account for {employee.first_name} {employee.last_name} '
                    f'(username: {username}, password: {default_password})'
                )
            )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\nSuccessfully created {created_count} employee accounts!'
            )
        )
        self.stdout.write(
            self.style.WARNING(
                '\nIMPORTANT: Employees should change their passwords after first login.'
            )
        )
