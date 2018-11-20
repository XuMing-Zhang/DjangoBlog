from django import forms
from django.forms import fields
from captcha.fields import CaptchaField
from blog import models


class CommentForm(forms.Form):
    name = fields.CharField(label='称呼', max_length=16, error_messages={
        'required': '请填写完整的称呼！',
        'max_length': '字段太长了，范围大于4个字符小于16个字符！'
    })

    email = fields.EmailField(label='邮箱', error_messages={
        'required': '请填写正确的邮箱地址！',
        'invalid': '邮箱格式不正确，例：XXX@email.com'
    })

    content = fields.CharField(label='评论', error_messages={
        'required': '内容不能为空，请填写！',
        'max_length': '评论内容太长，请删减！最多240字符。'
    }, widget=forms.Textarea)


class ContactForm(forms.Form):
    name = fields.CharField(label='称呼', max_length=16, error_messages={
        'required': '请填写完整的称呼！',
        'max_length': '字段太长了，范围大于4个字符小于16个字符！'
    })

    email = fields.EmailField(label='邮箱', error_messages={
        'required': '请填写正确的邮箱地址！',
        'invalid': '邮箱格式不正确，例：XXX@email.com'
    })

    content = fields.CharField(label='意见', error_messages={
        'required': '内容不能为空，请填写！',
        'max_length': '评论内容太长，请删减！最多240字符。'
    }, widget=forms.Textarea)

    captcha = CaptchaField(label='请输入验证码')


class BlogModelForm(forms.ModelForm):
    captcha = CaptchaField(label='请输入验证码')

    class Meta:
        model = models.Blog
        fields = ['title', 'content', 'catagory', 'tags']

    def __init__(self, *args, **kwargs):
        super(BlogModelForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "标题"
        # self.fields['author_user'].label = "作者"
        self.fields['content'].label = "内容"
        self.fields['catagory'].label = "分类"
        self.fields['tags'].label = "标签"


class LoginForm(forms.Form):
    username = fields.CharField(label='账号', max_length=16)
    password = fields.CharField(label='密码', widget=forms.PasswordInput())
    captcha = CaptchaField(label='请输入验证码')
