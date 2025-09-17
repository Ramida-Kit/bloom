
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import ComedianUser

class ComedianUserCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

	class Meta:
		model = ComedianUser
		fields = ('username', 'email')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user
from django.contrib import messages

def login_view(request):
	if request.method == 'POST':
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			return redirect('main')
		else:
			messages.error(request, 'Invalid username or password.')
	else:
		form = AuthenticationForm()
	return render(request, 'users/login.html', {'form': form})

def logout_view(request):
	logout(request)
	return redirect('login')

def register_view(request):
	if request.method == 'POST':
		form = ComedianUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect('main')
		else:
			messages.error(request, 'Registration error. Please check the form.')
	else:
		form = ComedianUserCreationForm()
	return render(request, 'users/register.html', {'form': form})
