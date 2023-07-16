from django import forms
from .models import *
from django.forms import ClearableFileInput
from .widgets import ClearableMultipleFileInput
from markdownfield.forms import MarkdownFormField ,MDEWidget


class RoomCreationForm(forms.ModelForm):
    
    class Meta:
        model = Room
        fields = ('name','description','is_private','topic',)
        widgets = { 
            'name': forms.TextInput(attrs={'class':'bg-dark text-white form-control'}),
            'description': MDEWidget(attrs={'class':'bg-dark text-white form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class':'form-check',}),
            'topic': forms.Select(attrs={'class':'form-control text-white bg-dark'}),
        }

class RoomFileForm(forms.ModelForm):
    file = forms.FileField(required=False,widget=ClearableMultipleFileInput())
    class Meta:
        model = RoomFile
        fields = ['file']

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control bg-dark text-white'}),
            'content': MDEWidget(attrs={'class':'bg-dark text-white form-control'}),
        }

class PostFileForm(forms.ModelForm):
    file = forms.FileField(required=False,widget=ClearableMultipleFileInput())
    class Meta:
        model = PostFile
        fields = ['file']
        

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class':'form-control bg-dark text-white'}),
        }
