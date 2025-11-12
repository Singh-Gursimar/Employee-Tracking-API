"""
App configuration for employees app.

This file tells Django about our app and lets us do setup
when the app loads (like registering signals).
"""
from django.apps import AppConfig


class EmployeesConfig(AppConfig):
    """Configuration for the employees app."""
    
    default_auto_field = "django.db.models.BigAutoField"  # Default ID field type
    name = "employees"  # App name - must match the folder name!

    def ready(self):
        """
        Import signals when app is ready.
        
        This method is called when Django starts up. We import our signals
        here so they get registered and start listening for events.
        
        IMPORTANT: Don't put this import at the top of the file!
        It needs to be here in ready() to avoid circular import issues.
        """
        import employees.signals  # This registers our auto-account-creation signal!
