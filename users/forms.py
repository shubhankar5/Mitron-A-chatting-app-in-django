from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Address
from .validators import validate_dob


class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username','email','password1','password2']


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['email']


class ProfileCreateForm(forms.ModelForm):
	dob = forms.DateField(validators = [validate_dob], label='Date of Birth')

	class Meta:
		model = Profile
		fields = ['first_name', 'last_name', 'sex', 'dob', 'bio']


class AddressForm(forms.ModelForm):
	
	class Meta:
		model = Address
		fields = ['city','state','country']


class ProfileUpdateForm(forms.ModelForm):
	
	class Meta:
		model = Profile
		fields = ['sex', 'bio']


class ProfilePictureForm(forms.ModelForm):
	display_picture = forms.ImageField(label='')

	class Meta:
		model = Profile
		fields = ['display_picture']