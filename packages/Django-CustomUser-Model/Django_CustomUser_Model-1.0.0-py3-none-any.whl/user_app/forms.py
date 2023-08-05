from django import forms
from .models import CustomUserProfile
from allauth.account.forms import SignupForm



class CustomUserProfileSignupForm(SignupForm):
    first_name = forms.CharField(max_length=50, label='First Name', help_text='First Name', required=True)
    last_name = forms.CharField(max_length=50, label='Last Name', help_text='Last Name', required=True)

    def save(self, request):

        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(CustomUserProfileSignupForm, self).save(request)

        # Add your own processing here.

        # You must return the original result.
        return user
