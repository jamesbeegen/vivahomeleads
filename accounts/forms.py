from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from leads.models import Profile




class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    phone = forms.CharField(max_length=10, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=40, required=True)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','email')
class ProfileForm(forms.ModelForm):
    class Meta:
        model= Profile
        fields = ('phone',)