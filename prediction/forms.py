from django import forms
from django.utils.translation import gettext_lazy as _

class CodeForm(forms.Form):
    code = forms.CharField(
        label=_('股票代码'),
        required=True,
        error_messages={'required':'这是必填栏。'},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '填写股票代码...'}))
    
    class Meta:
        fields = ('code', )
        