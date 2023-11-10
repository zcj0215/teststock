from django import forms

from .models import Topic, Post
from django.utils.translation import gettext_lazy as _

class NewTopicForm(forms.ModelForm):
    subject = forms.CharField(label=_('标题'))
    message = forms.CharField(
        label=_('信息内容'),
        widget=forms.Textarea(
            attrs={'rows': 5, 'placeholder': '说说您的想法?'}
        ),
        max_length=4000,
        help_text='文本的最大长度为 2000。'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']
        
class PostForm(forms.ModelForm):
    message = forms.CharField(
        label=_('信息内容'),
        widget=forms.Textarea(
            attrs={'rows': 5}
        )
    )
                            
    class Meta:
        model = Post
        fields = ['message', ]
        
class CodeForm(forms.Form):
    code = forms.CharField(
        required=True,
        error_messages={'required':'这是必填栏。'},
        widget=forms.TextInput(attrs={'class': 'form-control','placeholder': '填写股票代码...'}))
    
    class Meta:
        fields = ('code', )
