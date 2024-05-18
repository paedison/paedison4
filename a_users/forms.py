from django import forms

from a_users import models as user_models


class ProfileForm(forms.ModelForm):
    class Meta:
        model = user_models.Profile
        exclude = ['user']
        labels = {
            'realname': 'Name',
        }
        widgets = {
            'image': forms.FileInput(),
            'bio': forms.Textarea(attrs={'rows': 3})
        }
