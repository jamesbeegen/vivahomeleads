from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import SignUpForm, ProfileForm
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if signup_form.is_valid()and profile_form.is_valid():
            user = signup_form.save()
            login(request, user)
            return redirect('leads')

    else:
        profile_form = ProfileForm()
        signup_form = SignUpForm()
    return render(request, 'signup.html', {'signup_form': signup_form, 'profile_form': profile_form})




