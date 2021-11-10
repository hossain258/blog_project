from django import forms
from .models import Content, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Validation check --> 1. Object level validation, 2. Full validation


class ContentForm(forms.ModelForm):

    class Meta:
        model = Content
        # fields = "__all__"
        exclude = ["user", ]

    def clean_text(self):
        print("Validating text inside forms")
        text = self.cleaned_data.get("text")
        print(text)

        if "django" not in text:
            raise forms.ValidationError("Blog is not about Django")

        return text

    def clean_title(self):
        title = self.cleaned_data.get("title")
        # user = self.cleaned_data.get("user")  # it is none
        user = self.instance.user  # Since we made it in view as form.instance.user = request.user
        print("User ", user.username)
        print("Title ", title)

        qs = Content.objects.filter(user=user, title=title)
        if qs.exists():
            raise forms.ValidationError("User has already created a blog of this title")

        return title



class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField()

    def clean_username(self):
        username = self.cleaned_data.get("username")
        qs = User.objects.filter(username=username)
        if not qs.exists():
            raise forms.ValidationError("Username not found")
        return username

    def clean_password(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        auth = authenticate(username=username, password=password) # return user object
        if not auth:
            raise forms.ValidationError("Username and Password did not match")       

        return password



# class UserRegistrationForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = "__all__"


