from django import forms

from a_inbox import models as inbox_models


class InboxNewMessageForm(forms.ModelForm):
    class Meta:
        model = inbox_models.InboxMessage
        fields = ['body']
        labels = {
            'body': '',
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Add message...',
            }),
        }
