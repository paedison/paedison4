from django import forms

from a_posts import models as post_models


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = post_models.Post
        fields = ['url', 'body', 'tags']
        labels = {
            'body': 'Caption',
            'tags': 'Category',
        }
        widgets = {
            'body': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Add a caption...',
                    'class': 'font1 text-4xl',
                }
            ),
            'url': forms.TextInput(attrs={'placeholder': 'Add url...'}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class PostEditForm(forms.ModelForm):
    class Meta:
        model = post_models.Post
        fields = ['body', 'tags']
        labels = {
            'body': '',
            'tags': 'Category',
        }
        widgets = {
            'body': forms.Textarea(
                attrs={'rows': 3, 'class': 'font1 text-4xl'}
            ),
            'tags': forms.CheckboxSelectMultiple(),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = post_models.Comment
        fields = ['body']
        labels = {'body': ''}
        widgets = {'body': forms.TextInput(attrs={'placeholder': 'Add comment...'})}


class ReplyCreateForm(forms.ModelForm):
    class Meta:
        model = post_models.Reply
        fields = ['body']
        labels = {'body': ''}
        widgets = {
            'body': forms.TextInput(
                attrs={'placeholder': 'Add reply...', 'class': '!text-sm'}
            )
        }
