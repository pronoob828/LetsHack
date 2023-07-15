from django import forms
from .models import Room,Post,Comment,Topic

class RoomCreationForm(forms.ModelForm):
    
    class Meta:
        model = Room
        fields = ('name','description','is_private','topic',)
        widgets = { 
            'name': forms.TextInput(attrs={'class':'bg-dark text-white form-control'}),
            'description': forms.Textarea(attrs={'class':'bg-dark text-white form-control'}),
            'is_private': forms.CheckboxInput(attrs={'class':'form-check',}),
            'topic': forms.Select(attrs={'class':'form-control text-white bg-dark'}),
        }

class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control bg-dark text-white'}),
            'content': forms.Textarea(attrs={'class':'form-control bg-dark text-white'}),
        }

class CommentCreationForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'class':'form-control bg-dark text-white'}),
        }
