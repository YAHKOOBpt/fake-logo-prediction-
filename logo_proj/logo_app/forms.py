# logo_app/forms.py
from django import forms
from .models import LogoPrediction

class LogoPredictionForm(forms.ModelForm):
    class Meta:
        model = LogoPrediction
        fields = ['image']
