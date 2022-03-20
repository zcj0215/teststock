from django import forms
from .models import StockChoose
from accounts.models import Persons
from boards.models import Board
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
        
class StockChooseForm(forms.ModelForm):
    pick_date = forms.DateField(
        label=_('选股日期'),
        required=True,
        error_messages={'required':'这是必填栏。'},
        widget=forms.DateInput(attrs={'type': 'date'}))
    code = forms.CharField(
        label=_('股票代码'),
        required=True,
        error_messages={'required':'这是必填栏。'},
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(
        label=_('股票名称'),
        required=True,
        error_messages={'required':'这是必填栏。'},
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    reasons = forms.CharField(
        label=_('选股理由'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    boards = forms.ModelMultipleChoiceField(
        label=_('热点题材'),
        required=False,
        queryset=Board.objects.all(),
        widget=forms.CheckboxSelectMultiple)
    short = forms.CharField(
        label=_('警惕缺点'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    ndperformance = forms.CharField(
        label=_('次日表现'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    tenday_limits = forms.IntegerField(
        label=_('10日涨停次数'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    summary = forms.CharField(
        label=_('经验总结'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    person =  forms.ModelChoiceField(
        label=_('选股人'),
        queryset=Persons.objects.all().order_by('id'), 
        required=True,
        error_messages={'required':'这是必填栏。'})
   
    
    class Meta:
        model = StockChoose
        fields = ['pick_date', 'code', 'name', 'reasons', 'boards', 'short', 'ndperformance', 
                  'tenday_limits', 'summary', 'person']