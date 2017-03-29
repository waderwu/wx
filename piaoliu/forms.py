from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'placeholder':'Password'}))

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=254)
    email = forms.EmailField(label='e-mail')
    xuehao = forms.CharField(max_length=20)
    banji = forms.CharField(max_length=20)
    phoneNumber = forms.CharField(max_length=20)
    wechat = forms.CharField(max_length=20)
    password1 = forms.CharField(label='Password',
                               widget=forms.PasswordInput({
                                   'placeholder':'Password'}))
    password2= forms.CharField(label='confirm',
                               widget=forms.PasswordInput({
                                   'placeholder':'Password'}))


class search_form(forms.Form):
    keyword = forms.CharField(max_length=50)


class sort_form(forms.Form):
    sort_choices = (
        ('rating','豆瓣评分'),
        ('borrowed','被借数量'),
        ('onshelf','在架的'),
    )
    sort_way = forms.ChoiceField(choices=sort_choices)

