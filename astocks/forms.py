from django import forms
from django.utils.translation import gettext_lazy as _

class DateDataForm(forms.Form):
    beginindex = forms.IntegerField(label=_('起始索引'), required=True, error_messages={'required':'这是必填栏。'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    endindex = forms.IntegerField(label=_('结束索引'), required=True, error_messages={'required':'这是必填栏。'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    begindate = forms.CharField(label=_('起始日期'), required=True, error_messages={'required':'这是必填栏。'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    enddate = forms.CharField(label=_('结束日期'), required=True, error_messages={'required':'这是必填栏。'},
                                widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
    class Meta:
        fields = ('beginindex', 'endindex','begindate', 'enddate',)