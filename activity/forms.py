from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    text = forms.CharField(label='', widget=forms.Textarea(attrs={'rows':4}))

    class Meta:
        model = Comment
        fields = ('text',)
