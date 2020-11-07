from django import forms
from .models import MessageFeatures


class ImageMessageForm(forms.Form):
	image = forms.ImageField(label='')