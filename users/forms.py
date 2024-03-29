from django import forms
from users.models import UserProfile
from django.contrib.auth.forms import UserCreationForm,UserChangeForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ('username','email', 'mobile')


class UserEditForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ('username', 'nick_name', 'gender','email', 'mobile', 'image')


class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)

    def clean(self):
        pwd1 = self.cleaned_data["password1"]
        pwd2 = self.cleaned_data["password2"]

        if pwd1 != pwd2:
            raise forms.ValidationError("密码不一致")
        return self.cleaned_data