from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
class RegisterForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    password = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    password2 = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    avatar = fields.FileField(
        widget=widgets.FileInput(attrs={'id':'imgSelect','class':'f1'})
    )
    code = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )