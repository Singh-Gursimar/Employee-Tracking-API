"""
Forms for employee portal.

Forms in Django are like HTML forms but with server-side validation!
They handle all the messy stuff like checking if fields are filled out,
validating email addresses, etc.
"""
from django import forms
from attendance.models import AttendanceRecord


class EmployeeLoginForm(forms.Form):
    """
    Form for employee login.
    
    This is a simple form with just username and password.
    We're using forms.Form (not forms.ModelForm) because we're not
    saving this to a database - we're just using it for authentication.
    """
    username = forms.CharField(
        max_length=150,  # Django's default max username length
        widget=forms.TextInput(attrs={  # Widget controls how the HTML input looks
            'placeholder': 'Enter your username',  # Gray text that disappears when you type
            'autofocus': True,  # Cursor starts here when page loads - nice UX touch!
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={  # PasswordInput hides the text as you type
            'placeholder': 'Enter your password',
        })
    )


class AttendanceMarkForm(forms.Form):
    """
    Form for marking attendance.
    
    This lets employees mark themselves present, absent, etc.
    Notice we're not using ModelForm here either - we manually handle
    saving in the view because we have custom logic (like checking for notes).
    """
    status = forms.ChoiceField(
        choices=AttendanceRecord.Status.choices,  # Get the choices from our model (Present, Absent, etc.)
        widget=forms.Select(attrs={'class': 'form-control'})  # Add CSS class for styling
    )
    
    check_in_time = forms.TimeField(
        required=False,  # Optional field - not everyone tracks exact times
        widget=forms.TimeInput(attrs={
            'type': 'time',  # HTML5 time picker - shows a nice time selector in browser!
            'class': 'form-control'
        })
    )
    
    check_out_time = forms.TimeField(
        required=False,  # Also optional
        widget=forms.TimeInput(attrs={
            'type': 'time',
            'class': 'form-control'
        })
    )
    
    notes = forms.CharField(
        required=False,  # Optional in the form, but we enforce it in the view for absences!
        widget=forms.Textarea(attrs={  # Textarea = multi-line text input
            'rows': 3,  # Height of the box
            'placeholder': 'Enter any notes or reasons for absence...',
            'class': 'form-control'
        })
    )
