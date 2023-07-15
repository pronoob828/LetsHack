from django import forms
from .models import Room

class RoomCreationForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ('name','description','is_private')
        widgets = { 
            'name': forms.TextInput(attrs={'class':'form-control bg-dark text-white'}),
            'description': forms.Textarea(attrs={'class':'form-control bg-dark text-white'}),
            'is_private': forms.CheckboxInput(attrs={'class':'form-check'}),
        }
