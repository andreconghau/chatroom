from django import forms
from .models import Room

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'host', 'name', 'description'] # __all__ for all fields