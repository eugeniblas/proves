from django import forms
from .models import Buzz


class PostForm(forms.ModelForm):
    class Meta :
        model = Buzz
        fields = ('title','text',)
        