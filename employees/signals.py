"""
Signal handlers for employee model.

Signals are like event listeners - they automatically run code when something happens.
In this case, we want to create a user account every time a new employee is added!
"""
from django.db.models.signals import post_save  # This fires AFTER a model is saved
from django.dispatch import receiver  # Decorator to connect our function to the signal
from django.contrib.auth.models import User  # Django's built-in User model for authentication
from .models import Employee
import secrets  # For generating secure random strings
import string


def generate_temp_password(length=12):
    """
    Generate a secure temporary password.
    
    This creates a random password using letters, numbers, and special characters.
    We're not using this right now, but it's here if we want more security later!
    """
    alphabet = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


@receiver(post_save, sender=Employee)  # This decorator means "run this function after an Employee is saved"
def create_employee_user(sender, instance, created, **kwargs):
    """
    Automatically create a User account when a new Employee is created.
    
    This is the magic that makes it so admins don't have to manually create
    login accounts for every employee - it just happens automatically!
    
    Args:
        sender: The model class (Employee)
        instance: The actual employee object that was just saved
        created: Boolean - True if this is a new employee, False if updating existing
        **kwargs: Other stuff Django passes in (we don't need it)
    """
    # Only create a user if this is a NEW employee (not an update) and they don't already have a user
    if created and instance.user is None:
        # Generate username from email (everything before the @ symbol)
        # Example: "john.doe@company.com" becomes "john.doe"
        username = instance.email.split('@')[0]
        
        # Make sure the username is unique (in case we already have a john.doe)
        # If username exists, we'll try john.doe1, john.doe2, etc.
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1
        
        # Set a default password - in a real system, you'd want to email this
        # or force a password change on first login!
        temp_password = 'employee123'  
        # Alternative: use generate_temp_password() for a random secure password
        
        # Create the user account with Django's built-in User model
        user = User.objects.create_user(
            username=username,
            email=instance.email,
            password=temp_password,  # Django will hash this automatically
            first_name=instance.first_name,
            last_name=instance.last_name,
        )
        
        # Link the user to the employee (this creates the one-to-one relationship)
        instance.user = user
        instance.save(update_fields=['user'])  # Only update the 'user' field to avoid infinite loop
        
        # Print info to console so admin knows the credentials
        # In production, you'd send an email instead
        print(f"✓ Auto-created user account for {instance.first_name} {instance.last_name}")
        print(f"  Username: {username}")
        print(f"  Temporary Password: {temp_password}")
        print(f"  Employee should change password after first login!")
