from django import forms
from api.models import UserProfile, Work, Language

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['native_language', 'target_language', 'difficulty_score', 'themes']
        widgets = {
            'themes': forms.CheckboxSelectMultiple,
        }

class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['title', 'author', 'language', 'difficulty', 'type', 'amazon_link', 'cover_url']
        widgets = {
            'language': forms.Select(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'difficulty': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'amazon_link': forms.URLInput(attrs={'class': 'form-control'}),
            'cover_url': forms.URLInput(attrs={'class': 'form-control'}),
        }