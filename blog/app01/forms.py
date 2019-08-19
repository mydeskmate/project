from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
class RegisterForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control'}),
        required=True,  #默认True
        max_length=8,
        min_length=2,
        error_messages = {
            'required': '不能为空',
            'max_length': '太长',
            'min_length': '太短',
        }
    )
    nickname = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    password = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control','type':'password'})
    )
    password2 = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control','type':'password'})
    )
    email = fields.EmailField(
        widget=widgets.EmailInput(attrs={'class': 'form-control'})
    )
    avatar = fields.FileField(
        required=False,
        widget=widgets.FileInput(attrs={'id':'imgSelect','class':'f1'})
    )
    code = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )

    # 封装request
    def __init__(self,request,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        self.request = request

    def clean_code(self):
        input_code = self.cleaned_data['code']
        session_code = self.request.session.get('code')
        if input_code.upper() == session_code.upper():
            return input_code
        raise ValidationError("验证码错误")

    def clean(self):
        p1 = self.cleaned_data.get('password')
        p2 = self.cleaned_data.get('password2')
        if p1 == p2:
            return None
        else:
            self.add_error("password2",ValidationError("密码不一致"))


class ArticleForm(Form):
    title = fields.CharField(max_length=64)
    content = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'i1'})
    )

    def clean_content(self):
        old = self.cleaned_data['content']
        from utils.xss import xss
        return xss(old)

