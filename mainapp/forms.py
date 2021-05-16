from django import forms
from django.forms import fields
from .models import Link

class LinkForm(forms.ModelForm):
    class Meta:
        model = Link
        exclude = ('uploaded_by','likes',)