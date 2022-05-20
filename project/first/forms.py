from django import forms
from django.forms import ModelForm, TextInput
from .models import Tools
class UserForm(forms.Form):
    first_name= forms.CharField(max_length=100)
    last_name= forms.CharField(max_length=100)
    email= forms.EmailField()
class ltiForm(forms.Form):
    lti_message_type= forms.CharField(max_length=100)
    lti_version= forms.CharField(max_length=100)
    resource_link_id= forms.CharField(max_length=100)
    oauth_consumer_key= forms.CharField(max_length=100)
    oauth_signature_method= forms.CharField(max_length=100)
    oauth_version= forms.CharField(max_length=100, )
    oauth_nonce = forms.CharField(max_length=100,widget = forms.HiddenInput(),required = False)
    oauth_timestamp = forms.CharField(max_length=100,widget = forms.HiddenInput(),required = False)
    oauth_signature = forms.CharField(max_length=100,widget = forms.HiddenInput(),required = False)

class ToolsForm(ModelForm):
    class Meta:
        model = Tools
        fields = ['consumer_key', 'consumer_secret', 'launch_url']

        widgets = {
            "consumer_key": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Consumer key'
            }),
            "consumer_secret": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Consumer secret'
            }),
            "launch_url": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'URL'
            })
        }


    # consumer_key = forms.CharField(max_length=20)
    # consumer_secret = forms.CharField(max_length=20)
    # launch_url = forms.URLField()
    # lti_message_type = forms.CharField(max_length=30)
    # lti_version = forms.CharField(max_length=10)
    # resource_link_id = forms.CharField(max_length=20)
