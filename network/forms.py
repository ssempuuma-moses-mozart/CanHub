# forms.py
from django import forms
from .models import User, Group

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic', 'bio', 'nickname', 'location', 'who', 'gender', 'age', 'cancertype', 'cover']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
            'nickname': forms.TextInput(attrs={'placeholder': 'Nickname'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'who': forms.TextInput(attrs={'placeholder': 'Who you are'}),
            'gender': forms.TextInput(attrs={'placeholder': 'Gender'}),
            'age': forms.TextInput(attrs={'placeholder': 'Age'}),
            'cancertype': forms.TextInput(attrs={'placeholder': 'Cancer Type'}),
        }


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name', 'description', 'industry', 'location', 'rules', 'group_type', 
                  'cover_photo', 'profile_image', 'allow_invite', 'post_review']
        widgets = {
            'group_type': forms.RadioSelect,
            'rules': forms.Textarea(attrs={'rows': 5}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
