from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
class RegisterForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    nickname = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    password = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control'})
    )
    password2 = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    email = fields.EmailField(
        widget=widgets.EmailInput(attrs={'class': 'form-control'})
    )
    avatar = fields.FileField(
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

