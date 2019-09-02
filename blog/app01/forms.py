from django.forms import Form
from django.forms import fields
from django.forms import widgets
from django.core.exceptions import ValidationError
from app01 import models


class RegisterForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'class':'form-control'}),
        required=True,  #默认True
        max_length=32,
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
    # blog_id = request.session.get('blog_id')
    # print(request)
    title = fields.CharField(max_length=64)
    summary = fields.CharField(
        widget=widgets.Textarea(attrs={'rows': 3, 'cols': 60})
    )
    type = fields.ChoiceField(
        choices=models.Article.type_choices,
        widget=widgets.Select(),
    )
    category = fields.ChoiceField(
        widget=widgets.Select(),
        # choices = models.Category.objects.filter(blog_id=1).values_list('nid', 'title')
    )
    tags = fields.MultipleChoiceField(
        widget=widgets.CheckboxSelectMultiple(),
        # choices=models.Tag.objects.filter(blog_id=1).values_list('nid', 'title')
    )
    content = fields.CharField(
        widget=widgets.Textarea(attrs={'id': 'i1'})
    )


    def __init__(self,request,*args,**kwargs):
        # 封装 request  从session中获取数据
        super(ArticleForm,self).__init__(*args,**kwargs)
        self.request = request
        self.fields['category'].choices = models.Category.objects.filter(blog_id=request.session.get('blog_id')).values_list('nid', 'title')
        self.fields['tags'].choices = models.Tag.objects.filter(blog_id=request.session.get('blog_id')).values_list('nid', 'title')



    # def clean_content(self):
    #     """
    #     xss防护
    #     """
    #     old = self.cleaned_data['content']
    #     from utils.xss import xss
    #     return xss(old)



class UserinfoForm(Form):
    """
    用户个人信息页
    """
    # username = fields.CharField(
    #     widget=widgets.TextInput(attrs={'class':'form-control'}),
    #     required=True,  #默认True
    #     max_length=32,
    #     min_length=2,
    #     error_messages = {
    #         'required': '不能为空',
    #         'max_length': '太长',
    #         'min_length': '太短',
    #     }
    # )
    nickname = fields.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    email = fields.EmailField(
        widget=widgets.EmailInput(attrs={'class': 'form-control'})
    )
    site = fields.CharField(
        required=False,
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    theme = fields.CharField(
        required=False,
        widget=widgets.TextInput(attrs={'class': 'form-control'})
    )
    avatar = fields.FileField(
        required=False,
        widget=widgets.FileInput(attrs={'id':'imgSelect','class':'f1'})
    )

    # 封装request
    def __init__(self,request,*args,**kwargs):
        super(UserinfoForm, self).__init__(*args,**kwargs)
        self.request = request

