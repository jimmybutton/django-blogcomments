from django.forms import ModelForm
from django.core.exceptions import ValidationError
from .models import Comment

class CommentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        """
        Save the request with the form so it can be accessed in clean() to do recaptcha
        and name validation
        """
        self.request = kwargs.pop('request', None)
        super(CommentForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Comment
        fields = ['name', 'comment']
    
    def clean_name(self):
        """Make sure people don't use my name"""
        data:str = self.cleaned_data['name']
        if not self.request.user.is_authenticated and data.lower().strip() == 'samuel':
            raise ValidationError("Sorry, you cannot use this name.")

        return data