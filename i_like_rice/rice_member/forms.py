#coding:utf-8
from captcha.fields import CaptchaField


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm 



class RegForm(forms.Form):
    """ for member register """
    email = forms.EmailField(label='email')
    username = forms.CharField(max_length=20, label='username')
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, label='password')
    password1 = forms.CharField(max_length=20,widget=forms.PasswordInput, label='password1')
    captcha = CaptchaField()
    
    def clean_email(self):
        try:
            User.objects.get(email=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        else:
            raise forms.ValidationError('此邮箱已被使用')

    def clean(self):
        super(RegForm, self).clean()
        username = self.cleaned_data.get('username', '')
        password = self.cleaned_data.get('password', '')
        password1 = self.cleaned_data.get('password1', '')
        if username and User.objects.filter(username=username).exists():
            raise forms.ValidationError(u'此用户名已被注册，请更换其他用户名')
        if password and password1 and password != password1:
            raise forms.ValidationError(u'两次输入的密码不一致')
        return self.cleaned_data


class LoginForm(AuthenticationForm):
    """ for user login with captcha """
    captcha = CaptchaField()
