from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.html import format_html
from django.contrib.auth.models import User
from .models import Persons
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(label=_('姓'),max_length=12, min_length=1, required=True, help_text='必填项。',
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    last_name = forms.CharField(label=_('名'),max_length=12, min_length=1, required=True, help_text='必填项。',
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    email = forms.EmailField(label=_('电子邮件'),max_length=254,required=True, help_text='必填项。 提供有效的电子邮件地址.',
                               widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label=_('密码'),
                               widget=(forms.PasswordInput(attrs={'class': 'form-control'})),
                               help_text= format_html('<ul><li>您的密码不能与您的其他个人信息过于相似。</li><li>您的密码必须至少包含 8 个字符。</li><li>您的密码不能是常用密码。</li><li>您的密码不能完全是数字。</li></ul>'))
    password2 = forms.CharField(label=_('确认密码'), widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                               help_text=_('只需输入相同的密码，进行确认'))
    username = forms.CharField(
        label=_('用户名'),
        max_length=150,
        help_text=_('必填项。 最多150个字符。 仅限字母、数字和@/./+/-/_。'),
        validators=[UnicodeUsernameValidator()],
        error_messages={'unique': _("具有该用户名的用户已存在。")},
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        
class SignInForm(forms.Form):
    username = forms.CharField(
        label=_('用户名'),
        required=True,
        error_messages={'required':'这是必填栏。'},
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label=_('密码'), 
        required=True,
        error_messages={'required':'这是必填栏。'},
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'password',)
        

class PersonsForm(forms.ModelForm):
    name = forms.CharField(
        label=_('选股人'),
        required=True,
        error_messages={'required':'这是必填栏。'},
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        label=_('说明'),
        required=True,
        error_messages={'required':'这是必填栏。'},
        widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Persons
        fields = ['name', 'description']