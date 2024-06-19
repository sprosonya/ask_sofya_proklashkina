from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import CharField

# class UsernameField(CharField):
#     def validate(self, value):
#         super().validate(value)
#         if value == '123':
#             raise ValidationError("No 123!!")
from app.models import User, Question, Answer, Profile


class QuestionForm(forms.ModelForm):
    title = forms.CharField()
    text = forms.CharField()
    tag = forms.CharField()

    def __init__(self, user, **kwargs):
        self._user = user
        super(QuestionForm, self).__init__(**kwargs)
    class Meta:
        model = Question
        fields = ['title', 'text', 'tag']

class AnswerForm(forms.ModelForm):
    text = forms.CharField()
    class Meta:
        model = Answer
        fields = ['text']
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


    # def clean_username(self):
    #     username = self.cleaned_data['username']
    #     username = username.strip()
    #     if username != 'test':
    #         raise ValidationError("Wrong username")
    #     return username

class SettingsForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))

    def __init__(self, user, **kwargs):
        self._user = user
        super(SettingsForm, self).__init__(**kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        user_with_email = User.objects.filter(email=email).first()
        user_with_username = User.objects.filter(username=username).first()
        if (user_with_email != None) or (user_with_username != None):
            if ((user_with_username != None) and username != self._user.username) or (
                    (user_with_email != None) and email != self._user.email):
                raise forms.ValidationError('Username or Email is already registered')

    def save(self):
        user = self._user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        profile = Profile.objects.filter(user=user).first()
        if self.cleaned_data.get('avatar'):
            profile.avatar = self.cleaned_data['avatar']
        profile.save()

        return user

class SettingsFormOld(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password' ]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.save()
        profile = Profile(user=user)
        profile.save()
        return user